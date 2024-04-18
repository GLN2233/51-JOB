# coding=gbk
import pandas as pd
from sqlalchemy import create_engine

# ��ȡ CSV �ļ�Ϊ DataFrame
new_data = pd.read_csv('newPython.csv')

# MySQL���ݿ�������Ϣ
db_username = 'root'
db_password = 'root'
db_host = 'localhost'
db_name = 'python'

# ���ݿ������ַ���
db_connection_str = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
engine = create_engine(db_connection_str)

# �� DataFrame ������д�����ݿ���±�
new_data.to_sql('newAnalyse', con=engine, if_exists='replace', index=False)