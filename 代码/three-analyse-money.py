# coding=gbk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sqlalchemy import create_engine

# ����������ʾ
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def load_data_from_mysql(username, password, host, db_name, query):
    # �� MySQL ���ݿ��м������ݵ� DataFrame
    db_connection_str = f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
    engine = create_engine(db_connection_str)
    data = pd.read_sql(query, engine)
    return data

def clean_data(data):
    # ��ϴ���ݣ�ȥ�����ֶκ��ظ���
    non_empty_rows = np.any(data != '', axis=1)
    cleaned_data = data[non_empty_rows].drop_duplicates()
    return cleaned_data

def process_work_areas(data, column):
    # ������������Ϣ����ȡ������ǰ�����ַ�
    data['��������'] = data[column].str[:2]
    return data
# MySQL���ݿ�������Ϣ
db_username = 'root'
db_password = 'root'
db_host = 'localhost'
db_name = 'python'
sql_query = 'SELECT * FROM analyse'

# ��������
data = load_data_from_mysql(db_username, db_password, db_host, db_name, sql_query)
cleaned_data = clean_data(data)

# ������������Ϣ
processed_data = process_work_areas(cleaned_data, '�ص�')
# print(processed_data)

def extract_first_number(salary):
    # ʹ��������ʽƥ���һ�����֣�����С����
    first_number = re.search(r'\d+\.?\d*', str(salary))  # ������ת��Ϊ�ַ���
    if first_number:
        return float(first_number.group())
    return 0  # ����Ĭ��ֵ0

# ��ȡÿ�С�н�ʡ����еĵ�һ������
processed_data['��һ������'] = processed_data['н��'].apply(extract_first_number)

def process_salary(num):
    if num < 4:
        return int(num * 13000)
    elif 4 <= num < 10:
        return int(num * 1300)
    elif 10 <= num < 100:
        return int((num * 13000) / 12)
    else:
        return int(num * 30)

# ���������߼�����н�ʡ����еĵ�һ������
processed_data['��ʵ��н'] = processed_data['��һ������'].apply(process_salary)
print(processed_data)

def generate_boxplot(data, column, by_column, title):
    # ��������ͼ�ĺ���
    top_categories = data[by_column].value_counts().head(8).index.tolist()
    filtered_data = data[data[by_column].isin(top_categories)]

    plt.figure(figsize=(10, 6))
    boxplot = filtered_data.boxplot(column=column, by=by_column, figsize=(12, 8))
    plt.title(title)
    plt.xlabel(by_column)
    plt.ylabel(column)
    plt.suptitle('')
    plt.show()


# ���ɡ�������������Ӧ������ͼ
generate_boxplot(processed_data, '��ʵ��н', '��������', '��������ʵ��н����ͼ')

# ���ɡ��������顱��Ӧ������ͼ
generate_boxplot(processed_data, '��ʵ��н', '��������', '��ͬ����������ʵ��н����ͼ')


average_salary = processed_data['��ʵ��н'].mean()
print(f"��ʵ��н�е�ƽ����Ϊ: {average_salary}")

most_common_experience = processed_data['��������'].value_counts().idxmax()
print(f"�����������г��ִ�������������: {most_common_experience}")

# # ѡ����Ҫ��������
# columns_to_keep = ['�ؼ���', '��λ����', '��ʵ��н','��������','��������','ѧ��Ҫ��']  # �滻Ϊ��ϣ�������������б�
#
# # ����һ���µ� DataFrame����������Ҫ��������
# selected_columns_data = processed_data[columns_to_keep]
#
# # ���µ� DataFrame ����Ϊ CSV �ļ�
# selected_columns_data.to_csv('newPython.csv', index=False)
