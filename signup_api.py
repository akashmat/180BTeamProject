# SJSU CMPE 138 Spring 2022 TEAM9 

import hashlib
from flask import render_template, flash, request, Blueprint, session, url_for, redirect
import db_operations as dbOp

def success(request_data):
    pwd = hashlib.md5(request_data.get('password').encode()).hexdigest()
    username = request_data.get('username')
    email = request_data.get('email')
    #query = f"INSERT INTO fan (username, email, hashed_password) VALUES ('{username}', '{email}', '{pwd}') ;"
    check_flag = 0
    # data = dbOp.read_sql_raw(f"INSERT INTO fan (username, email, hashed_password) VALUES (\'{username}\', \'{email}\', \'{pwd}\')") 
    check_flag = dbOp.insert_sql("fan (username, email, hashed_password)", f"'{username}', '{email}', '{pwd}'")

    #exec_sql(query, True)
    return check_flag
    #print(data)
    #return data

