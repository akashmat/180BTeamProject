import hashlib
from flask import render_template, flash, request, Blueprint, session, url_for, redirect
import db_operations as dbOp

def success(request_data):
    pwd = hashlib.md5(request_data.get('password').encode()).hexdigest()
    username = request_data.get('username')
    email = request_data.get('email')
    query = f"INSERT INTO [dbo].[Fan] (username, email, hashed_password) VALUES ('{username}', '{email}', '{pwd}') ;"
    data = dbOp.exec_sql(query)
    return data

