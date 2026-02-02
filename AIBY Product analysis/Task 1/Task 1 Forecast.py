import pandas as pd
from prophet import Prophet

# 1. Загрузка данных
df = pd.read_csv('E:\Саша\AIBY\Task 1 Dataset.csv')

# Преобразуем столбцы в формат Prophet
df['ds'] = pd.to_datetime(df['Date'])
df['y'] = df['Revenue ($)']

# 2. Фильтрация тренировочного периода
train = df[(df['ds'] >= '2022-03-01') & (df['ds'] <= '2022-09-30')]

# 3. Обучение модели
model = Prophet(weekly_seasonality=True)
model.fit(train)

# 4. Создание датафрейма для прогноза
future = model.make_future_dataframe(periods=31,freq='D')
future_period = future[(future['ds'] >= '2022-10-01') & (future['ds'] <= '2022-10-31')]

# 5. Получение прогноза
forecast = model.predict(future_period)

# 6. Вывод результата
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
forecast.to_csv('E:\Саша\AIBY\Task 1 Forecast.csv')

