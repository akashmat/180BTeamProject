#from tabnanny import check
from flask import render_template, flash, request, Blueprint, session, url_for, redirect
#from forms import RegistrationForm, LoginForm
from datetime import date
import db_operations as dbOp
import random

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


# Database operations by Administer
@admin.route("/homeAdmin")
def homeAdmin():
    if not ('user' in session and session['user'] == 'user1'):
        return redirect(url_for('login'))
    else:
        return render_template('homeAdmin.html')


@admin.route("/readDB", methods=['POST', 'GET'])
def readDB():
    if request.method == "POST":
        name = request.form['read']

        df = dbOp.read_sql("*", str(name), "", "", "", "")
        return render_template("homeAdmin.html", tables=[df.to_html(classes='data', header="true")])
    else:
        return render_template("homeAdmin.html")


@admin.route("/add_score", methods=['POST', 'GET'])
def add_score():
    if request.method == "POST":
        name = request.form['record_name']
        year = request.form['record_year']
        new_player = request.form.get('new_player')
        new_coach = request.form.get('new_coach')
        new_team = request.form.get('new_team')

        df_p = dbOp.read_sql_raw("SELECT member_id" + " " 
                            "FROM TEAM_MEMBER as T join PLAYER_SCORE as P on T.member_id = P.pscore_id" + " "
                            "WHERE fname = \'" + name + "\'")

        df_c = dbOp.read_sql_raw("SELECT member_id" + " " 
                            "FROM TEAM_MEMBER as T join COACH_SCORE as C on T.member_id = C.cscore_id" + " "
                            "WHERE fname = \'" + name + "\'")

        if df_p.empty:
            p_id = 0
        else:
            p_id = df_p['member_id'].iloc[0]

        if df_c.empty:
            c_id = 0
        else:
            c_id = df_c['member_id'].iloc[0]

        if new_player:
            check_flag = dbOp.insert_sql("PLAYER_SCORE (p_year, pscore_id)", f"{year}, {p_id}")
        elif new_coach:
            check_flag = dbOp.insert_sql("COACH_SCORE (c_year, cscore_id)", f"{year}, {c_id}")
        elif new_team:
            check_flag = dbOp.insert_sql("TEAM_SCORE (year, t_name)", f"{year}, \'{name}\'")
        else:
            check_flag = 0

        if check_flag:
            flash('Score for {name}, {year} added', 'success')
        else:
            flash('Score for {name}, {year} not added', 'danger')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")
    

@admin.route("/update_pscore", methods=['POST', 'GET'])
def update_pscore():
    if request.method == "POST":
        name = request.form['p_name']
        year = request.form['p_year']
        yards = request.form['yards']
        touchdowns = request.form['touchdowns']
        total_sacks = request.form['total_sacks']
        total_fumbles = request.form['total_fumbles']
        number_games_played = request.form['number_games_played']

        df_id = dbOp.read_sql_raw("SELECT member_id" + " " 
                            "FROM TEAM_MEMBER as T join PLAYER_SCORE as P on T.member_id = P.pscore_id" + " "
                            "WHERE fname = \'" + name + "\'" + " " + "and p_year = " + year)

        if df_id.empty:
            member_id = 0
        else:
            member_id = str(df_id['member_id'].iloc[0])

        error_list = ""
        if str(yards) and member_id:
            check_flag = dbOp.update_sql("PLAYER_SCORE", f"yards = {yards}", f"pscore_id = {member_id} and p_year = {year}" )
            if check_flag == 0:
                error_list += "[yards] "

        if str(touchdowns) and member_id:
            check_flag = dbOp.update_sql("PLAYER_SCORE", f"touchdowns = {touchdowns}", f"pscore_id = {member_id} and p_year = {year}" )
            if check_flag == 0:
                error_list += "[touchdowns] "

        if str(total_sacks) and member_id:
            check_flag = dbOp.update_sql("PLAYER_SCORE", f"total_sacks = {total_sacks}", f"pscore_id = {member_id} and p_year = {year}" )
            if check_flag == 0:
                error_list += "[total sacks] "

        if str(total_fumbles) and member_id:
            check_flag = dbOp.update_sql("PLAYER_SCORE", f"total_fumbles = {total_fumbles}", f"pscore_id = {member_id} and p_year = {year}" )
            if check_flag == 0:    
                error_list += "[total fumbles] "

        if str(number_games_played) and member_id:
            check_flag = dbOp.update_sql("PLAYER_SCORE", f"number_games_played = {number_games_played}", f"pscore_id = {member_id} and p_year = {year}" )
            if check_flag == 0:    
                error_list += "[number of games played] "

        if member_id == 0:
            flash('Player Information: Incorrect [name]!', 'danger')
        elif not error_list:
            flash('Player Information: Updated!', 'success')
        else:
            flash(f'Player Information: {error_list} have not been updated!', 'danger')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

