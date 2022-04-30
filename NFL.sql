use master
GO
if exists (select * from master.sys.databases where name = 'nfl')
  drop database nfl
GO
create database nfl
GO
use nfl
GO

CREATE TABLE TEAM (
  team_name VARCHAR(20) NOT NULL,
  mascot VARCHAR(20) NOT NULL,
  city VARCHAR(20) NOT NULL,
  logo VARCHAR(20) NOT NULL,
  home_stadium VARCHAR(20) NOT NULL,
  division VARCHAR(5) NOT NULL,
  conference CHAR(3), -- AFC and NFC,
  [owner] VARCHAR(20),
  team_color VARCHAR(10) NOT NULL,
  roster INTEGER NOT NULL,
  established_year date NOT NULL,

  PRIMARY KEY (team_name),
  UNIQUE (mascot, city, logo, home_stadium),
);

CREATE TABLE TEAM_MEMBER (
  member_id INTEGER NOT NULL,
  fname VARCHAR(20) NOT NULL,
  minit VARChar(5),
  lname VARCHAR(20) NOT NULL,
  te_name VARCHAR(20),

  PRIMARY KEY (member_id),
  FOREIGN KEY (te_name) REFERENCES TEAM(team_name) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE PLAYER (
  player_id INTEGER NOT NULL,
  FOREIGN KEY (player_id) REFERENCES TEAM_MEMBER(member_id) ON DELETE CASCADE
);

CREATE TABLE COACH (
  coach_id INTEGER NOT NULL,
  FOREIGN KEY (coach_id) REFERENCES TEAM_MEMBER(member_id) ON DELETE CASCADE
);

CREATE TABLE MEMBER_CONTRACT (
  member_id INTEGER NOT NULL,
  [contract_name] VARCHAR(20) NOT NULL,
  signed_date date NOT NULL,
  active_status VARCHAR(20) NOT NULL,

  PRIMARY KEY (member_id, [contract_name], signed_date),
  FOREIGN KEY (member_id) REFERENCES TEAM_MEMBER(member_id) ON DELETE CASCADE
);

CREATE TABLE PLAYER_SCORE (
  p_year INTEGER NOT NULL,
  pscore_id INTEGER NOT NULL,
  yards INTEGER DEFAULT 0,
  touchdowns INTEGER DEFAULT 0,
  total_sacks INTEGER DEFAULT 0,
  total_fumbles INTEGER DEFAULT 0,
  number_games_played INTEGER DEFAULT 0,

  PRIMARY KEY (p_year, pscore_id), 
  FOREIGN KEY (pscore_id) REFERENCES TEAM_MEMBER(member_id) ON DELETE CASCADE
);

CREATE TABLE COACH_SCORE (
  c_year INTEGER NOT NULL,
  cscore_id INTEGER NOT NULL,
  years_coached INTEGER DEFAULT 0,
  total_games_coached INTEGER DEFAULT 0,
  sb_champ_won INTEGER DEFAULT 0,
  league_champ_won INTEGER DEFAULT 0,
  conference_champ_won INTEGER DEFAULT 0,
  division_champ_won INTEGER DEFAULT 0,

  PRIMARY KEY (c_year, cscore_id),
  FOREIGN KEY (cscore_id) REFERENCES TEAM_MEMBER(member_id) ON DELETE CASCADE
);

CREATE TABLE TEAM_SCORE (
  [year] INTEGER NOT NULL,
  t_name VARCHAR(20) NOT NULL,
  total_field_goals INTEGER DEFAULT 0,
  total_touchdowns INTEGER DEFAULT 0,
  total_passing_yards INTEGER DEFAULT 0,
  avg_time_possession INTEGER DEFAULT 0,
  total_rushing_yards INTEGER DEFAULT 0,
  total_offensive_yards INTEGER DEFAULT 0,

  PRIMARY KEY ([year], t_name),
  FOREIGN KEY (t_name) REFERENCES TEAM(team_name) ON DELETE CASCADE
);

CREATE TABLE [MATCH] (
  match_id INTEGER NOT NULL,
  Mte_name1 VARCHAR(20) NOT NULL,
  Mte_name2 VARCHAR(20) NOT NULL,
  [date] date NOT NULL,
  results VARCHAR(5), --10-11
  venue VARCHAR(20),
  t1_win_lost_ratio VARCHAR(10), -- 10%-90&
  t2_win_lost_ratio VARCHAR(10), -- 90%-10&

  PRIMARY KEY (match_id),
  CONSTRAINT unique_match CHECK (Mte_name1 <> Mte_name2),
  FOREIGN KEY (Mte_name1) REFERENCES TEAM(team_name), -- no need to cascade since teams should not be deleted
  FOREIGN KEY (Mte_name2) REFERENCES TEAM(team_name)
);

CREATE TABLE ADMINISTRATOR (
  username VARCHAR(20) NOT NULL,
  email VARCHAR(20) NOT NULL, 
  hashed_password VARCHAR(20) NOT NULL,

  PRIMARY KEY (username),
  UNIQUE (email, hashed_password)
);

CREATE TABLE FAN (
  profile_id INTEGER NOT NULL,
  admin_ver_name VARCHAR(20),
  Fa_team VARCHAR(20),
  Fo_team VARCHAR(20),
  username VARCHAR(20) NOT NULL,
  email VARCHAR(20) NOT NULL,
  hashed_password VARCHAR(20) NOT NULL,

  PRIMARY KEY (profile_id),
  CONSTRAINT unique_fan_team CHECK (Fa_team <> Fo_team),
  FOREIGN KEY (Fa_team) REFERENCES TEAM(team_name), -- no need to cascade since teams should not be deleted
  FOREIGN KEY (Fo_team) REFERENCES TEAM(team_name), -- also, the constraint is check that no  two teams will ever be the same
  FOREIGN KEY (admin_ver_name) REFERENCES ADMINISTRATOR(username) ON DELETE SET NULL ON UPDATE CASCADE,
  UNIQUE (username, email, hashed_password)
);

CREATE TABLE NOTIFIES (
  m_id INTEGER NOT NULL,
  p_id INTEGER NOT NULL,
  
  PRIMARY KEY (m_id, p_id),
  FOREIGN KEY (m_id) REFERENCES [MATCH](match_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (p_id) REFERENCES FAN(profile_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE POLLS (
  poll_id INTEGER NOT NULL,
  creator_name VARCHAR(20) NOT NULL,
  duration INTEGER NOT NULL, --convert time to seconds
  creation_date date NOT NULL, 
  poll_name VARCHAR(20) NOT NULL,
  poll_percentage VARCHAR(7), --10%-90%
  number_of_predictions INTEGER NOT NULL,
  team_name1 VARCHAR(20) NOT NULL,
  team_name2 VARCHAR(20) NOT NULL,

  PRIMARY KEY (poll_id),
  FOREIGN KEY (creator_name) REFERENCES ADMINISTRATOR(username) ON DELETE CASCADE ON UPDATE CASCADE,

);

CREATE TABLE PETITIONS (
  pf_id INTEGER NOT NULL,
  admin_id VARCHAR(20) NOT NULL

  PRIMARY KEY (pf_id, admin_id),
  FOREIGN KEY (admin_id) REFERENCES ADMINISTRATOR(username) ON DELETE CASCADE,
  FOREIGN KEY (pf_id) REFERENCES FAN(profile_id) ON DELETE CASCADE,
);

CREATE TABLE INTERACTS (
  ip_id INTEGER NOT NULL,
  if_id INTEGER NOT NULL,

  PRIMARY KEY (ip_id, if_id),
  FOREIGN KEY (ip_id) REFERENCES POLLS(poll_id) ON DELETE CASCADE,
  FOREIGN KEY (if_id) REFERENCES FAN(profile_id) ON DELETE CASCADE,
);
GO

INSERT INTO TEAM VALUES('team_name1', 'mascot1', 'city1', 'logo1', 'home_stad1', 'div1', 'AFC', 'owner1', 'blue1', 23, '2000-01-27');
INSERT INTO TEAM VALUES('team_name2', 'mascot2', 'city2', 'logo2', 'home_stad2', 'div1', 'AFC', 'owner2', 'blue2', 23, '1999-01-26');
INSERT INTO TEAM VALUES('team_name3', 'mascot3', 'city3', 'logo3', 'home_stad3', 'div1', 'AFC', 'owner3', 'blue3', 23, '2001-01-27');
INSERT INTO TEAM VALUES('team_name4', 'mascot4', 'city4', 'logo4', 'home_stad4', 'div1', 'AFC', 'owner4', 'blue4', 23, '2005-01-26');
INSERT INTO TEAM VALUES('team_name5', 'mascot5', 'city5', 'logo5', 'home_stad5', 'div2', 'AFC', 'owner5', 'blue5', 23, '2002-01-27');
INSERT INTO TEAM VALUES('team_name6', 'mascot6', 'city6', 'logo6', 'home_stad6', 'div2', 'AFC', 'owner6', 'blue6', 23, '1997-01-26');
INSERT INTO TEAM VALUES('team_name7', 'mascot7', 'city7', 'logo7', 'home_stad7', 'div2', 'AFC', 'owner7', 'blue7', 23, '2000-01-27');
INSERT INTO TEAM VALUES('team_name8', 'mascot8', 'city8', 'logo8', 'home_stad8', 'div2', 'AFC', 'owner8', 'blue8', 23, '1999-01-26');
INSERT INTO TEAM VALUES('team_name9', 'mascot9', 'city9', 'logo9', 'home_stad9', 'div3', 'NFC', 'owner9', 'blue9', 23, '1996-01-27');
INSERT INTO TEAM VALUES('team_name10', 'mascot10', 'city10', 'logo10', 'home_stad10', 'div3', 'NFC', 'owner10', 'blue10', 23, '1999-01-26');
INSERT INTO TEAM VALUES('team_name11', 'mascot11', 'city11', 'logo11', 'home_stad11', 'div3', 'NFC', 'owner11', 'blue11', 23, '2010-01-27');
INSERT INTO TEAM VALUES('team_name12', 'mascot12', 'city12', 'logo12', 'home_stad12', 'div3', 'NFC', 'owner12', 'blue12', 23, '1999-01-26');
INSERT INTO TEAM VALUES('team_name13', 'mascot13', 'city13', 'logo13', 'home_stad13', 'div4', 'NFC', 'owner13', 'blu13', 23, '1980-01-27');
INSERT INTO TEAM VALUES('team_name14', 'mascot14', 'city14', 'logo14', 'home_stad14', 'div4', 'NFC', 'owner14', 'blue14', 23, '1999-01-26');
INSERT INTO TEAM VALUES('team_name15', 'mascot15', 'city15', 'logo15', 'home_stad15', 'div4', 'NFC', 'owner15', 'blue15', 23, '1985-01-27');
INSERT INTO TEAM VALUES('team_name16', 'mascot16', 'city16', 'logo16', 'home_stad16', 'div4', 'NFC', 'owner16', 'blue16', 23, '1995-01-26');

INSERT INTO TEAM_MEMBER VALUES(1, 'fname1', 'm1', 'lname1', 'team_name1');
INSERT INTO TEAM_MEMBER VALUES(2, 'fname2', 'm2', 'lname2', 'team_name2');
INSERT INTO TEAM_MEMBER VALUES(3, 'fname3', 'm3', 'lname3', 'team_name1');
INSERT INTO TEAM_MEMBER VALUES(4, 'fname4', 'm4', 'lname4', 'team_name1');
INSERT INTO TEAM_MEMBER VALUES(5, 'fname5', 'm5', 'lname5', null);

INSERT INTO PLAYER VALUES(1);
INSERT INTO PLAYER VALUES(2);

INSERT INTO COACH VALUES(3);
INSERT INTO COACH VALUES(4);
INSERT INTO COACH VALUES(5)

INSERT INTO MEMBER_CONTRACT VALUES(1, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(2, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(3, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(4, 'contract4', '2000-02-10', 'inactive');

INSERT INTO PLAYER_SCORE VALUES(1999, 1, 1, 2, 3, 4, 5);
INSERT INTO PLAYER_SCORE VALUES(1998, 1, 1, 2, 3, 4, 5);
INSERT INTO PLAYER_SCORE VALUES(1998, 2, 1, 2, 3, 4, 5);


INSERT INTO COACH_SCORE VALUES(1997, 3, 1, 2, 3, 4, 5, 6);
INSERT INTO COACH_SCORE (c_year, cscore_id) VALUES(1995, 4);


INSERT INTO TEAM_SCORE VALUES(2000, 'team_name1', 1, 2, 3, 4, 5, 6);
INSERT INTO TEAM_SCORE VALUES(2001, 'team_name2', 1, 2, 3, 4, 5, 6);

INSERT INTO [MATCH] VALUES(1234, 'team_name1', 'team_name2', '2000-06-01', '6-1', 'venue1', '60%-40%', '40%-60%');
--INSERT INTO [MATCH] VALUES(4567, 'team_name1', 'team_name1', '2000-06-01', '6-1', 'venue1', '60%-40%', '40%-60%');


INSERT INTO ADMINISTRATOR VALUES('user1', 'a@blog.com', 'pass');

INSERT INTO FAN VALUES(56, 'user1', 'team_name1', 'team_name2', 'fuser1', 'femail1', 'fpass1');

INSERT INTO NOTIFIES VALUES(1234, 56);

INSERT INTO POLLS VALUES(78, 'user1', 3600, '2000-02-28', 'poll1', '10%-90%', 50, 'team_name11', 'team_name22');

INSERT INTO PETITIONS VALUES(56, 'user1');

INSERT INTO INTERACTS VALUES(78, 56);
