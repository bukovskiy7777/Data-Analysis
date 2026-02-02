import numpy as np
import pandas as pd

# 1. Загрузка данных
df = pd.read_csv('E:\Саша\AIBY\Task 3 Dataset.csv')

# 2. Из сводной таблицы делаем равернутую таблицу по строкам
data = pd.melt(df, id_vars=['Active monthly subscribers amount', 'Date', 'Trial'], var_name='Month', value_name='Subscribers')

# 3. Расчет ретеншена для каждого месяца
data['Retention'] = round(data['Subscribers'] / data['Trial'], 4)

# 4. Удаляем из таблицы NaN значения по полю Subscribers
data = data.dropna(subset=['Subscribers']).reset_index()

data.to_csv('E:\Саша\AIBY\Task 3 unpivot data.csv')
# print(data)

# 5. Группируем таблицу по номеру месяца (Month), суммируя начальное (Trial) и конечное (Subscribers) кол-во подписчиков
#    также расчитываем средний Retention и кол-во строк для каждого Month
dataset = data.groupby('Month').agg({
                    'Trial':'sum',
                    'Subscribers':'sum',
                    'Retention':'mean',
                    'Date':'count',
                    'index':'min'}).sort_values(by=['index'], ascending=True)
dataset['RetentionWeighted'] = round(dataset['Subscribers'] / dataset['Trial'], 4)

dataset = dataset.drop(columns=['index']).reset_index()
dataset['Retention'] = round(dataset['Retention'], 4)

# 6. Добавляем номер месяца (Month number), доход от подписки (Subs Price), Apple charges (Charges)
dataset['Month number'] = dataset['Month'].str.split(' ').str[1].astype(int)
dataset['Subs Price'] = 9.99
dataset['Charges'] = np.where(dataset['Month number'] <= 12, 0.30, 0.15)
dataset['Net Price'] = round(dataset['Subs Price'] * (1 - dataset['Charges']), 2)

# 6. Расчет LTV для каждого месяца и LTV12, LTV24
dataset['LTV'] = round(dataset['RetentionWeighted'] * dataset['Net Price'], 2)

dataset.to_csv('E:\Саша\AIBY\Task 3 result data.csv')
# print(dataset)

LTV12 = round(dataset[dataset['Month number'] <= 12]['LTV'].sum(), 2)
LTV24 = round(dataset[dataset['Month number'] <= 24]['LTV'].sum(), 2)

print(LTV12)
print(LTV24)