@admin.route("/update_cscore", methods=['POST', 'GET'])
def update_cscore():
    if request.method == "POST":
        name = request.form['c_name']
        year = request.form['c_year']
        years_coached = request.form['years_coached']
        total_games_coached = request.form['total_games_coached']
        sb_champ_won = request.form['sb_champ_won']
        league_champ_won = request.form['league_champ_won']
        conference_champ_won = request.form['conference_champ_won']
        division_champ_won = request.form['division_champ_won']

        df_id = dbOp.read_sql_raw("SELECT member_id" + " " 
                            "FROM TEAM_MEMBER as T join COACH_SCORE as C on T.member_id = C.cscore_id" + " "
                            "WHERE fname = \'" + name + "\'" + " " + "and c_year = " + year)

        if df_id.empty:
            member_id = 0
        else:
            member_id = str(df_id['member_id'].iloc[0])

        error_list = ""
        if str(years_coached) and member_id:
            check_flag = dbOp.update_sql("COACH_SCORE", f"years_coached = {years_coached}", f"cscore_id = {member_id} and c_year = {year}" )
            if check_flag == 0:
                error_list += "[Years Coached] "

        if str(total_games_coached) and member_id:
            check_flag = dbOp.update_sql("COACH_SCORE", f"total_games_coached = {total_games_coached}", f"cscore_id = {member_id} and c_year = {year}" )
            if check_flag == 0:
                error_list += "[Total Games Coached] "

        if str(sb_champ_won) and member_id:
            check_flag = dbOp.update_sql("COACH_SCORE", f"sb_champ_won = {sb_champ_won}", f"cscore_id = {member_id} and c_year = {year}" )
            if check_flag == 0:
                error_list += "[Super Bowl Championships Won] "

        if str(league_champ_won) and member_id:
            check_flag = dbOp.update_sql("COACH_SCORE", f"league_champ_won = {league_champ_won}", f"cscore_id = {member_id} and c_year = {year}" )
            if check_flag == 0:    
                error_list += "[League Championships Won] "

        if str(conference_champ_won) and member_id:
            check_flag = dbOp.update_sql("COACH_SCORE", f"conference_champ_won = {conference_champ_won}", f"cscore_id = {member_id} and c_year = {year}" )
            if check_flag == 0:    
                error_list += "[Conference Championships Won] "

        if str(division_champ_won) and member_id:
            check_flag = dbOp.update_sql("COACH_SCORE", f"division_champ_won = {division_champ_won}", f"cscore_id = {member_id} and c_year = {year}" )
            if check_flag == 0:    
                error_list += "[Division Championships Won] "

        if member_id == 0:
            flash('Coach Information: Incorrect [year] or [name]!', 'danger')
        elif not error_list:
            flash('Coach Information: Updated!', 'success')
        else:
            flash(f'Coach Information: {error_list} have not been updated!', 'danger')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

