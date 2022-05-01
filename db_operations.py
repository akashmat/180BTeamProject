
from sqlalchemy import create_engine
import pandas as pd

# Server = "DESKTOP-31O3JDL\SQLEXPRESS01"
Server = "DESKTOP-BS4D8BR\SQLEXPRESS"

Database = "nfl"
Driver = "ODBC Driver 17 for SQL Server"
Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'

engine = create_engine(Database_Con)
con = engine.connect()

def read_sql(operation):
    return pd.read_sql_query(operation, con) #returns data fra

query = "select * from FAN"
query1 = "select email from MATCH join NOTIFIES on match_id=m_id join FAN on p_id =profile_id"
res = read_sql(query1)
print(res['email'].to_list())
