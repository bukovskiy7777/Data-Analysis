"""
Video Script Feature Extractor — Parallel Version
===================================================
pip install anthropic pandas tqdm
python analyze_scripts.py
"""

import os, json, time
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import anthropic

# ─── CONFIG ───────────────────────────────────────────
API_KEY     = os.getenv("ANTHROPIC_API_KEY", "api_key")
INPUT_FILE  = "Video scripts.csv"
OUTPUT_FILE = "scripts_features.csv"
TEXT_COLUMN = "Transcript"         # ← колонка с данными
MODEL       = "claude-haiku-4-5-20251001"
MAX_WORKERS = 2                   # параллельных запросов
RETRY_LIMIT = 3
RETRY_DELAY = 30

# ─── PROMPT ───────────────────────────────────────────
SYSTEM_PROMPT = """You are a video script analyst. Extract features from the script.
Return ONLY valid JSON, no markdown, no explanation.

{
  "hook_type": "problem|curiosity|contrarian|story|authority|question|other",
  "hook_length_words": <int>,
  "curiosity_gap": "yes|no",
  "emotional_intensity_hook": "low|medium|high",
  "product_in_hook": "yes|no",
  "time_to_product": "beginning|middle|end|none",
  "time_to_payoff": "early|middle|late",
  "narrative_structure": "Problem-Solution-Proof-CTA|Story-led|Educational|Contrarian|Other",
  "open_loop": "yes|no",
  "selling_points_count": <int>,
  "selling_point_density": <float>,
  "benefit_feature_ratio": "mostly_benefits|balanced|mostly_features",
  "mechanism_present": "yes|no",
  "proof_type": "none|scientific|authority|testimonial|social_proof|mixed",
  "language": "English|Spanish|Other",
  "conversational_score": "low|medium|high|very_high",
  "pronoun_you_count": <int>,
  "avg_sentence_length_words": <float>,
  "sentiment_trajectory": "<description>",
  "emotion_shift_after_hook": "<description>",
  "key_idea": "<one sentence>",
  "concept_cluster": "<category>"
}"""

# ─── CORE ─────────────────────────────────────────────
def analyze(client, text, idx):
    for attempt in range(RETRY_LIMIT):
        try:
            r = client.messages.create(
                model=MODEL, max_tokens=600,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": f"Script:\n\n{text}"}]
            )
            raw = r.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1].lstrip("json").strip()
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"\n[{idx}] JSON error: {e}")
        except anthropic.RateLimitError:
            print(f"\n[{idx}] Rate limit, sleeping {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"\n[{idx}] Error: {e}")
            time.sleep(RETRY_DELAY)
    return {"error": "failed"}

FEATURE_COLS = [
    "hook_type", "hook_length_words", "curiosity_gap", "emotional_intensity_hook",
    "product_in_hook", "time_to_product", "time_to_payoff", "narrative_structure",
    "open_loop", "selling_points_count", "selling_point_density", "benefit_feature_ratio",
    "mechanism_present", "proof_type", "language", "conversational_score",
    "pronoun_you_count", "avg_sentence_length_words", "sentiment_trajectory",
    "emotion_shift_after_hook", "key_idea", "concept_cluster"
]

def get_failed_indices(done_df):
    """Возвращает индексы строк где error=failed и все фичи пустые."""
    failed = set()
    for _, row in done_df.iterrows():
        if str(row.get("error", "")).strip() == "failed":
            feature_vals = [row.get(col) for col in FEATURE_COLS if col in done_df.columns]
            all_empty = all(pd.isna(v) or str(v).strip() in ("", "nan") for v in feature_vals)
            if all_empty:
                failed.add(int(row["original_index"]))
    return failed

# ─── MAIN ─────────────────────────────────────────────
def main():
    df = pd.read_csv(INPUT_FILE, encoding='cp1252')
    print(f"Loaded {len(df)} rows from {INPUT_FILE}")

    # Resume: определяем какие строки уже готовы
    done_indices = set()
    done_features = {}

    if os.path.exists(OUTPUT_FILE):
        done_df = pd.read_csv(OUTPUT_FILE)

        if "original_index" in done_df.columns:
            # Находим failed-строки для перезапуска
            failed_indices = get_failed_indices(done_df)
            if failed_indices:
                print(f"Found {len(failed_indices)} failed rows — will retry them")

            for _, row in done_df.iterrows():
                idx = int(row["original_index"])
                if idx in failed_indices:
                    continue  # пропускаем — уйдут в todo
                done_indices.add(idx)
                done_features[idx] = row.to_dict()

        print(f"Resuming: {len(done_indices)} valid rows already processed")

    # Строки для обработки
    todo = [(i, str(row[TEXT_COLUMN])) for i, row in df.iterrows()
            if i not in done_indices and str(row[TEXT_COLUMN]) not in ("", "nan")]
    print(f"To process: {len(todo)} rows with {MAX_WORKERS} workers\n")

    client = anthropic.Anthropic(api_key=API_KEY)
    results = dict(done_features)  # начинаем с уже готовых

    # Параллельная обработка
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(analyze, client, text, idx): idx
            for idx, text in todo
        }
        with tqdm(total=len(futures), desc="Analyzing") as pbar:
            for future in as_completed(futures):
                idx = futures[future]
                features = future.result()
                results[idx] = {"original_index": idx, **features}
                pbar.update(1)

                # Чекпоинт каждые 50 строк
                if len(results) % 50 == 0:
                    _save(df, results, OUTPUT_FILE)
                    pbar.write(f"✓ Checkpoint: {len(results)} rows saved")

    # Финальное сохранение
    _save(df, results, OUTPUT_FILE)
    print(f"\n✅ Done! Saved to: {OUTPUT_FILE}")
    print(f"   Total rows: {len(results)}")

# ─── SAVE: исходный CSV + новые колонки ───────────────
def _save(original_df, results, path):
    feature_rows = []
    for idx in sorted(results.keys()):
        r = results[idx]
        feature_rows.append(r)

    features_df = pd.DataFrame(feature_rows).set_index("original_index")

    # Джойним с оригинальным датафреймом
    merged = original_df.join(features_df, how="left")
    merged.to_csv(path, index=False)

if __name__ == "__main__":
    main()