@admin.route("/update_tscore", methods=['POST', 'GET'])
def update_tscore():
    if request.method == "POST":
        year = request.form['year']
        name = request.form['t_name']
        total_field_goals = request.form['total_field_goals']
        total_touchdowns = request.form['total_touchdowns']
        total_passing_yards = request.form['total_passing_yards']
        avg_time_possession = request.form['avg_time_possession']
        total_rushing_yards = request.form['total_rushing_yards']
        total_offensive_yards = request.form['total_offensive_yards']

        id = dbOp.read_sql_raw("SELECT t_name" + " " 
                            "FROM TEAM_SCORE" + " "
                            "WHERE t_name = \'" + name + "\'" + " " + "and year = " + year)

        if id.empty:
            member_id = 0
        else:
            member_id = str(id['t_name'].iloc[0])

        error_list = ""
        if str(total_field_goals) and member_id:
            check_flag = dbOp.update_sql("TEAM_SCORE", f"total_field_goals = {total_field_goals}", f"t_name = \'{name}\' and year = {year}" )
            if check_flag == 0:
                error_list += "[Total Field Goals]] "

        if str(total_touchdowns) and member_id:
            check_flag = dbOp.update_sql("TEAM_SCORE", f"total_touchdowns = {total_touchdowns}", f"t_name = \'{name}\' and year = {year}" )
            if check_flag == 0:
                error_list += "[Total Touchdowns] "

        if str(total_passing_yards) and member_id:
            check_flag = dbOp.update_sql("TEAM_SCORE", f"total_passing_yards = {total_passing_yards}", f"t_name = \'{name}\' and year = {year}" )
            if check_flag == 0:
                error_list += "[Total Passing Yards] "

        if str(avg_time_possession) and member_id:
            check_flag = dbOp.update_sql("TEAM_SCORE", f"avg_time_possession = {avg_time_possession}", f"t_name = \'{name}\' and year = {year}" )
            if check_flag == 0:    
                error_list += "[Average Time Possession] "

        if str(total_rushing_yards) and member_id:
            check_flag = dbOp.update_sql("TEAM_SCORE", f"total_rushing_yards = {total_rushing_yards}", f"t_name = \'{name}\' and year = {year}" )
            if check_flag == 0:    
                error_list += "[Total Rushing Yards] "

        if str(total_offensive_yards) and member_id:
            check_flag = dbOp.update_sql("TEAM_SCORE", f"total_offensive_yards = {total_offensive_yards}", f"t_name = \'{name}\' and year = {year}" )
            if check_flag == 0:    
                error_list += "[Total Offensive Yards] "

        if member_id == 0:
            flash('Team Information: Incorrect [year] or [name]!', 'danger')
        elif not error_list:
            flash('Team Information: Updated!', 'success')
        else:
            flash(f'Team Information: {error_list} have not been updated!', 'danger')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

