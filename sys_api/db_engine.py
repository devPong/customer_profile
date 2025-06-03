from django.conf import settings
from django.db import connections
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd


def conn_fetchall(dataBase,q_txt):
    rawDatas = None
    with connections[dataBase].cursor() as cursor:
        cursor.execute(q_txt)
        rawDatas = cursor.fetchall()
    return rawDatas

def pd_conn(dataBase, q_txt):
    conn = connections[dataBase]
    df = pd.read_sql_query(q_txt, conn)
    return df.to_dict(orient='records')

def get_sqlalchemy_engine(db_key='default'):
    db = settings.DATABASES[db_key]
    password = quote_plus(db['PASSWORD']) 
    db_url = f"postgresql://{db['USER']}:{password}@{db['HOST']}:{db['PORT']}/{db['NAME']}"
    return create_engine(db_url)

