# SJSU CMPE 138 Spring 2022 TEAM9 

import logging
import logging.config

from tkinter import ttk
from flask import render_template, flash, request, Blueprint, session, url_for, redirect
from datetime import date
import db_operations as dbOp
import random
import pandas as pd

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

logging.basicConfig(filename="output.log",
                    filemode='a',
                    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

################################################ --- Database operations by Administer ---- ############################################################################

# Database operations by Administer
@admin.route("/homeAdmin")
def homeAdmin(USERID):
    # if not ('user' in session and session['user'] == 'user1'):
    #     return redirect(url_for('login'))
    # else:
    return render_template('homeAdmin.html', user = USERID)


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
        lr_name = request.form['lr_name']
        mr_name = request.form['mr_name']
        new_player = request.form.get('new_player')
        new_coach = request.form.get('new_coach')
        new_team = request.form.get('new_team')
        one = request.form.get("add")
        two = request.form.get("remove")

        if mr_name: #check if team/members exists
            df_p = dbOp.read_sql_raw("SELECT member_id" + " " 
                                "FROM TEAM_MEMBER as T join PLAYER as P on T.member_id = P.player_id" + " "
                                "WHERE fname = \'" + name + "\'" + " and " 
                                + "minit = \'" + mr_name + "\'" + " and "
                                + "lname = \'" + lr_name + "\'")

            df_c = dbOp.read_sql_raw("SELECT member_id" + " " 
                                "FROM TEAM_MEMBER as T join COACH as C on T.member_id = C.coach_id" + " "
                                "WHERE fname = \'" + name + "\'" + " and " 
                                + "minit = \'" + mr_name + "\'" + " and "
                                + "lname = \'" + lr_name + "\'")
        else:
            df_p = dbOp.read_sql_raw("SELECT member_id" + " " 
                                "FROM TEAM_MEMBER as T join PLAYER as P on T.member_id = P.player_id" + " "
                                "WHERE fname = \'" + name + "\'" + " and "
                                + "minit is null" + " and "
                                + "lname = \'" + lr_name + "\'")  

            df_c = dbOp.read_sql_raw("SELECT member_id" + " " 
                                "FROM TEAM_MEMBER as T join COACH as C on T.member_id = C.coach_id" + " "
                                "WHERE fname = \'" + name + "\'" + " and "
                                + "minit is null" + " and "
                                + "lname = \'" + lr_name + "\'")  

        df_t = dbOp.read_sql_raw(f"SELECT t_name FROM TEAM_SCORE WHERE t_name = \'{name}\' and year = {year}")

        if df_p.empty:
            p_id = 0
        else:
            p_id = df_p['member_id'].iloc[0]

        if df_c.empty:
            c_id = 0
        else:
            c_id = df_c['member_id'].iloc[0]

        check_flag = 0
        if one is not None:
            if new_player is not None and p_id:
                check_flag = dbOp.insert_sql("PLAYER_SCORE (p_year, pscore_id)", f"{year}, {p_id}")
            elif new_coach is not None and c_id:
                check_flag = dbOp.insert_sql("COACH_SCORE (c_year, cscore_id)", f"{year}, {c_id}")
            elif new_team is not None and df_t.empty:
                check_flag = dbOp.insert_sql("TEAM_SCORE (year, t_name)", f"{year}, \'{name}\'")
            else:
                check_flag = 0
        elif two is not None:
            if p_id:
                check_flag = dbOp.delete_sql("PLAYER_SCORE", f"pscore_id = {p_id} and p_year = {year}")
            elif c_id:
                check_flag = dbOp.delete_sql("COACH_SCORE", f"cscore_id = {c_id} and c_year = {year}")
            elif not df_t.empty:
                check_flag = dbOp.delete_sql("TEAM_SCORE", f"t_name = \'{name}\' and year = {year}")
            else:
                check_flag = 0            

        if check_flag and one is not None:
            flash(f'Score for {name}, {year} added', 'success')
            logging.info(f'%s, %s score for {name}, {year} added', name, year)
        elif check_flag and two is not None:
            flash(f'Score for {name}, {year} removed', 'success')
            logging.info(f'%s, %s score for {name}, {year} removed', name, year)
        elif not check_flag and one is not None:
            flash(f'Score for {name}, {year} not added', 'danger')
            logging.info(f'%s, %s score for {name}, {year} not added', name, year)
        elif not check_flag and two is not None:
            flash(f'Score for {name}, {year} not removed', 'danger')
            logging.info(f'%s, %s score for {name}, {year} not removed', name, year)
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

@admin.route("/update_pscore", methods=['POST', 'GET'])
def update_pscore():
    if request.method == "POST":
        name = request.form['p_name']
        lp_name = request.form['lp_name']
        mp_name = request.form['mp_name']
        year = request.form['p_year']
        yards = request.form['yards']
        touchdowns = request.form['touchdowns']
        total_sacks = request.form['total_sacks']
        total_fumbles = request.form['total_fumbles']
        number_games_played = request.form['number_games_played']

        if mp_name:
            df_id = dbOp.read_sql_raw("SELECT member_id" + " " 
                                "FROM TEAM_MEMBER as T join PLAYER_SCORE as P on T.member_id = P.pscore_id" + " "
                                "WHERE fname = \'" + name + "\'" + " and " 
                                    + "minit = \'" + mp_name + "\'" + " and "
                                    + "lname = \'" + lp_name + "\'" + " and " + "p_year = " + year)
        else:
            df_id = dbOp.read_sql_raw("SELECT member_id" + " " 
                                "FROM TEAM_MEMBER as T join PLAYER_SCORE as P on T.member_id = P.pscore_id" + " "
                                "WHERE fname = \'" + name + "\'" + " and "
                                    + "lname = \'" + lp_name + "\'" + " and " + "p_year = " + year)            

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
            flash('Player Information: Incorrect [name] or [year]!', 'danger')
            logging.info(f'%s, %s Player information: Incorrect [{name}] or [{year}]!', name, year)
        elif not error_list:
            flash(f'Player Information for [{name}], [{year}]: Updated!', 'success')
            logging.info(f'%s, %s Player information: [{name}] or [{year}]: Updated!', name, year)
        else:
            flash(f'Player Information for [{name}], [{year}]: {error_list} have not been updated!', 'danger')
            logging.info(f'%s, %s Player information: [{name}] or [{year}]: have not been updated!', name, year)
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

@admin.route("/update_cscore", methods=['POST', 'GET'])
def update_cscore():
    if request.method == "POST":
        name = request.form['c_name']
        lc_name = request.form['lc_name']
        mc_name = request.form['mc_name']
        year = request.form['c_year']
        years_coached = request.form['years_coached']
        total_games_coached = request.form['total_games_coached']
        sb_champ_won = request.form['sb_champ_won']
        league_champ_won = request.form['league_champ_won']
        conference_champ_won = request.form['conference_champ_won']
        division_champ_won = request.form['division_champ_won']

        if mc_name:
            df_id = dbOp.read_sql_raw("SELECT member_id" + " " 
                                "FROM TEAM_MEMBER as T join COACH_SCORE as C on T.member_id = C.cscore_id" + " "
                                "WHERE fname = \'" + name + "\'" + " and " 
                                    + "minit = \'" + mc_name + "\'" + " and "
                                    + "lname = \'" + lc_name + "\'" + " and " + "c_year = " + year)
        else:
            df_id = dbOp.read_sql_raw("SELECT member_id" + " " 
                                "FROM TEAM_MEMBER as T join COACH_SCORE as C on T.member_id = C.cscore_id" + " "
                                "WHERE fname = \'" + name + "\'" + " and "
                                    + "lname = \'" + lc_name + "\'" + " and " + "c_year = " + year)            

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
            flash('Coach Information for: Incorrect [name] or [year]!', 'danger')
            logging.info(f'%s, %s Incorrect coach information [{name}] or [{year}] entered', name, year)
        elif not error_list:
            flash(f'Coach Information for [{name}], [{year}]: Updated!', 'success')
            logging.info(f'%s, %s Coach information [{name}], [{year}] updated', name, year)
        else:
            flash(f'Coach Information for [{name}], [{year}]: {error_list} have not been updated!', 'danger')
            logging.info(f'%s, %s Coach information [{name}], [{year}] not updated', name, year)
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
            flash('Team Information: Incorrect [name] or [year]!', 'danger')
            logging.info(f'%s, %s Incorrect team information [{name}] or [{year}]', name, year)
        elif not error_list:
            flash(f'Team Information for [{name}], [{year}]: Updated!', 'success')
            logging.info(f'%s, %s Team information [{name}], [{year}] updated', name, year)
        else:
            flash(f'Team Information for [{name}], [{year}]: {error_list} have not been updated!', 'danger')
            logging.info(f'%s, %s Team information [{name}], [{year}] not updated', name, year)
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
        draft_add = request.form.get("draft_add")
        draft_remove = request.form.get("draft_remove")       

        rand_id = random.randint(1, 1000)

        df_id = dbOp.read_sql_raw("SELECT member_id from TEAM_MEMBER")
        #df_team = dbOp.read_sql_raw("SELECT team_name from TEAM")

        #checks if first name and last name are absence 
        name_flag = 1
        if not fname or not lname:
            name_flag = 0

        #ensures that member_id will be unique
        check_random = 1
        while check_random == 1 and name_flag:
            for id in df_id['member_id']:
                if rand_id == id:
                    rand_id = random.randint(1, 1000)
                    continue
            check_random = 0

        check_flag = 0
        inserted_flag = 0
        check_delete = 0
        if name_flag == 1 and draft_add is not None and check_player is not None or check_coach is not None: #and team_flag == 1:
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

            if check_player and not check_coach and check_flag:
                inserted_flag = dbOp.insert_sql("PLAYER", rand_id)
            elif not check_player and check_coach and check_flag:
                inserted_flag = dbOp.insert_sql("COACH", rand_id)

        elif name_flag == 1 and draft_remove is not None: #only remove if player and coach does not have a team
            if minit:
                team_name = dbOp.read_sql_raw(f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{fname}\' and minit=\'{minit}\' and lname=\'{lname}\'")
            else:
                team_name = dbOp.read_sql_raw(f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{fname}\' and minit is null and lname=\'{lname}\'")
            
            if team_name.empty:
                check_delete = 0
            elif team_name['te_name'].iloc[0] is None:
                if minit:
                    check_delete = dbOp.delete_sql("TEAM_MEMBER", f"fname=\'{fname}\' and minit=\'{minit}\' and lname =\'{lname}\'")
                else: 
                    check_delete = dbOp.delete_sql("TEAM_MEMBER", f"fname=\'{fname}\' and minit is null and lname =\'{lname}\'")

        if name_flag == 0: #or team_flag == 0:
            flash('Drafted Information: Draft [first name] or [last name] missing!', 'danger')
            logging.info(f'%s, %s Draft information [{fname} or [{lname} missing!', fname, lname)
        elif draft_add is not None: #or not team_flag:
            if not inserted_flag and not check_flag:
                flash(f'Drafted Information for [{fname}], [{lname}]: Draft invalid', 'danger')
                logging.info(f'%s, %s Draft information [{fname}] or [{lname}] invalid', fname, lname)
            else:
                flash(f'Drafted Information for [{fname}], [{lname}]: Draft added!', 'success')
                logging.info(f'%s, %s Draft information [{fname}] or [{lname}] added!', fname, lname)
        elif draft_remove is not None:
            if not check_delete:
                flash(f'Drafted Information for [{fname}], [{lname}]: Remove Invalid!', 'danger')
                logging.info(f'%s, %s Draft information [{fname}] or [{lname}] remove invalid!', fname, lname)
            else: 
                flash(f'Drafted Information for [{fname}], [{lname}]: Removed!', 'success')
                logging.info(f'%s, %s Draft information [{fname}] or [{lname}] removed!', fname, lname)

        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

@admin.route("/add_player", methods=['POST', 'GET'])
def add_player():
    if request.method == "POST":
        update_pteam = request.form['update_pteam']
        new_player = request.form['update_fname']
        update_minit = request.form['update_minit']
        update_lname = request.form['update_lname']

        team_flag = 0
        player_flag = 1
        
        df_items = dbOp.read_sql_raw("select * from TEAM_MEMBER as T join PLAYER as P on T.member_id = P.player_id")
        
        #checks if player exisits
        if update_minit:
            df_exists = pd.Series( [ str(i) + str(j) + str(k) for i,j, k in df_items[['fname', 'minit', 'lname']].values ] )
            new_entry = [str(new_player) + str(update_minit) + str(update_lname)]

            select_op = f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{new_player}\' and minit=\'{update_minit}\' and lname=\'{update_lname}\'"
            update_op = f"fname=\'{new_player}\' and minit=\'{update_minit}\' and lname=\'{update_lname}\'"
        else:
            df_exists = pd.Series( [ str(i) + str(j) for i,j in df_items[['fname', 'lname']].values ] )
            new_entry = [str(new_player) + str(update_lname)] 

            select_op = f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{new_player}\' and minit is null and lname=\'{update_lname}\'"
            update_op = f"fname=\'{new_player}\' and minit is null and lname=\'{update_lname}\'"        

        entry = df_items[ df_exists.isin(new_entry) ]
        
        if entry.empty:
            player_flag = 0

        #for item in df_items['fname']:
            #if item == new_player:
                #player_flag = 1

        #check if previous team exists
        df_items = dbOp.read_sql_raw(f"SELECT * FROM TEAM as T join TEAM_MEMBER as P on T.team_name = P.te_name WHERE {update_op}")
        previous_team = ''
        if not df_items.empty:
            for item in df_items['team_name']:
                if item == update_pteam:
                    team_flag = 1

        check_flag = 0
        if update_pteam and new_player and update_lname and player_flag:
            df_items = dbOp.read_sql_raw(select_op)
            check_flag = dbOp.update_sql("TEAM_MEMBER", f"te_name = \'{update_pteam}\'", update_op)
        
        if check_flag: #check for previous team
            if team_flag:
                previous_team = df_items['te_name'].iloc[0]
                dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster - 1 WHERE team_name = \'{previous_team}\'")
            dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster + 1 WHERE team_name = \'{update_pteam}\'")

        if check_flag: #or team_flag == 0:
            flash(f'Player [{new_player}] was added to team [{update_pteam}]!', 'success')
            logging.info(f'%s, %s Player [{new_player}] was added to team [{update_pteam}]', new_player, update_pteam)
        else:
            flash(f'Player [{new_player}] cannot be added to team [{update_pteam}]!', 'danger')
            logging.info(f'%s, %s Player [{new_player}] cannot be added to team [{update_pteam}]', new_player, update_pteam)
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")    

@admin.route("/remove_player", methods=['POST', 'GET'])
def remove_player():
    if request.method == "POST":
        update_pteam = request.form['update_pteam']
        new_player = request.form['update_fname']
        update_minit = request.form['update_minit']
        update_lname = request.form['update_lname']

        team_flag = 0
        player_flag = 1
        
        df_items = dbOp.read_sql_raw("select * from TEAM_MEMBER as T join PLAYER as P on T.member_id = P.player_id")

        #checks if player exisits
        if update_minit:
            df_exists = pd.Series( [ str(i) + str(j) + str(k) for i,j, k in df_items[['fname', 'minit', 'lname']].values ] )
            new_entry = [str(new_player) + str(update_minit) + str(update_lname)]

            select_op = f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{new_player}\' and minit=\'{update_minit}\' and lname=\'{update_lname}\'"
            update_op = f"fname=\'{new_player}\' and minit=\'{update_minit}\' and lname=\'{update_lname}\'"
        else:
            df_exists = pd.Series( [ str(i) + str(j) for i,j in df_items[['fname', 'lname']].values ] )
            new_entry = [str(new_player) + str(update_lname)] 

            select_op = f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{new_player}\' and minit is null and lname=\'{update_lname}\'"
            update_op = f"fname=\'{new_player}\' and minit is null and lname=\'{update_lname}\'"        

        entry = df_items[ df_exists.isin(new_entry) ]
        
        if entry.empty:
            player_flag = 0

        #checks if previous team exists
        df_items = dbOp.read_sql_raw(f"SELECT * FROM TEAM as T join TEAM_MEMBER as P on T.team_name = P.te_name WHERE {update_op}")
        if not df_items.empty:
            for item in df_items['team_name']:
                if item == update_pteam:
                    team_flag = 1

        check_flag = 0
        if update_pteam and new_player and update_lname and player_flag and team_flag:
            check_flag = dbOp.update_sql("TEAM_MEMBER", f"te_name = null", update_op)
            #check_flag = dbOp.delete_sql("TEAM_MEMBER", f"fname = \'{new_player}\'")
        
        if check_flag:
            dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster - 1 WHERE team_name = \'{update_pteam}\'")

        if check_flag: #or team_flag == 0:
            flash(f'Player [{new_player}] was removed from team [{update_pteam}]!', 'success')
            logging.info(f'%s, %s Player [{new_player}] removed from team [{update_pteam}]', new_player, update_pteam)
        else:
            flash(f'Player [{new_player}]  was not removed from team [{update_pteam}]!', 'danger')
            logging.info(f'%s, %s Player [{new_player}] was not removed from team [{update_pteam}]', new_player, update_pteam)
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")   


@admin.route("/add_coach", methods=['POST', 'GET'])
def add_coach():
    if request.method == "POST":
        update_cteam = request.form['update_cteam']
        new_coach = request.form['new_coach']
        update_cminit = request.form['update_cminit']
        update_clname = request.form['update_clname']

        team_flag = 0
        coach_flag = 1
        
        df_items = dbOp.read_sql_raw("select * from TEAM_MEMBER as T join COACH as C on T.member_id = C.coach_id")

        #checks if player exisits
        if update_cminit:
            df_exists = pd.Series( [ str(i) + str(j) + str(k) for i,j, k in df_items[['fname', 'minit', 'lname']].values ] )
            new_entry = [str(new_coach) + str(update_cminit) + str(update_clname)]

            select_op = f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{new_coach}\' and minit=\'{update_cminit}\' and lname=\'{update_clname}\'"
            update_op = f"fname=\'{new_coach}\' and minit=\'{update_cminit}\' and lname=\'{update_clname}\'"
        else:
            df_exists = pd.Series( [ str(i) + str(j) for i,j in df_items[['fname', 'lname']].values ] )
            new_entry = [str(new_coach) + str(update_clname)] 

            select_op = f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{new_coach}\' and minit is null and lname=\'{update_clname}\'"
            update_op = f"fname=\'{new_coach}\' and minit is null and lname=\'{update_clname}\'"        

        entry = df_items[ df_exists.isin(new_entry) ]
        
        if entry.empty:
            coach_flag = 0

        df_items = dbOp.read_sql_raw(f"SELECT * FROM TEAM as T join TEAM_MEMBER as P on T.team_name = P.te_name WHERE {update_op}")
        previous_team = ''
        for item in df_items['team_name']:
            if item == update_cteam:
                team_flag = 1

        check_flag = 0
        if update_cteam and new_coach and update_clname and coach_flag:
            df_items = dbOp.read_sql_raw(select_op)
            check_flag = dbOp.update_sql("TEAM_MEMBER", f"te_name = \'{update_cteam}\'", update_op)
        
        if check_flag:
            if team_flag:
                previous_team = df_items['te_name'].iloc[0]
                dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster - 1 WHERE team_name = \'{previous_team}\'")
            dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster + 1 WHERE team_name = \'{update_cteam}\'")

        if check_flag: #or team_flag == 0:
            flash(f'Coach [{new_coach}] was added to team [{update_cteam}]!', 'success')
            logging.info(f'%s, %s Coach [{new_coach}] was added to team [{update_cteam}]', new_coach, update_cteam)
        else:
            flash(f'Coach [{new_coach}] cannot be added to team [{update_cteam}]!', 'danger')
            logging.info(f'%s, %s Coach [{new_coach}] cannot be added to team [{update_cteam}]', new_coach, update_cteam)
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")    


@admin.route("/remove_coach", methods=['POST', 'GET'])
def remove_coach():
    if request.method == "POST":
        update_cteam = request.form['update_cteam']
        new_coach = request.form['new_coach']
        update_cminit = request.form['update_cminit']
        update_clname = request.form['update_clname']

        team_flag = 0
        coach_flag = 1
        
        df_items = dbOp.read_sql_raw("select * from TEAM_MEMBER as T join COACH as C on T.member_id = C.coach_id")

        #checks if player exisits
        if update_cminit:
            df_exists = pd.Series( [ str(i) + str(j) + str(k) for i,j, k in df_items[['fname', 'minit', 'lname']].values ] )
            new_entry = [str(new_coach) + str(update_cminit) + str(update_clname)]

            #select_op = f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{new_coach}\' and minit=\'{update_cminit}\' and lname=\'{update_clname}\'"
            update_op = f"fname=\'{new_coach}\' and minit=\'{update_cminit}\' and lname=\'{update_clname}\'"
        else:
            df_exists = pd.Series( [ str(i) + str(j) for i,j in df_items[['fname', 'lname']].values ] )
            new_entry = [str(new_coach) + str(update_clname)] 

            #select_op = f"SELECT te_name from TEAM_MEMBER WHERE fname=\'{new_coach}\' and minit is null and lname=\'{update_clname}\'"
            update_op = f"fname=\'{new_coach}\' and minit is null and lname=\'{update_clname}\'"        

        entry = df_items[ df_exists.isin(new_entry) ]
        if entry.empty:
            coach_flag = 0

        #checks if previous team exists
        df_items = dbOp.read_sql_raw(f"SELECT * FROM TEAM as T join TEAM_MEMBER as P on T.team_name = P.te_name WHERE {update_op}")
        if not df_items.empty:
            for item in df_items['team_name']:
                if item == update_cteam:
                    team_flag = 1

        check_flag = 0
        if update_cteam and new_coach and update_clname and coach_flag and team_flag:
            check_flag = dbOp.update_sql("TEAM_MEMBER", f"te_name = null", update_op)
            #check_flag = dbOp.delete_sql("TEAM_MEMBER", f"fname = \'{new_player}\'")

        if check_flag:
            dbOp.read_sql_raw(f"UPDATE TEAM SET roster = roster - 1 WHERE team_name = \'{update_cteam}\'")            

        if check_flag: #or team_flag == 0:
            flash(f'Coach [{new_coach}] was removed from team [{update_cteam}]!', 'success')
            logging.info(f'%s, %s Coach [{new_coach}] was removed from team [{update_cteam}]', new_coach, update_cteam)
        else:
            flash(f'Coach [{new_coach}]  was not removed from team [{update_cteam}]!', 'danger')
            logging.info(f'%s, %s Coach [{new_coach}] was not removed from team [{update_cteam}]', new_coach, update_cteam)
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")    

################################################ --- MATCH ---- ############################################################################
@admin.route("/add_match", methods=['POST', 'GET'])
def add_match():
    if request.method == "POST":
        t1 = request.form['Mte_name1']
        t2 = request.form['Mte_name2']
        date = request.form['date']

        rand_id = random.randint(1, 1000)

        df_id = dbOp.read_sql_raw("SELECT * from MATCH")
        #df_team = dbOp.read_sql_raw("SELECT team_name from TEAM")

        identical_check = 1
        df_exists = pd.Series( [ str(i) + str(j) + str(k) for i,j, k in df_id[['Mte_name1', 'Mte_name2', 'date']].values ] )
        new_entry = [str(t1) + str(t2) + str(date)]

        entry = df_id[ df_exists.isin(new_entry) ]
        
        if entry.empty:
            identical_check = 0

        #ensures that member_id will be unique
        check_random = 1
        while check_random and not identical_check:
            for id in df_id['match_id']:
                if rand_id == id:
                    rand_id = random.randint(1, 1000)
                    continue
            check_random = 0


        if t1 and t2 and date and not identical_check:
            check_flag = dbOp.insert_sql("MATCH", f"{rand_id}, \'{t1}\', \'{t2}\', \'{date}\', null, null, null, null")
            number_of_fans = dbOp.read_sql_raw("select profile_id from Fan")
            if not number_of_fans.empty:
                fan_array = number_of_fans['profile_id'].tolist()
                for user_id in fan_array:
                    check_insert = dbOp.insert_sql("NOTIFIES", f"{rand_id}, {user_id}")
        else:
            check_flag = 0

        if check_flag: #or team_flag == 0:
            flash(f'Match between [{t1}] and [{t2}] added for [{date}]!', 'success')
            logging.info(f'%s, %s match between [{t1}] and [{t2}] was added', t1, t2)
        elif identical_check:
            flash(f'Match between [{t1}] and [{t2}] already exists for [{date}]!', 'danger')
            logging.info(f'%s, %s match between [{t1}] and [{t2}] already exists', t1, t2)
        else:
            flash(f'Match between [{t1}] and [{t2}] not added for [{date}]!', 'danger')
            logging.info(f'%s, %s match between [{t1}] and [{t2}] was not added', t1, t2)

        return render_template("homeAdmin.html") 
    else:    
        return render_template("homeAdmin.html") 

#Match
@admin.route("/update_match", methods=['POST', 'GET'])
def update_match():
    if request.method == "POST":
        update_name1 = request.form['update_name1']
        update_name2 = request.form['update_name2']
        update_date = request.form['update_date']
        update_results = request.form['update_results']
        update_venue = request.form['update_venue']
        name1_win_ratio = request.form['name1_win_ratio']        
        name2_win_ratio = request.form['name2_win_ratio']

        df_id = dbOp.read_sql_raw("SELECT * from MATCH")
        #df_team = dbOp.read_sql_raw("SELECT team_name from TEAM")

        identical_check = 1

        df_exists = pd.Series( [ str(i) + str(j) + str(k) for i,j, k in df_id[['Mte_name1', 'Mte_name2', 'date']].values ] )
        new_entry = [str(update_name1) + str(update_name2) + str(update_date)]
        entry = df_id[ df_exists.isin(new_entry) ]
        if entry.empty:
            identical_check = 0

        update_list = ""
        update_op = f"Mte_name1 = \'{update_name1}\' and Mte_name2 = \'{update_name2}\' and date = \'{update_date}\'"
        if identical_check:
            if update_venue:
                check_flag = dbOp.update_sql("MATCH", f"venue = \'{update_venue}\'", update_op)
                if check_flag == 1:
                    update_list += "[venue] "

            if is_integer(update_results.translate({ord(i): None for i in '-'})):
                check_flag = dbOp.update_sql("MATCH", f"results = \'{update_results}\'", update_op)
                if check_flag == 1:
                    update_list += "[results] "
                
            if is_integer(name1_win_ratio.translate({ord(i): None for i in '%-'})):
                check_flag = dbOp.update_sql("MATCH", f"t1_win_lost_ratio = \'{name1_win_ratio}\'", update_op)
                if check_flag == 1:
                    update_list += "[Team 1 Win Ratio] "
            

            if is_integer(name2_win_ratio.translate({ord(i): None for i in '%-'})):
                check_flag = dbOp.update_sql("MATCH", f"t2_win_lost_ratio = \'{name2_win_ratio}\'", update_op)
                if check_flag == 1:
                    update_list += "[Team 2 Win Ratio] "

        if not identical_check:
            flash(f'Match information between [{update_name1}] and [{update_name2}] on [{update_date}] does not exist!', 'danger')
            logging.info(f'%s, %s match information between [{update_name1}] and [{update_name2}] check', update_name1, update_name2)
        elif not update_list:
            flash(f'Match information between [{update_name1}] and [{update_name2}] on [{update_date}]: Not updated!', 'success')
            logging.info(f'%s, %s match information between [{update_name1}] and [{update_name2}] not updated', update_name1,update_name2)
        else:
            flash(f'Match Information between [{update_name1}] and [{update_name2}] on [{update_date}]: {update_list} have been updated!', 'success')
            logging.info(f'%s, %s match information between [{update_name1}] and [{update_name2}] updated', update_name1,update_name2)
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

@admin.route("/delete_match", methods=['POST', 'GET'])
def delete_match():
    if request.method == "POST":
        delete_name1 = request.form['delete_name1']
        delete_name2 = request.form['delete_name2']
        delete_date = request.form['delete_date']

        df_id = dbOp.read_sql_raw("SELECT * from MATCH")
        #df_team = dbOp.read_sql_raw("SELECT team_name from TEAM")

        identical_check = 1
        df_exists = pd.Series( [ str(i) + str(j) + str(k) for i,j, k in df_id[['Mte_name1', 'Mte_name2', 'date']].values ] )
        new_entry = [str(delete_name1) + str(delete_name2) + str(delete_date)]
        entry = df_id[ df_exists.isin(new_entry) ]
        if entry.empty:
            identical_check = 0


        check_flag = 0
        delete_op = f"Mte_name1 = \'{delete_name1}\' and Mte_name2 = \'{delete_name2}\' and date = \'{delete_date}\'"
        if identical_check:
            check_flag = dbOp.delete_sql("MATCH", delete_op)

        if not identical_check:
            flash(f'Match information between [{delete_name1}] and [{delete_name2}] on [{delete_date}] does not exist!', 'danger')
            logging.info(f'%s, %s match information between [{delete_name1}] and [{delete_name2}] check', delete_name1, delete_name2)
        elif not check_flag:
            flash(f'Match information between [{delete_name1}] and [{delete_name2}] on [{delete_date}]: Not deleted!', 'danger')
            logging.info(f'%s, %s match information between [{delete_name1}] and [{delete_name2}] not deleted', delete_name1, delete_name2)
        else:
            flash(f'Match information between [{delete_name1}] and [{delete_name2}]on [{delete_date}]: Deleted!', 'success')
            logging.info(f'%s, %s match information between [{delete_name1}] and [{delete_name2}] deleted', delete_name1, delete_name2)
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

################################################ --- User Verification ---- ############################################################################

@admin.route("/add_verification", methods=['POST', 'GET'])
def add_verification():
    if request.method == "POST":
        add_username = request.form['add_username']
        add_user = request.form['add_user']

        df_u = dbOp.read_sql_raw(f"SELECT * FROM FAN WHERE username = \'{add_username}\'")

        already_flag = 0
        check_flag = 0
        exist_flag = 1
        if not df_u.empty:
            if add_user == df_u['admin_ver_name'].iloc[0]:
                already_flag = 1
            else:
                check_flag = dbOp.update_sql("FAN", f" admin_ver_name = \'{add_user}\'", f"username = \'{add_username}\'")
        else:
            exist_flag = 0

        if not exist_flag:
            flash(f'Verification: User [{add_username}] does not exist!', 'danger')
            logging.info(f'%s User [{add_username}] does not exist', add_username)
        elif already_flag:
            flash(f'Verification: User [{add_username}] already verified!', 'success')
            logging.info(f'%s User [{add_username}] already verified', add_username)
        elif check_flag:
            flash(f'Verfication: User [{add_username}] verified!', 'success')
            logging.info(f'%s User [{add_username}] verified', add_username)
        else:
            flash(f'Verification: User [{add_username}] could not be verified!', 'danger')
            logging.info(f'%s User [{add_username}] cannot be verified', add_username)
                
        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")


@admin.route("/remove_verification", methods=['POST', 'GET'])
def remove_verification():
    if request.method == "POST":
        remove_username = request.form['remove_username']

        df_u = dbOp.read_sql_raw(f"SELECT * FROM FAN WHERE username = \'{remove_username}\'")

        already_flag = 0
        check_flag = 0
        exist_flag = 1
        if not df_u.empty:
            if df_u['admin_ver_name'].iloc[0] is not None:
                check_flag = dbOp.update_sql("FAN", f"admin_ver_name = null", f"username = \'{remove_username}\'")
            else:
                already_flag = 1
        else:
            exist_flag = 0

        if not exist_flag:
            flash(f'Verification: User [{remove_username}] does not exist!', 'danger')
            logging.info(f'%s User [{remove_username}] does not exist', remove_username)
        elif already_flag:
            flash(f'Verification: User [{remove_username}] already un-verified!', 'success')
            logging.info(f'%s User [{remove_username}] already un-verified', remove_username)
        elif check_flag:
            flash(f'Verfication: User [{remove_username}] verification removed!', 'success')
            logging.info(f'%s User [{remove_username}] verification removed', remove_username)
        else:
            flash(f'Verification: User [{remove_username}] could not be un-verified!', 'danger')
            logging.info(f'%s User [{remove_username}] cannot be unverified', remove_username)

        return render_template("homeAdmin.html")
    else:
        return render_template("homeAdmin.html")
