# SJSU CMPE 138 Spring 2022 TEAM9 

from flask import render_template, flash, request, Blueprint, session, url_for, redirect

import db_operations as dbOp

def update_success(username, followteam, favteam, firstname, lastname, id):
    query = f"UPDATE [dbo].[Fan] SET username = '{username}', fa_team = '{favteam}', fo_team = '{followteam}', firstname = '{firstname}', lastname = '{lastname}' WHERE profile_id = {id};"
    # data = dbOp.exec_sql(query)
    data = dbOp.update_sql("FAN", f"username = '{username}' , fa_team = '{favteam}' , fo_team = '{followteam}', firstname = '{firstname}', lastname = '{lastname}'",  f"profile_id = {id}")
    return data


def getdata(id):
    data = dbOp.read_sql("*", "[dbo].[Fan]", "", "", "", "")
    print(data)
    return data

def getteams():
    query = f"SELECT [team_name] FROM [dbo].[TEAM]"
    data = dbOp.exec_sql(query)
    print(data)
    return data

# def search(playername):
#     query = f"SELECT CONCAT(firstname, ' ', lastname) as Name FROM [dbo].[Team_Member] t WHERE CONCAT(firstname, ' ', lastname) like '{playername}'; "
#     data = dbOp.exec_sql(query)
#     if len(data) > 0:
#         return data
#     else:
#         return None