@admin.route("/insert_player", methods=['POST', 'GET'])
def insert_player():
    if request.method == "POST":
        fname = request.form['fname']
        minit = request.form['minit']
        lname = request.form['lname']
        te_name = request.form['te_name']
        check_player = request.form.get('record_player')
        check_coach = request.form.get('record_coach')

        rand_id = random.randint(1, 1000)

        df_id = dbOp.read_sql_raw("SELECT member_id from TEAM_MEMBER")
        #df_team = dbOp.read_sql_raw("SELECT team_name from TEAM")

        #print(check_coach)
        #print(check_player)

        #ensures that member_id will be unique
        check_random = 1
        while check_random == 1:
            for id in df_id['member_id']:
                if rand_id == id:
                    rand_id = random.randint(1, 1000)
                    continue
            check_random = 0

        #checks if first name and last name are absence 
        name_flag = 1
        if not fname or not lname:
            name_flag = 0

        #checks for valid team name in DB
        #team_flag = 0
        #for names in df_team['team_name']:
            #if te_name == names:
                #team_flag = 1
                #break

        check_flag = 0
        if name_flag == 1: #and team_flag == 1:
            if not minit and not te_name:
                check_flag = dbOp.insert_sql("TEAM_MEMBER", f"{rand_id}, \'{fname}\', null, \'{lname}\', null")
            elif not minit and te_name:
                check_flag = dbOp.insert_sql("TEAM_MEMBER", f"{rand_id}, \'{fname}\', null, \'{lname}\', \'{te_name}\'")
                if check_flag:
                    dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster + 1 WHERE team_name = \'{te_name}\'")
            elif minit and not te_name:
                check_flag = dbOp.insert_sql("TEAM_MEMBER", f"{rand_id}, \'{fname}\', \'{minit}\', \'{lname}\', null")
            else:
                check_flag = dbOp.insert_sql("TEAM_MEMBER", f"{rand_id}, \'{fname}\', \'{minit}\', \'{lname}\', \'{te_name}\'")
                if check_flag:
                    dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster + 1 WHERE team_name = \'{te_name}\'")
            
            if check_player and not check_coach:
                inserted_flag = dbOp.insert_sql("PLAYER", rand_id)
            elif not check_player and check_coach:
                inserted_flag = dbOp.insert_sql("COACH", rand_id)
            else:
                inserted_flag = 0

        if name_flag == 0: #or team_flag == 0:
            flash('Drafted Information: Draft [first name] or [last name] missing!', 'danger')
        elif not inserted_flag or not check_flag: #or not team_flag:
            flash('Drafted Information: Draft Invalid - Please Try Again!', 'danger')
        else:
            flash(f'Drafted Information: Draft {fname}, {lname} added!', 'success')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

@admin.route("/add_player", methods=['POST', 'GET'])
def add_player():
    if request.method == "POST":
        update_pteam = request.form['update_pteam']
        new_player = request.form['new_player']

        team_flag = 0
        player_flag = 0
        
        df_items = dbOp.read_sql_raw("select * from TEAM_MEMBER as T join PLAYER as P on T.member_id = P.player_id")

        for item in df_items['fname']:
            if item == new_player:
                player_flag = 1

        df_items = dbOp.read_sql_raw("select * from TEAM")

        previous_team = ''
        for item in df_items['team_name']:
            if item == update_pteam:
                team_flag = 1

        check_flag = 0
        if update_pteam and new_player and team_flag and player_flag:
            df_items = dbOp.read_sql_raw(f"SELECT te_name from TEAM_MEMBER WHERE fname = \'{new_player}\'")
            check_flag = dbOp.update_sql("TEAM_MEMBER", f"te_name = \'{update_pteam}\'", f"fname = \'{new_player}\'")
        
        if check_flag:
            previous_team = df_items['te_name'].iloc[0]
            if previous_team:
                dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster - 1 WHERE team_name = \'{previous_team}\'")
            dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster + 1 WHERE team_name = \'{update_pteam}\'")

        if check_flag: #or team_flag == 0:
            flash(f'Player [{new_player}] was added to team [{update_pteam}]!', 'success')
        else:
            flash(f'Player [{new_player}] cannot be added to team [{update_pteam}]!', 'danger')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")    

@admin.route("/add_coach", methods=['POST', 'GET'])
def add_coach():
    if request.method == "POST":
        update_cteam = request.form['update_cteam']
        new_coach = request.form['new_coach']

        team_flag = 0
        coach_flag = 0
        
        df_items = dbOp.read_sql_raw("select * from TEAM_MEMBER as T join COACH as C on T.member_id = C.coach_id")
        for item in df_items['fname']:
            if item == new_coach:
                coach_flag = 1

        df_items = dbOp.read_sql_raw("select * from TEAM")
        for item in df_items['team_name']:
            if item == update_cteam:
                team_flag = 1

        check_flag = 0
        if update_cteam and new_coach and coach_flag and team_flag:
            df_items = dbOp.read_sql_raw(f"SELECT te_name from TEAM_MEMBER WHERE fname = \'{new_coach}\'")
            check_flag = dbOp.update_sql("TEAM_MEMBER", f"te_name = \'{update_cteam}\'", f"fname = \'{new_coach}\'")
        
        if check_flag:
            previous_team = df_items['te_name'].iloc[0]
            if previous_team:
                dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster - 1 WHERE team_name = \'{previous_team}\'")
            dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster + 1 WHERE team_name = \'{update_cteam}\'")

        if check_flag: #or team_flag == 0:
            flash(f'Coach [{new_coach}] was added to team [{update_cteam}]!', 'success')
        else:
            flash(f'Coach [{new_coach}] cannot be added to team [{update_cteam}]!', 'danger')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")    

