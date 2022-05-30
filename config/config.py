import yaml
import os

with open(r"C:\Users\Mi\PyCharmProjects\vannya_beck\config\config.yaml", 'r', encoding='utf-8') as f:
    conf = yaml.safe_load(f)
    conn_string = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(**conf)
