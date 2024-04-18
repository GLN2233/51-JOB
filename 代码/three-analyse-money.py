# coding=gbk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sqlalchemy import create_engine

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def load_data_from_mysql(username, password, host, db_name, query):
    # 从 MySQL 数据库中加载数据到 DataFrame
    db_connection_str = f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
    engine = create_engine(db_connection_str)
    data = pd.read_sql(query, engine)
    return data

def clean_data(data):
    # 清洗数据，去除空字段和重复行
    non_empty_rows = np.any(data != '', axis=1)
    cleaned_data = data[non_empty_rows].drop_duplicates()
    return cleaned_data

def process_work_areas(data, column):
    # 处理工作地区信息，提取地区的前两个字符
    data['工作地区'] = data[column].str[:2]
    return data
# MySQL数据库连接信息
db_username = 'root'
db_password = 'root'
db_host = 'localhost'
db_name = 'python'
sql_query = 'SELECT * FROM analyse'

# 加载数据
data = load_data_from_mysql(db_username, db_password, db_host, db_name, sql_query)
cleaned_data = clean_data(data)

# 处理工作地区信息
processed_data = process_work_areas(cleaned_data, '地点')
# print(processed_data)

def extract_first_number(salary):
    # 使用正则表达式匹配第一个数字（包括小数）
    first_number = re.search(r'\d+\.?\d*', str(salary))  # 将参数转换为字符串
    if first_number:
        return float(first_number.group())
    return 0  # 返回默认值0

# 提取每行“薪资”列中的第一个数字
processed_data['第一个数字'] = processed_data['薪资'].apply(extract_first_number)

def process_salary(num):
    if num < 4:
        return int(num * 13000)
    elif 4 <= num < 10:
        return int(num * 1300)
    elif 10 <= num < 100:
        return int((num * 13000) / 12)
    else:
        return int(num * 30)

# 根据条件逻辑处理“薪资”列中的第一个数字
processed_data['真实月薪'] = processed_data['第一个数字'].apply(process_salary)
print(processed_data)

def generate_boxplot(data, column, by_column, title):
    # 生成箱型图的函数
    top_categories = data[by_column].value_counts().head(8).index.tolist()
    filtered_data = data[data[by_column].isin(top_categories)]

    plt.figure(figsize=(10, 6))
    boxplot = filtered_data.boxplot(column=column, by=by_column, figsize=(12, 8))
    plt.title(title)
    plt.xlabel(by_column)
    plt.ylabel(column)
    plt.suptitle('')
    plt.show()


# 生成“工作地区”对应的箱型图
generate_boxplot(processed_data, '真实月薪', '工作地区', '各地区真实月薪箱型图')

# 生成“工作经验”对应的箱型图
generate_boxplot(processed_data, '真实月薪', '工作经验', '不同工作经验真实月薪箱型图')


average_salary = processed_data['真实月薪'].mean()
print(f"真实月薪列的平均数为: {average_salary}")

most_common_experience = processed_data['工作经验'].value_counts().idxmax()
print(f"工作经验列中出现次数最多的数据是: {most_common_experience}")

# # 选择需要保留的列
# columns_to_keep = ['关键词', '岗位名称', '真实月薪','工作地区','工作经验','学历要求']  # 替换为你希望保留的列名列表
#
# # 创建一个新的 DataFrame，仅包含需要保留的列
# selected_columns_data = processed_data[columns_to_keep]
#
# # 将新的 DataFrame 保存为 CSV 文件
# selected_columns_data.to_csv('newPython.csv', index=False)
