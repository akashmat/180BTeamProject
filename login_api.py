# SJSU CMPE 138 Spring 2022 TEAM9 

from flask import render_template, flash, request, Blueprint, session, url_for, redirect
import db_operations as dbOp


def success(email, pwd, type):
    if type == 'fan':
        query = f"SELECT f.profile_id as ID FROM [dbo].[Fan] as f WHERE f.email = '{email}' AND f.hashed_password = '{pwd}';"
    elif type == 'admin':
        query = f"SELECT a.username as ID FROM [dbo].[Administrator] as a WHERE a.email = '{email}' AND a.hashed_password = '{pwd}';"
    
    data = dbOp.exec_sql(query, True)
    print(data)

    if len(data) > 0:
        return data[0]['ID']
    else:
        return None
    