from sqlalchemy import create_engine
import pandas as pd

Server = "DESKTOP-31O3JDL\SQLEXPRESS01"
Database = "nfl"
Driver = "ODBC Driver 17 for SQL Server"
Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Database_Con)
con = engine.connect()

def read_sql(operation):
    return pd.read_sql_query(operation, con) #returns data fram
