from flask import render_template, flash, request, Blueprint, session, url_for, redirect
from datetime import date
import random
import db_operations as dbOp


polling = Blueprint("polling", __name__, static_folder="static", template_folder="templates")


@polling.route("/createPoll", methods=['POST', 'GET'])
def createPoll():
    if request.method == "POST":
        team1 = request.form['team1']
        team2 = request.form['team2']
        duration = request.form['duration']
        poll_name = request.form['poll_name']
        creation_date = date.today()
        creator_name = session['user']
        team1_vote = 0
        team2_vote = 0
        poll_data['question'] = poll_name

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

        sql_op = f"{rand_id}, \'{creator_name}\', {duration}, \'{creation_date}\', \'{poll_name}\', \'{team1_vote}\', {team2_vote}, \'{team1}\', \'{team2}\'"
        check_flag = dbOp.insert_sql("POLLS", sql_op)
        if check_flag:
            flash('Poll: Created', 'success')
        else:
            flash('Poll: Not Created', 'danger')
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

        vote = request.form.get('field')
        
        if vote is not None:
            out = open('data.txt', 'a')
            out.write( vote + '\n' )
            out.close()

        votes = {}
        for f in poll_data['fields']:
            votes[f] = 0
            total = 0
            count1 = 0
            count2 = 0
            
        f = open('data.txt', 'r')
        for line in f:
            vote = line.rstrip("\n")
            votes[vote] += 1
            total += 1
            if vote == 'team1':
                count1 += 1
            else:
                count2 += 1

        percentage1 = (count1 / total) * 100
        percentage2 = (count2 / total) * 100

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
        if comments is not None:
            insert_comments = dbOp.insert_sql("INTERACTS", f"78, 56, \'{rand_id}\', \'{comments}\'")
            if insert_comments == 0:
                flash('Comment Not Made: ', 'danger')
            else:
                flash('Comment Made: ', 'success')

        display_comments = dbOp.read_sql_raw("select * from INTERACTS as I join POLLS as P on I.ip_id = P.poll_id")
       # display_comments2 = dis_comments[['comments', 'creator_name']]


        #dbOp.update_sql('polls', "poll_percentage = \'{vote}\'", "poll_name = \'{data.question}\'")
            #10%-90%
            #display_comments2=display_comments2.to_dict(),
        return render_template('results.html', dis_comments=dis_comments, display_comments=display_comments['comments'], total=total, percentage1=percentage1, percentage2=percentage2, data=poll_data, votes=votes)
    else:
        return render_template('results.html')