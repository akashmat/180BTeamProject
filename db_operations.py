from sqlalchemy import create_engine
import pandas as pd

# Windows Authentication

Server = "LAPTOP-EDCPNSRD\SQLEXPRESS"
Database = "nfl"
Driver = "ODBC Driver 17 for SQL Server"
Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Database_Con)
con = engine.connect()

def read_sql(operation, mode):
    if mode == 0: # read from db
        return pd.read_sql_query(operation, con) #returns data frame
    elif mode == 1: # write to db
        pd.read_sql_query(operation, con)
        return 1
    else: #nothing happens
        return 0
