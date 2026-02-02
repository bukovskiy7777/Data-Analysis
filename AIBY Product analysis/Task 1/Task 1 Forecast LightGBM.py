import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import numpy as np

# 1. Загрузка данных
df = pd.read_csv('E:\Саша\AIBY\Task 1 Dataset.csv')

# Преобразование столбца даты
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns={'Revenue ($)': 'y'}) # Переименовываем целевую переменную для удобства

# 2. Создание признаков из даты (Feature Engineering)
def create_time_features(df):
    """Создает временные признаки для модели LightGBM."""
    df['dayofmonth'] = df['Date'].dt.day
    df['dayofweek'] = df['Date'].dt.dayofweek
    df['month'] = df['Date'].dt.month
    df['year'] = df['Date'].dt.year
    df['is_weekend'] = (df['Date'].dt.dayofweek >= 5).astype(int)
    # Добавьте другие признаки, если нужно (например, праздники)
    return df

df = create_time_features(df)

# Определение признаков и целевой переменной
FEATURES = ['dayofmonth', 'dayofweek', 'month', 'year', 'is_weekend']
TARGET = 'y'

# 3. Фильтрация тренировочного и тестового периодов
train_start, train_end = '2022-03-01', '2022-09-30'
forecast_start, forecast_end = '2022-10-01', '2022-10-31'

train_df = df[(df['Date'] >= train_start) & (df['Date'] <= train_end)].copy()
# Для LightGBM мы должны создать "будущий" датафрейм вручную, так как его нет в исходных данных для прогноза.

# Создаем будущий датафрейм для октября 2022 года
future_dates = pd.date_range(start=forecast_start, end=forecast_end, freq='D')
future_period = pd.DataFrame({'Date': future_dates})
future_period = create_time_features(future_period)

X_train = train_df[FEATURES]
y_train = train_df[TARGET]
X_future = future_period[FEATURES]

# 4. Обучение модели LightGBM
# Инициализация модели (модель регрессии для прогнозирования выручки)
model = lgb.LGBMRegressor(random_state=42)

# Обучение
model.fit(X_train, y_train)

# 5. Получение прогноза
forecast_values = model.predict(X_future)

# Добавление прогнозов в датафрейм будущего периода
future_period['yhat'] = forecast_values
# LightGBM не предоставляет встроенных интервалов предсказания (нижний/верхний уровень), как Prophet.
# Если они вам критически необходимы, потребуется использовать более сложные методы (например, бутстрап или квантильную регрессию).

# 6. Вывод результата и сохранение
print(future_period[['Date', 'yhat']])

# Сохранение результата
# Переименовываем столбец 'Date' обратно в 'ds' для соответствия формату вывода Prophet, если нужно
results_df = future_period.rename(columns={'Date': 'ds'})
# Создаем фиктивные столбцы для yhat_lower и yhat_upper, чтобы сохранить структуру исходного файла
results_df['yhat_lower'] = np.nan
results_df['yhat_upper'] = np.nan

results_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv('E:\Саша\AIBY\Task 1 Forecast_LightGBM.csv', index=False)