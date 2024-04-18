# coding=gbk
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
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

def plot_pie_chart(data, column, title):
    # 绘制饼图
    counts = data[column].value_counts()
    threshold = 0.015
    mask = (counts / counts.sum()) < threshold
    other_count = counts[mask].sum()
    filtered_counts = counts[~mask]
    filtered_counts['其他'] = other_count

    plt.figure(figsize=(6, 6))
    plt.pie(filtered_counts, labels=filtered_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.show()

def generate_word_cloud(data):
    # 生成词云
    column_1 = data.iloc[:, 0]
    text = ' '.join(column_1.astype(str).values)

    wordcloud = WordCloud(font_path='msyh.ttc', width=800, height=400, background_color='white')
    wordcloud.generate(text)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

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
print(processed_data)

# 绘制饼图
plot_pie_chart(processed_data, '工作地区', '各城市的岗位数量分布')
plot_pie_chart(processed_data, '学历要求', '不同学历要求下的岗位数量分布')

# 生成词云
generate_word_cloud(data)