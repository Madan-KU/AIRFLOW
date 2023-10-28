import time
from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
import pandas as pd

#Declare Dag
@dag(schedule_interval="0 10 * * *", start_date=datetime(2022,2,15), catchup=False, tags=['load_sql_server'])
#Define Dag Function
def extract_and_load():
    #Define tasks
    @task()
    def sql_extract():
        try:
            hook=MsSqlHook(mssql_conn_id="sqlserver")
            sql="""
                SELECT * from 
                """
            df=hook.get_pandas_df(sql)
            print(df)
            tbl_dict=df.to_dict('dict')
            return tbl_dict
        except Exception as e:
            print("Data Extract error: " + str(e))

            