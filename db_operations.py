# SJSU CMPE 138 Spring 2022 TEAM9 

from sqlalchemy import create_engine
import pandas as pd
from pandas.io.sql import DatabaseError 
import pyodbc


# Windows Authentication
# Server = "DESKTOP-31O3JDL\SQLEXPRESS01"
Server = "DESKTOP-TIANPEN\SQLEXPRESS"
Database = "nfl"
Driver = "ODBC Driver 17 for SQL Server"
Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'
engine = create_engine(Database_Con)
con = engine.connect()

connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-TIANPEN\SQLEXPRESS;DATABASE=nfl;Trusted_Connection=yes;')

#select statement
def read_sql(r_select, r_from, r_where, r_groupby, r_having, r_order_by):
    if not r_select or not r_from:
        return pd.DataFrame()
    else:
        select_op = "SELECT" + " " + r_select
        from_op = "FROM" + " " + r_from 
        where_op = read_where(r_where)
        group_by_op = read_groub_by(r_groupby)
        r_having_op = read_having(r_having)
        r_order_by_op = read_order_by(r_order_by)

        operation = (select_op + " " + 
                    from_op + " " + 
                    where_op + " " + 
                    group_by_op + " " + 
                    r_having_op + " " + 
                    r_order_by_op)
        print(operation)

        try:
            return pd.read_sql_query(operation, con) #returns data frame
        except Exception as e:
            return pd.DataFrame()         

#select statement
def read_sql_raw(operation):
    print(operation)
    try:
        #c = con.execute(operation)
        #rows = c.fetchall()    # get all selected rows, as Barmar mentioned
        return pd.read_sql_query(operation, con) #returns data frame
        #pd.read_sql_query(operation, con) #returns data frame
    except Exception as e:
        return pd.DataFrame()    

#insert statement
def insert_sql(i_table, i_values):
    if not i_table or not i_values:
        return 0
    else:
        operation = f"INSERT INTO {i_table} VALUES({i_values})" 
        print(operation)
        try:
            con.execute(operation)
        except Exception as e:
            return 0    
        return 1

#update statement
def update_sql(u_table, u_set, u_condition):
    if not u_table or not u_set:
        return 0
    else:
        operation = ""
        if u_condition:
            operation = f"UPDATE {u_table} SET {u_set} WHERE {u_condition}" 
        else:
            operation = f"UPDATE {u_table} SET {u_set}"
        print(operation)
        try:
            con.execute(operation)
        except Exception as e:
            return 0    
        return 1

#delete statement
def delete_sql(d_table, d_condition):
    if not d_table:
        return  0
    else:
        operation = ""
        if d_condition:
            operation = f"DELETE FROM {d_table} WHERE {d_condition}" 
        else:
            operation = f"DELETE FROM {d_table}"
        print(operation)
        try:
            con.execute(operation)
        except Exception as e:
            return 0    
        return 1

def read_where(read_where):
    if not read_where:
        return ""
    else:
        return "WHERE" + " " + read_where

def read_groub_by(read_group_by):
    if not read_group_by:
        return ""
    else:
        return "GROUP BY" + " " + read_group_by

def read_having(read_having):
    if not read_having:
        return ""
    else:
        return "HAVING" + " " + read_having

def read_order_by(read_order_by):
    if not read_order_by:
        return ""
    else:
        return "ORDER BY" + " " + read_order_by

def exec_sql(query, force_json=False):
    cursor = connection.cursor()   
    print(query)
    try:
        cursor.execute(query)
        if not force_json:
            data = cursor.fetchall()
        else:
            data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    except Exception as e:
        print('Excep', e)
        cursor.close()
        return 0
    connection.commit()
    cursor.close()
    return data