@admin.route("/remove_player", methods=['POST', 'GET'])
def remove_player():
    if request.method == "POST":
        update_pteam = request.form['update_pteam']
        new_player = request.form['new_player']

        team_flag = 0
        player_flag = 0
        
        df_items = dbOp.read_sql_raw("select * from TEAM_MEMBER as T join PLAYER as P on T.member_id = P.player_id")

        for item in df_items['fname']:
            if item == new_player:
                player_flag = 1

        df_items = dbOp.read_sql_raw("select * from TEAM")

        for item in df_items['team_name']:
            if item == update_pteam:
                team_flag = 1

        check_flag = 0
        if update_pteam and new_player and player_flag and team_flag:
            check_flag = dbOp.delete_sql("TEAM_MEMBER", f"fname = \'{new_player}\'")
        
        if check_flag:
            dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster - 1 WHERE team_name = \'{update_pteam}\'")

        if check_flag: #or team_flag == 0:
            flash(f'Player [{new_player}] was removed to team [{update_pteam}]!', 'success')
        else:
            flash(f'Player [{new_player}]  was not removed to team [{update_pteam}]!', 'danger')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")   

@admin.route("/remove_coach", methods=['POST', 'GET'])
def remove_coach():
    if request.method == "POST":
        update_cteam = request.form['update_cteam']
        new_coach = request.form['new_coach']

        team_flag = 0
        coach_flag = 0
        
        df_items = dbOp.read_sql_raw("select * from TEAM_MEMBER as T join COACH as C on T.member_id = C.coach_id")

        for item in df_items['fname']:
            if item == new_coach:
                coach_flag = 1

        df_items = dbOp.read_sql_raw("select * from TEAM")

        for item in df_items['team_name']:
            if item == update_cteam:
                team_flag = 1

        check_flag = 0
        if update_cteam and new_coach and coach_flag and team_flag:
            check_flag = dbOp.delete_sql("TEAM_MEMBER", f"fname = \'{new_coach}\'")
        
        if check_flag:
            dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster - 1 WHERE team_name = \'{update_cteam}\'")

        if check_flag: #or team_flag == 0:
            flash(f'Coach [{new_coach}] was removed to team [{update_cteam}]!', 'success')
        else:
            flash(f'Coach [{new_coach}]  was not removed to team [{update_cteam}]!', 'danger')
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")    

#Match
@admin.route("/add_match", methods=['POST', 'GET'])
def add_match():
    if request.method == "POST":
        t1 = request.form['Mte_name1']
        t2 = request.form['Mte_name2']
        date = request.form['date']
        print(date)

        rand_id = random.randint(1, 1000)

        df_id = dbOp.read_sql_raw("SELECT match_id from MATCH")
        #df_team = dbOp.read_sql_raw("SELECT team_name from TEAM")

        #ensures that member_id will be unique
        check_random = 1
        while check_random == 1:
            for id in df_id['match_id']:
                if rand_id == id:
                    rand_id = random.randint(1, 1000)
                    continue
            check_random = 0


        if t1 and t2 and date:
            check_flag = dbOp.insert_sql("MATCH", f"{rand_id}, \'{t1}\', \'{t2}\', \'{date}\', null, null, null, null")
        else:
            check_flag = 0

        if check_flag: #or team_flag == 0:
            flash(f'Match between [{t1}] and [{t2}] added for [{date}]!', 'success')
        else:
            flash(f'Match between [{t1}] and [{t2}] not added for [{date}]!', 'danger')

        return render_template("homeAdmin.html") 
    else:    
        return render_template("homeAdmin.html") 