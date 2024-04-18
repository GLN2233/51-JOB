# coding=gbk
import pandas as pd
from sqlalchemy import create_engine

# 读取 CSV 文件为 DataFrame
new_data = pd.read_csv('newPython.csv')

# MySQL数据库连接信息
db_username = 'root'
db_password = 'root'
db_host = 'localhost'
db_name = 'python'

# 数据库连接字符串
db_connection_str = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
engine = create_engine(db_connection_str)

# 将 DataFrame 的数据写入数据库的新表
new_data.to_sql('newAnalyse', con=engine, if_exists='replace', index=False)