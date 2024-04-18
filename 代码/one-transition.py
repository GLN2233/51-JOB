import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# df = pd.read_csv("python.csv",encoding='gbk')  # 读数据
# print(df)
# # 选择要保留的列
# columns_to_keep = ['关键词', '名称', 'sal', 'd', 'd1', 'd2']  # 将列名替换为要保留的列名列表
# # 从原始数据中选择特定列
# selected_data = df[columns_to_keep]
# # 将选择的列保存到新文件
# new_file_path = 'new_python.csv'
# selected_data.to_csv(new_file_path, index=False)

# 读取CSV文件
file_path = 'new_python.csv'
data = pd.read_csv(file_path)

# MySQL数据库连接信息
db_username = 'root'
db_password = 'root'
db_host = 'localhost'
db_name = 'python'

# 创建MySQL数据库连接
db_connection_str = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
engine = create_engine(db_connection_str)

# 新列名字典，用于映射原始列名到新的列名
column_mapping = {
    '名称': '岗位名称',
    'sal': '薪资',
    'd': '地点',
    'd1': '工作经验',
    'd2': '学历要求'
}

# 重命名列
data = data.rename(columns=column_mapping)

# 将数据保存到MySQL数据库中的新表格
new_table_name = 'analyse'
data.to_sql(new_table_name, engine, index=False, if_exists='replace')

# 关闭数据库连接（可选）
engine.dispose()






