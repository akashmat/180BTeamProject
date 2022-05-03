# SJSU CMPE 138 Spring 2022 TEAM9 

from flask import render_template, flash, request, Blueprint, session, url_for, redirect
from datetime import date
import random
import db_operations as dbOp

import logging
import logging.config


polling = Blueprint("polling", __name__, static_folder="static", template_folder="templates")

logging.basicConfig(filename="output.log",
                    filemode='a',
                    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


@polling.route("/createPoll", methods=['POST', 'GET'])
def createPoll():
    if request.method == "POST":
        team1 = request.form['team1']
        team2 = request.form['team2']
        duration = request.form['duration']
        poll_name = request.form['poll_name']
        creation_date = date.today()
        creator_name = session['admin']
        team1_vote = 0
        team2_vote = 0
        #poll_data['question'] = poll_name

        rand_id = random.randint(1, 1000)

        df_id = dbOp.read_sql_raw("SELECT poll_id from POLLS")

        #ensures that member_id will be unique
        check_random = 1
        while check_random == 1:
            for id in df_id['poll_id']:
                if rand_id == id:
                    rand_id = random.randint(1, 1000)
                    continue
            check_random = 0

        sql_op = f"{rand_id}, \'{creator_name}\', {duration}, \'{creation_date}\', \'{poll_name}\', {team1_vote}, {team2_vote}, \'{team1}\', \'{team2}\'"
        check_flag = dbOp.insert_sql("POLLS", sql_op)
        if check_flag:
            flash('Poll: Created', 'success')
            logging.info('Poll created')
        else:
            flash('Poll: Not Created', 'danger')
            logging.info('Poll not created')
        #opDB = "INSERT INTO " + str(team2) + " "

        #strpoll = session['poll_id']
        #print(strpoll[0])

    return render_template("homeAdmin.html")

poll_data = {
   'question' : 'Which team do you think will win?',
   'fields'   : ['team1', 'team2']
   
}

@polling.route("/poll", methods =['POST', 'GET'])
def countVote():
    if request.method == "POST":
        #array_pollid = df_poll['poll_id']
        strpoll = session['poll_id']
        strpoll2 = session['user']
        # print(strpoll[0])



        vote = request.form.get('field')
        
        if vote is not None:
           # out = open('data.txt', 'a')
           # out.write( vote + '\n' )
           # out.close()

           q = dbOp.read_sql_raw(f"SELECT * from POLLS where poll_id = {strpoll}")
           if vote == q['team_name1'].iloc[0]:
               u = dbOp.read_sql_raw(f"update polls set team1_vote = team1_vote + 1 where poll_id = {strpoll}")
           else:
               u = dbOp.read_sql_raw(f"update polls set team2_vote = team2_vote + 1 where poll_id = {strpoll}")

        q2 = dbOp.read_sql_raw(f"select * from POLLS where poll_id = {strpoll}")
        count1 = q2['team1_vote'].iloc[0]
        count2 = q2['team2_vote'].iloc[0]
        
        total = count1 + count2
        if total == 0:
            percentage1 = 0
            percentage2 = 0
        else:
            percentage1 = int((count1 / total) * 100)
            percentage2 = int((count2 / total) * 100)

        q3 = dbOp.read_sql_raw(f"select * from fan where username = \'{strpoll2}\'")
        print(q3['profile_id'])
        userID = q3['profile_id'].iloc[0]

        dis_comments = dbOp.read_sql_raw("select * from INTERACTS as I join POLLS as P on I.ip_id = P.poll_id")
        rand_id = random.randint(1, 1000)
        check_random = 1
        while check_random == 1:
            for id in dis_comments['interact_id']:
                if rand_id == id:
                    rand_id = random.randint(1, 1000)
                    continue
            check_random = 0

        #comments = request.form['button1']
        comments = request.form.get('comments')
        if comments is not None and not comments.isspace():
            if comments == '':
                insert_comments = 0
            else: 
                insert_comments = dbOp.insert_sql("INTERACTS", f"{strpoll}, {userID} , \'{rand_id}\', \'{comments}\'")
            if insert_comments == 0:
                flash('Comment Not Made: ', 'danger')
                logging.info('Comment not made')
            else:
                flash('Comment Made: ', 'success')
                logging.info('Comment made')


        display_comments = dbOp.read_sql_raw(f"select * from INTERACTS as I join POLLS as P on I.ip_id = P.poll_id where P.poll_id = {strpoll}")

        return render_template('results.html', dis_comments=dis_comments, display_comments=display_comments['comments'], total=total, percentage1=percentage1, percentage2=percentage2, data=poll_data)
    else:
        return render_template('results.html')