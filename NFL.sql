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
  team_name VARCHAR(40) NOT NULL,
  mascot VARCHAR(20) NOT NULL, --changed
  city VARCHAR(20) NOT NULL,
  logo VARCHAR(20) NOT NULL,
  home_stadium VARCHAR(40) NOT NULL,
  division VARCHAR(5) NOT NULL,
  conference CHAR(3) NOT NULL, -- AFC and NFC,
  [owner] VARCHAR(40) NOT NULL,
  team_color VARCHAR(20) NOT NULL,
  roster INTEGER DEFAULT 0 NOT NULL,
  established_year date NOT NULL,

  PRIMARY KEY (team_name),
  UNIQUE (mascot, city, logo, home_stadium),
);

CREATE TABLE TEAM_MEMBER (
  member_id INTEGER NOT NULL,
  fname VARCHAR(20) NOT NULL,
  minit VARChar(5),
  lname VARCHAR(20) NOT NULL,
  te_name VARCHAR(40),

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
  t_name VARCHAR(40) NOT NULL,
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
  Mte_name1 VARCHAR(40) NOT NULL,
  Mte_name2 VARCHAR(40) NOT NULL,
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
  username VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL, 
  hashed_password VARCHAR(250) NOT NULL,

  PRIMARY KEY (username),
  UNIQUE (email, hashed_password)
);

CREATE TABLE FAN (
  profile_id INTEGER NOT NULL IDENTITY(1,1),
  admin_ver_name VARCHAR(40),
  Fa_team VARCHAR(40),
  Fo_team VARCHAR(40),
  username VARCHAR(40) NOT NULL,
  firstname VARCHAR(40),
  lastname VARCHAR(40),
  email VARCHAR(40) NOT NULL,
  hashed_password VARCHAR(250) NOT NULL,

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
  creator_name VARCHAR(40) NOT NULL,
  duration INTEGER NOT NULL, --convert time to seconds
  creation_date date NOT NULL, 
  poll_name VARCHAR(40) NOT NULL,
  team1_vote INTEGER DEFAULT 0, --10%-90%
  team2_vote INTEGER DEFAULT 0,
  team_name1 VARCHAR(40) NOT NULL,
  team_name2 VARCHAR(40) NOT NULL,

  PRIMARY KEY (poll_id),
  FOREIGN KEY (creator_name) REFERENCES ADMINISTRATOR(username) ON DELETE CASCADE ON UPDATE CASCADE,

);

CREATE TABLE PETITIONS (
  pf_id INTEGER NOT NULL,
  admin_id VARCHAR(40) NOT NULL

  PRIMARY KEY (pf_id, admin_id),
  FOREIGN KEY (admin_id) REFERENCES ADMINISTRATOR(username) ON DELETE CASCADE,
  FOREIGN KEY (pf_id) REFERENCES FAN(profile_id) ON DELETE CASCADE,
);

CREATE TABLE INTERACTS (
  ip_id INTEGER NOT NULL,
  if_id INTEGER NOT NULL,
  interact_id INTEGER NOT NULL,
  comments VARCHAR(100),

  PRIMARY KEY (ip_id, if_id, interact_id),
  FOREIGN KEY (ip_id) REFERENCES POLLS(poll_id) ON DELETE CASCADE,
  FOREIGN KEY (if_id) REFERENCES FAN(profile_id) ON DELETE CASCADE,
);
GO

-- AFC
INSERT INTO TEAM VALUES('Buffalo Bills', 'Billy Buffalo', 'Orchard Park', 'Buffalo', 'Highmark Stadium', 'East', 'AFC', 'Terry Pegula', 'Royal blue', 5, '1959-10-28');
INSERT INTO TEAM VALUES('Miami Dolphins', 'The Dolphin', 'Miami Gardens', 'Dolphins', 'Hard Rock Stadium', 'East', 'AFC', 'Stephen M. Ross', 'Aqua', 5, '1965-08-16');
INSERT INTO TEAM VALUES('New England Patriots', 'Pat Patriot', 'Foxborough', 'Patriots', 'Gillette Stadium', 'East', 'AFC', 'Robert Kraft', 'Nautical blue', 5, '1959-11-16');
INSERT INTO TEAM VALUES('New York Jets', 'Missing', 'Florham Park', 'Jets', 'MetLife Stadium', 'East', 'AFC', 'Woody Johnson', 'Gotham green', 5, '1959-08-14');

INSERT INTO TEAM VALUES('Baltimore Ravens', 'Poe', 'Baltimore', 'Ravens', 'M&T Bank Stadium', 'North', 'AFC', 'Steve Bisciotti', 'Purple', 5, '1996-02-09');
INSERT INTO TEAM VALUES('Cincinnati Bengals', 'Bengal tiger', 'Cincinnati', 'Tiger', 'Paul Brown Stadium', 'North', 'AFC', 'Mike Brown', 'Black', 5, '1967-05-23');
INSERT INTO TEAM VALUES('Cleveland Browns', 'Chomps', 'Cleveland', 'Helmet', 'FirstEnergy Stadium', 'North', 'AFC', 'Jimmy Haslam', 'Brown', 5, '1944-06-04');
INSERT INTO TEAM VALUES('Pittsburgh Steelers', 'Steely McBeam', 'Pittsburgh', 'Steelers', 'Heinz Field', 'North', 'AFC', 'Rooney family', 'Gold', 5, '1933-07-08');

INSERT INTO TEAM VALUES('Houston Texans', 'Toro', 'Houston', 'Bull', 'NRG Stadium', 'South', 'AFC', 'Janice McNair', 'Deep steel blue', 5, '1999-10-06');
INSERT INTO TEAM VALUES('Indianapolis Colts', 'Blue', 'Indianapolis', 'Horseshoe', 'Lucas Oil Stadium', 'South', 'AFC', 'Jim Irsay', 'Speed blue', 5, '1953-01-23');
INSERT INTO TEAM VALUES('Jacksonville Jaguars', 'Jaxson de Ville', 'Jacksonville', 'Cougar', 'TIAA Bank Field', 'South', 'AFC', 'Shahid Khan', 'Teal', 5, '1993-11-30');
INSERT INTO TEAM VALUES('Tennessee Titans', 'T-Rac', 'Nashville', 'Titans Fire', 'Nissan Stadium', 'South', 'AFC', 'Amy Adams Strunk', 'Navy blue', 5, '1953-08-03');

INSERT INTO TEAM VALUES('Denver Broncos', 'Thunder and Miles', 'Denver', 'Horse', 'Empower Field at Mile High', 'West', 'AFC', 'Pat Bowlen Trust', 'Orange', 5, '1959-08-14');
INSERT INTO TEAM VALUES('Kansas City Chiefs', 'K. C. Wolf', 'Kansas City', 'Arrow', 'Arrowhead Stadium', 'West', 'AFC', 'Hunt family', 'Red', 5, '1959-08-14');
INSERT INTO TEAM VALUES('Las Vegas Raiders', 'Raider Rusher', 'Paradise', 'Eyepatch', 'Allegiant Stadium', 'West', 'AFC', 'Mark Davis', 'Silver', 5, '1960-01-30');
INSERT INTO TEAM VALUES('Los Angeles Chargers', 'Missing', 'Inglewood', 'Lightning bolt', 'SoFi Stadium', 'West', 'AFC', 'Dean Spanos', 'Powder blue', 5, '1959-08-14');

INSERT INTO TEAM VALUES('Dallas Cowboys', 'Star', 'Arlington', 'Star', 'AT&T Stadium', 'East', 'NFC', 'Jerry Jones', 'Navy blue', 5, '1960-01-28');
INSERT INTO TEAM VALUES('New York Giants', 'Missing', 'East Rutherford', 'NY', 'MetLife Stadium', 'East', 'NFC', 'John Mara', 'Red', 5, '1925-08-01');
INSERT INTO TEAM VALUES('Philadelphia Eagles', 'Swoop', 'Philadelphia', 'Eagles', 'Lincoln Financial Field', 'East', 'NFC', 'Jeffrey Lurie', 'Midnight green', 5, '1933-07-08');
INSERT INTO TEAM VALUES('Washington Commanders', 'Redskins', 'Landover', 'W', 'FedExField', 'East', 'NFC', 'Daniel Snyder', 'Burgundy', 5, '1932-07-09');

INSERT INTO TEAM VALUES('Chicago Bears', 'Rocky and Bearman', 'Chicago', 'C', 'Soldier Field', 'North', 'NFC', 'Virginia Halas McCaskey', 'Burnt orange', 5, '1920-09-17');
INSERT INTO TEAM VALUES('Detroit Lions', 'Roary the Lion', 'Detroit', 'Lion', 'Ford Field', 'North', 'NFC', 'Sheila Ford Hamp', 'Honolulu blue', 5, '1930-07-12');
INSERT INTO TEAM VALUES('Green Bay Packers', 'Missing', 'Green Bay', 'G', 'Lambeau Field', 'North', 'NFC', 'Green Bay Packers, Inc.', 'Dark green', 5, '1919-08-11');
INSERT INTO TEAM VALUES('Minnesota Vikings', 'Viktor the Viking', 'Minneapolis', 'Vikings', 'U.S. Bank Stadium', 'North', 'NFC', 'Mark Wilf', 'Purple', 5, '1960-01-28');

INSERT INTO TEAM VALUES('Atlanta Falcons', 'Freddie Falcon', 'Atlanta', 'Falcon', 'Mercedes-Benz Stadium', 'South', 'NFC', 'Arthur Blank', 'Black', 5, '1965-06-30');
INSERT INTO TEAM VALUES('Carolina Panthers', 'Sir Purr', 'Charlotte', 'Panther', 'Bank of America Stadium', 'South', 'NFC', 'David Tepper', 'Black', 5, '1993-10-26');
INSERT INTO TEAM VALUES('New Orleans Saints', 'Gumbo, Sir Saint', 'New Orleans', 'Saints Cross', 'Caesars Superdome', 'South', 'NFC', 'Gayle Benson', 'Old gold', 5, '1966-11-01');
INSERT INTO TEAM VALUES('Tampa Bay Buccaneers', 'Captain Fear', 'Tampa', 'Pirate Flag', 'Raymond James Stadium', 'South', 'NFC', 'Glazer family', 'Buccaneer red', 5, '1974-04-24');

INSERT INTO TEAM VALUES('Arizona Cardinals', 'Big Red', 'Glendale', 'Cardinals', 'State Farm Stadium', 'West', 'NFC', 'Michael Bidwill', 'Cardinal red', 5, '1898-01-27');
INSERT INTO TEAM VALUES('Los Angeles Rams', 'Rampage', 'Inglewood', 'LA', 'SoFi Stadium', 'West', 'NFC', 'Stan Kroenke', 'Royal blue', 5, '1936-01-26');
INSERT INTO TEAM VALUES('San Francisco 49ers', 'Sourdough Sam', 'Santa Clara', 'SF', 'Levi Stadium', 'West', 'NFC', '49ers Enterprises', 'Red', 5, '1944-06-04');
INSERT INTO TEAM VALUES('Seattle Seahawks', 'Taima the Hawk', 'Seattle', 'Seahawks', 'Lumen Field', 'West', 'NFC', 'The Paul Allen Trust', 'College navy', 5, '1974-06-04');

INSERT INTO TEAM_MEMBER VALUES(1, 'John', 'W', 'Williams', 'Buffalo Bills');
INSERT INTO TEAM_MEMBER VALUES(2, 'William', 'A', 'Adams', 'Buffalo Bills');
INSERT INTO TEAM_MEMBER VALUES(3, 'David', null, 'Meyer', 'Buffalo Bills');
INSERT INTO TEAM_MEMBER VALUES(4, 'Fischer', 'T', 'Bone', 'Buffalo Bills');
INSERT INTO TEAM_MEMBER VALUES(5, 'Jackie', null, 'Chan', 'Buffalo Bills');


INSERT INTO TEAM_MEMBER VALUES(6, 'Mack', 'U', 'Davis', 'Miami Dolphins');
INSERT INTO TEAM_MEMBER VALUES(7, 'Ken', null, 'Wheeler', 'Miami Dolphins');
INSERT INTO TEAM_MEMBER VALUES(8, 'Rednas', 'O', 'Deep', 'Miami Dolphins');
INSERT INTO TEAM_MEMBER VALUES(9, 'Johnny', 'C', 'Tiny', 'Miami Dolphins');
INSERT INTO TEAM_MEMBER VALUES(10, 'Mike', 'V', 'Mikey', 'Miami Dolphins');


INSERT INTO TEAM_MEMBER VALUES(11, 'Paimon', 'E', 'Britian', 'New England Patriots');
INSERT INTO TEAM_MEMBER VALUES(12, 'Bradon', 'A', 'Wheels', 'New England Patriots');
INSERT INTO TEAM_MEMBER VALUES(13, 'Altas', 'T', 'Gradient', 'New England Patriots');
INSERT INTO TEAM_MEMBER VALUES(14, 'Jason', 'L', 'Lackie', 'New England Patriots');
INSERT INTO TEAM_MEMBER VALUES(15, 'McArthur', 'O', 'Salley', 'New England Patriots');


INSERT INTO TEAM_MEMBER VALUES(16, 'Jackson', null, 'McBeth', 'New York Jets');
INSERT INTO TEAM_MEMBER VALUES(17, 'Asian', null, 'Ly', 'New York Jets');
INSERT INTO TEAM_MEMBER VALUES(18, 'Zeus', null, 'Li', 'New York Jets');
INSERT INTO TEAM_MEMBER VALUES(19, 'Arthur', null, 'Brownie', 'New York Jets');
INSERT INTO TEAM_MEMBER VALUES(20, 'Yusei', null, 'Johnson', 'New York Jets');

INSERT INTO TEAM_MEMBER VALUES(21, 'Grey', 'A', 'Mounty', 'Baltimore Ravens');
INSERT INTO TEAM_MEMBER VALUES(22, 'Greyson', 'A', 'Jackson', 'Baltimore Ravens');
INSERT INTO TEAM_MEMBER VALUES(23, 'Jerry', 'A', 'Kane', 'Baltimore Ravens');
INSERT INTO TEAM_MEMBER VALUES(24, 'Dia', 'A', 'Matthew', 'Baltimore Ravens');
INSERT INTO TEAM_MEMBER VALUES(25, 'Kelly', 'A', 'Nguyen', 'Baltimore Ravens');

INSERT INTO TEAM_MEMBER VALUES(26, 'Undie', 'E', 'Killer', 'Cincinnati Bengals');
INSERT INTO TEAM_MEMBER VALUES(27, 'Wacky', 'H', 'Hillview', 'Cincinnati Bengals');
INSERT INTO TEAM_MEMBER VALUES(28, 'Light', 'Q', 'Yagami', 'Cincinnati Bengals');
INSERT INTO TEAM_MEMBER VALUES(29, 'Dill', 'Y', 'Matthew', 'Cincinnati Bengals');
INSERT INTO TEAM_MEMBER VALUES(30, 'Ei', 'P', 'Nguyen', 'Cincinnati Bengals');

INSERT INTO TEAM_MEMBER VALUES(31, 'AAA', 'A', 'Saw', 'Cleveland Browns');
INSERT INTO TEAM_MEMBER VALUES(32, 'BBB', 'B', 'Vrit', 'Cleveland Browns');
INSERT INTO TEAM_MEMBER VALUES(33, 'CCC', 'C', 'Kane', 'Cleveland Browns');
INSERT INTO TEAM_MEMBER VALUES(34, 'DDD', 'D', 'Grand', 'Cleveland Browns');
INSERT INTO TEAM_MEMBER VALUES(35, 'EEE', 'E', 'Nill', 'Cleveland Browns');

INSERT INTO TEAM_MEMBER VALUES(36, 'Ill', null, 'Lord', 'Pittsburgh Steelers');
INSERT INTO TEAM_MEMBER VALUES(37, 'Bruce', null, 'Ten', 'Pittsburgh Steelers');
INSERT INTO TEAM_MEMBER VALUES(38, 'Yen', 'P', 'Press', 'Pittsburgh Steelers');
INSERT INTO TEAM_MEMBER VALUES(39, 'Jilly', 'I', 'Immortal', 'Pittsburgh Steelers');
INSERT INTO TEAM_MEMBER VALUES(40, 'Jessie', 'J', 'Jam', 'Pittsburgh Steelers');

INSERT INTO TEAM_MEMBER VALUES(41, 'Ussie', null, 'Penny', 'Houston Texans');
INSERT INTO TEAM_MEMBER VALUES(42, 'Tenson', null, 'Eye', 'Houston Texans');
INSERT INTO TEAM_MEMBER VALUES(43, 'Ben', 'W', 'Tennyson', 'Houston Texans');
INSERT INTO TEAM_MEMBER VALUES(44, 'Uc', 'A.E.', 'Gress', 'Houston Texans');
INSERT INTO TEAM_MEMBER VALUES(45, 'Illya', 'Q', 'Nickson', 'Houston Texans');

INSERT INTO TEAM_MEMBER VALUES(46, 'Beeler', 'L', 'Mountie', 'Indianapolis Colts');
INSERT INTO TEAM_MEMBER VALUES(47, 'Dan', 'U', 'Jacky', 'Indianapolis Colts');
INSERT INTO TEAM_MEMBER VALUES(48, 'Tripe', 'W', 'Myster', 'Indianapolis Colts');
INSERT INTO TEAM_MEMBER VALUES(49, 'Johnny', 'O.I.', 'Matthew', 'Indianapolis Colts');
INSERT INTO TEAM_MEMBER VALUES(50, 'Singy', 'S', 'Wow', 'Indianapolis Colts');

INSERT INTO TEAM_MEMBER VALUES(51, 'Grenie', 'A.C.', 'World', 'Jacksonville Jaguars');
INSERT INTO TEAM_MEMBER VALUES(52, 'Cathy', 'Y', 'Yorson', 'Jacksonville Jaguars');
INSERT INTO TEAM_MEMBER VALUES(53, 'Yor', 'O', 'Myson', 'Jacksonville Jaguars');
INSERT INTO TEAM_MEMBER VALUES(54, 'Dady', 'K', 'Jewy', 'Jacksonville Jaguars');
INSERT INTO TEAM_MEMBER VALUES(55, 'Dewey', null, 'First', 'Jacksonville Jaguars');

INSERT INTO TEAM_MEMBER VALUES(56, 'Trope', 'T', 'Mon', 'Tennessee Titans');
INSERT INTO TEAM_MEMBER VALUES(57, 'Moonson', 'E', 'Wacky', 'Tennessee Titans');
INSERT INTO TEAM_MEMBER VALUES(58, 'Benie', 'B', 'Benben', 'Tennessee Titans');
INSERT INTO TEAM_MEMBER VALUES(59, 'James', 'W', 'Jameson', 'Tennessee Titans');
INSERT INTO TEAM_MEMBER VALUES(60, 'Elvens', 'I', 'Ellenie', 'Tennessee Titans');

INSERT INTO TEAM_MEMBER VALUES(61, 'Ellen', 'A', 'Mounty', 'Denver Broncos');
INSERT INTO TEAM_MEMBER VALUES(62, 'Truse', 'B', 'Levy', 'Denver Broncos');
INSERT INTO TEAM_MEMBER VALUES(63, 'Joh', 'B', 'Devy', 'Denver Broncos');
INSERT INTO TEAM_MEMBER VALUES(64, 'Goh', 'B', 'Mavy', 'Denver Broncos');
INSERT INTO TEAM_MEMBER VALUES(65, 'Deku', 'B', 'Ovy', 'Denver Broncos');

INSERT INTO TEAM_MEMBER VALUES(66, 'Oliver', 'A', 'Mounty', 'Kansas City Chiefs');
INSERT INTO TEAM_MEMBER VALUES(67, 'Penny', 'E', 'Willy', 'Kansas City Chiefs');
INSERT INTO TEAM_MEMBER VALUES(68, 'Granny', 'R', 'Ceil', 'Kansas City Chiefs');
INSERT INTO TEAM_MEMBER VALUES(69, 'Salley', 'T', 'Cell', 'Kansas City Chiefs');
INSERT INTO TEAM_MEMBER VALUES(70, 'Macbethy', 'J', 'Morson', 'Kansas City Chiefs');

INSERT INTO TEAM_MEMBER VALUES(71, 'Grand', null, 'Cool', 'Las Vegas Raiders');
INSERT INTO TEAM_MEMBER VALUES(72, 'Nelson', null, 'Watson', 'Las Vegas Raiders');
INSERT INTO TEAM_MEMBER VALUES(73, 'Nelly', null, 'Kanberrry', 'Las Vegas Raiders');
INSERT INTO TEAM_MEMBER VALUES(74, 'Lola', null, 'Anchor', 'Las Vegas Raiders');
INSERT INTO TEAM_MEMBER VALUES(75, 'Villy', null, 'Lee', 'Las Vegas Raiders');

INSERT INTO TEAM_MEMBER VALUES(76, 'Madison', 'Z', 'Bruny', 'Los Angeles Chargers');
INSERT INTO TEAM_MEMBER VALUES(77, 'Yeeson', 'Z', 'Kill', 'Los Angeles Chargers');
INSERT INTO TEAM_MEMBER VALUES(78, 'Pellie', 'Z', 'Poeopoe', 'Los Angeles Chargers');
INSERT INTO TEAM_MEMBER VALUES(79, 'Queen', 'Z', 'Eiyo', 'Los Angeles Chargers');
INSERT INTO TEAM_MEMBER VALUES(80, 'Yoyo', 'AZ', 'Lass', 'Los Angeles Chargers');

INSERT INTO TEAM_MEMBER VALUES(82, 'George', 'M', 'McCane', 'Dallas Cowboys');
INSERT INTO TEAM_MEMBER VALUES(83, 'Peter', 'V', 'Peterson', 'Dallas Cowboys');
INSERT INTO TEAM_MEMBER VALUES(84, 'Francis', null, 'Penton', 'Dallas Cowboys');
INSERT INTO TEAM_MEMBER VALUES(85, 'Samus', 'L', 'Jackson', 'Dallas Cowboys');
INSERT INTO TEAM_MEMBER VALUES(86, 'Connor', 'O', 'Brian', 'Dallas Cowboys');

INSERT INTO TEAM_MEMBER VALUES(87, 'Steve', 'B', 'Anthony', 'New York Giants');
INSERT INTO TEAM_MEMBER VALUES(88, 'Stephen', null, 'Strange', 'New York Giants');
INSERT INTO TEAM_MEMBER VALUES(89, 'Marc', null, 'Wahlberg', 'New York Giants');
INSERT INTO TEAM_MEMBER VALUES(90, 'Daniel', null , 'Son', 'New York Giants');
INSERT INTO TEAM_MEMBER VALUES(91, 'Park', 'V', 'Choi', 'New York Giants');

INSERT INTO TEAM_MEMBER VALUES(92, 'Arthur', null, 'John', 'Philadelphia Eagles');
INSERT INTO TEAM_MEMBER VALUES(93, 'Satoshi', null, 'Ash', 'Philadelphia Eagles');
INSERT INTO TEAM_MEMBER VALUES(94, 'Cane', 'B', 'Johnson', 'Philadelphia Eagles');
INSERT INTO TEAM_MEMBER VALUES(95, 'Isaac', 'J', 'Newton', 'Philadelphia Eagles');
INSERT INTO TEAM_MEMBER VALUES(96, 'Mark', 'V', 'Brown', 'Philadelphia Eagles');

INSERT INTO TEAM_MEMBER VALUES(97, 'Richard', 'M', 'Brown', 'Washington Commanders');
INSERT INTO TEAM_MEMBER VALUES(98, 'Ricky', 'V', 'Hernando', 'Washington Commanders');
INSERT INTO TEAM_MEMBER VALUES(99, 'Andy', 'C', 'Davis', 'Washington Commanders');
INSERT INTO TEAM_MEMBER VALUES(100, 'Wade', null , 'Wilson', 'Washington Commanders');
INSERT INTO TEAM_MEMBER VALUES(101, 'Smith', 'O', 'Depp', 'Washington Commanders');

INSERT INTO TEAM_MEMBER VALUES(102, 'Zack', 'S', 'Scuderi', 'Chicago Bears');
INSERT INTO TEAM_MEMBER VALUES(103, 'Zachary', 'J', 'Taylor', 'Chicago Bears');
INSERT INTO TEAM_MEMBER VALUES(104, 'William', 'M', 'Hartman', 'Chicago Bears');
INSERT INTO TEAM_MEMBER VALUES(105, 'Sam', 'O', 'Samson', 'Chicago Bears');
INSERT INTO TEAM_MEMBER VALUES(106, 'Lee', 'W', 'Jones', 'Chicago Bears');

INSERT INTO TEAM_MEMBER VALUES(107, 'Tony', null, 'Smith', 'Detroit Lions');
INSERT INTO TEAM_MEMBER VALUES(108, 'Martin', 'L', 'Sanchez', 'Detroit Lions');
INSERT INTO TEAM_MEMBER VALUES(109, 'Paul', 'O', 'White', 'Detroit Lions');
INSERT INTO TEAM_MEMBER VALUES(110, 'Harry', 'H', 'Harris', 'Detroit Lions');
INSERT INTO TEAM_MEMBER VALUES(111, 'Louis', null, 'Moore', 'Detroit Lions');

INSERT INTO TEAM_MEMBER VALUES(112, 'Peter', 'M', 'Parker', 'Green Bay Packers');
INSERT INTO TEAM_MEMBER VALUES(113, 'Pete', 'S', 'John', 'Green Bay Packers');
INSERT INTO TEAM_MEMBER VALUES(114, 'Johnny', 'J', 'Johnson', 'Green Bay Packers');
INSERT INTO TEAM_MEMBER VALUES(115, 'Scott', null, 'King', 'Green Bay Packers');
INSERT INTO TEAM_MEMBER VALUES(116, 'Lewis', null, 'Ramirez', 'Green Bay Packers');

INSERT INTO TEAM_MEMBER VALUES(117, 'Kenneth', 'L', 'Wright', 'Minnesota Vikings');
INSERT INTO TEAM_MEMBER VALUES(118, 'Rob', 'O', 'Morris', 'Minnesota Vikings');
INSERT INTO TEAM_MEMBER VALUES(119, 'Allen', 'S', 'Green', 'Minnesota Vikings');
INSERT INTO TEAM_MEMBER VALUES(120, 'Robby', 'R', 'Rodriguez', 'Minnesota Vikings');
INSERT INTO TEAM_MEMBER VALUES(121, 'Thomas', 'T', 'Thompson', 'Minnesota Vikings');

INSERT INTO TEAM_MEMBER VALUES(122, 'Jake', 'T', 'Carter', 'Atlanta Falcons');
INSERT INTO TEAM_MEMBER VALUES(123, 'Finn', 'B', 'Young', 'Atlanta Falcons');
INSERT INTO TEAM_MEMBER VALUES(124, 'Nelson', 'P', 'Osborne', 'Atlanta Falcons');
INSERT INTO TEAM_MEMBER VALUES(125, 'Manny', 'M', 'Mitchell', 'Atlanta Falcons');
INSERT INTO TEAM_MEMBER VALUES(126, 'Harry', 'T', 'Rivera', 'Atlanta Falcons');

INSERT INTO TEAM_MEMBER VALUES(127, 'Chris', 'T', 'Christopher', 'Carolina Panthers');
INSERT INTO TEAM_MEMBER VALUES(128, 'Davy', 'D', 'Locke', 'Carolina Panthers');
INSERT INTO TEAM_MEMBER VALUES(129, 'Henry', 'A', 'Ward', 'Carolina Panthers');

INSERT INTO TEAM_MEMBER VALUES(130, 'Jose', 'W', 'Rivera', 'New Orleans Saints');
INSERT INTO TEAM_MEMBER VALUES(131, 'Joseph', 'J', 'Reed', 'New Orleans Saints');
INSERT INTO TEAM_MEMBER VALUES(132, 'Joey', 'T', 'Wood', 'New Orleans Saints');

INSERT INTO TEAM_MEMBER VALUES(133, 'Will', 'N', 'Newman', 'Tampa Bay Buccaneers');
INSERT INTO TEAM_MEMBER VALUES(134, 'Carl', 'K', 'Newton', 'Tampa Bay Buccaneers');
INSERT INTO TEAM_MEMBER VALUES(135, 'Carson', 'T', 'Cox', 'Tampa Bay Buccaneers');

INSERT INTO TEAM_MEMBER VALUES(136, 'Morgan', 'M', 'Morales', 'Arizona Cardinals');
INSERT INTO TEAM_MEMBER VALUES(137, 'Edward', 'L', 'Watson', 'Arizona Cardinals');
INSERT INTO TEAM_MEMBER VALUES(138, 'Edwin', 'T', 'Ortiz', 'Arizona Cardinals');

INSERT INTO TEAM_MEMBER VALUES(139, 'Stewart', 'T', 'Chavez', 'Los Angeles Rams');
INSERT INTO TEAM_MEMBER VALUES(140, 'Stevie', 'A', 'James', 'Los Angeles Rams');
INSERT INTO TEAM_MEMBER VALUES(141, 'Howie', 'B', 'Bowman', 'Los Angeles Rams');

INSERT INTO TEAM_MEMBER VALUES(142, 'Bruce', 'H', 'Wilson', 'San Francisco 49ers');
INSERT INTO TEAM_MEMBER VALUES(143, 'Kevin', 'O', 'Brown', 'San Francisco 49ers');
INSERT INTO TEAM_MEMBER VALUES(144, 'Brian', 'T', 'Ramirez', 'San Francisco 49ers');

INSERT INTO TEAM_MEMBER VALUES(145, 'Oscar', 'O', 'Hernandez', 'Seattle Seahawks');
INSERT INTO TEAM_MEMBER VALUES(146, 'Martin', 'T', 'Wonder', 'Seattle Seahawks');
INSERT INTO TEAM_MEMBER VALUES(147, 'Cody', 'C', 'Mills', 'Seattle Seahawks');

INSERT INTO COACH VALUES(1);
INSERT INTO PLAYER VALUES(2);
INSERT INTO PLAYER VALUES(3);
INSERT INTO PLAYER VALUES(4);
INSERT INTO PLAYER VALUES(5);

INSERT INTO COACH VALUES(6);
INSERT INTO PLAYER VALUES(7);
INSERT INTO PLAYER VALUES(8);
INSERT INTO PLAYER VALUES(9);
INSERT INTO PLAYER VALUES(10);

INSERT INTO COACH VALUES(11);
INSERT INTO PLAYER VALUES(12);
INSERT INTO PLAYER VALUES(13);
INSERT INTO PLAYER VALUES(14);
INSERT INTO PLAYER VALUES(15);

INSERT INTO COACH VALUES(16);
INSERT INTO PLAYER VALUES(17);
INSERT INTO PLAYER VALUES(18);
INSERT INTO PLAYER VALUES(19);
INSERT INTO PLAYER VALUES(20);

INSERT INTO COACH VALUES(21);
INSERT INTO PLAYER VALUES(22);
INSERT INTO PLAYER VALUES(23);
INSERT INTO PLAYER VALUES(24);
INSERT INTO PLAYER VALUES(25);

INSERT INTO COACH VALUES(26);
INSERT INTO PLAYER VALUES(27);
INSERT INTO PLAYER VALUES(28);
INSERT INTO PLAYER VALUES(29);
INSERT INTO PLAYER VALUES(30);

INSERT INTO COACH VALUES(31);
INSERT INTO PLAYER VALUES(32);
INSERT INTO PLAYER VALUES(33);
INSERT INTO PLAYER VALUES(34);
INSERT INTO PLAYER VALUES(35);

INSERT INTO COACH VALUES(36);
INSERT INTO PLAYER VALUES(37);
INSERT INTO PLAYER VALUES(38);
INSERT INTO PLAYER VALUES(39);
INSERT INTO PLAYER VALUES(40);

INSERT INTO COACH VALUES(41);
INSERT INTO PLAYER VALUES(42);
INSERT INTO PLAYER VALUES(43);
INSERT INTO PLAYER VALUES(44);
INSERT INTO PLAYER VALUES(45);

INSERT INTO COACH VALUES(46);
INSERT INTO PLAYER VALUES(47);
INSERT INTO PLAYER VALUES(48);
INSERT INTO PLAYER VALUES(49);
INSERT INTO PLAYER VALUES(50);


INSERT INTO COACH VALUES(51);
INSERT INTO PLAYER VALUES(52);
INSERT INTO PLAYER VALUES(53);
INSERT INTO PLAYER VALUES(54);
INSERT INTO PLAYER VALUES(55);

INSERT INTO COACH VALUES(56);
INSERT INTO PLAYER VALUES(57);
INSERT INTO PLAYER VALUES(58);
INSERT INTO PLAYER VALUES(59);
INSERT INTO PLAYER VALUES(60);

INSERT INTO COACH VALUES(61);
INSERT INTO PLAYER VALUES(62);
INSERT INTO PLAYER VALUES(63);
INSERT INTO PLAYER VALUES(64);
INSERT INTO PLAYER VALUES(65);

INSERT INTO COACH VALUES(66);
INSERT INTO PLAYER VALUES(67);
INSERT INTO PLAYER VALUES(68);
INSERT INTO PLAYER VALUES(69);
INSERT INTO PLAYER VALUES(70);

INSERT INTO COACH VALUES(71);
INSERT INTO PLAYER VALUES(72);
INSERT INTO PLAYER VALUES(73);
INSERT INTO PLAYER VALUES(74);
INSERT INTO PLAYER VALUES(75);

INSERT INTO COACH VALUES(76);
INSERT INTO PLAYER VALUES(77);
INSERT INTO PLAYER VALUES(78);
INSERT INTO PLAYER VALUES(79);
INSERT INTO PLAYER VALUES(80);

---------------------------------

INSERT INTO COACH VALUES(82);
INSERT INTO PLAYER VALUES(83);
INSERT INTO PLAYER VALUES(84);
INSERT INTO PLAYER VALUES(85);
INSERT INTO PLAYER VALUES(86);

INSERT INTO COACH VALUES(87);
INSERT INTO PLAYER VALUES(88);
INSERT INTO PLAYER VALUES(89);
INSERT INTO PLAYER VALUES(90);
INSERT INTO PLAYER VALUES(91);

INSERT INTO COACH VALUES(92);
INSERT INTO PLAYER VALUES(93);
INSERT INTO PLAYER VALUES(94);
INSERT INTO PLAYER VALUES(95);
INSERT INTO PLAYER VALUES(96);

INSERT INTO COACH VALUES(97);
INSERT INTO PLAYER VALUES(98);
INSERT INTO PLAYER VALUES(99);
INSERT INTO PLAYER VALUES(100);
INSERT INTO PLAYER VALUES(101);

INSERT INTO COACH VALUES(102);
INSERT INTO PLAYER VALUES(103);
INSERT INTO PLAYER VALUES(104);
INSERT INTO PLAYER VALUES(105);
INSERT INTO PLAYER VALUES(106);

INSERT INTO COACH VALUES(107);
INSERT INTO PLAYER VALUES(108);
INSERT INTO PLAYER VALUES(109);
INSERT INTO PLAYER VALUES(110);
INSERT INTO PLAYER VALUES(111);

INSERT INTO COACH VALUES(112);
INSERT INTO PLAYER VALUES(113);
INSERT INTO PLAYER VALUES(114);
INSERT INTO PLAYER VALUES(115);
INSERT INTO PLAYER VALUES(116);

INSERT INTO COACH VALUES(117);
INSERT INTO PLAYER VALUES(118);
INSERT INTO PLAYER VALUES(119);
INSERT INTO PLAYER VALUES(120);
INSERT INTO PLAYER VALUES(121);

INSERT INTO COACH VALUES(122);
INSERT INTO PLAYER VALUES(123);
INSERT INTO PLAYER VALUES(124);
INSERT INTO PLAYER VALUES(125);
INSERT INTO PLAYER VALUES(126);

INSERT INTO COACH VALUES(127);
INSERT INTO PLAYER VALUES(128);
INSERT INTO PLAYER VALUES(129);

INSERT INTO COACH VALUES(130);
INSERT INTO PLAYER VALUES(131);
INSERT INTO PLAYER VALUES(132);

INSERT INTO COACH VALUES(133);
INSERT INTO PLAYER VALUES(134);
INSERT INTO PLAYER VALUES(135);

INSERT INTO COACH VALUES(136);
INSERT INTO PLAYER VALUES(137);
INSERT INTO PLAYER VALUES(138);

INSERT INTO COACH VALUES(139);
INSERT INTO PLAYER VALUES(140);
INSERT INTO PLAYER VALUES(141);

INSERT INTO COACH VALUES(142);
INSERT INTO PLAYER VALUES(143);
INSERT INTO PLAYER VALUES(144);

INSERT INTO COACH VALUES(145);
INSERT INTO PLAYER VALUES(146);
INSERT INTO PLAYER VALUES(147);

INSERT INTO MEMBER_CONTRACT VALUES(1, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(2, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(3, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(4, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(5, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(6, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(7, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(8, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(9, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(10, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(11, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(12, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(13, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(14, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(15, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(16, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(17, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(18, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(19, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(20, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(21, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(22, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(23, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(24, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(25, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(26, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(27, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(28, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(29, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(30, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(31, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(32, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(33, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(34, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(35, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(36, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(37, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(38, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(39, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(40, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(41, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(42, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(43, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(44, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(45, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(46, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(47, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(48, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(49, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(50, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(51, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(52, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(53, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(54, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(55, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(56, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(57, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(58, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(59, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(60, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(61, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(62, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(63, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(64, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(65, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(66, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(67, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(68, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(69, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(70, 'contract4', '2000-02-10', 'active');


INSERT INTO MEMBER_CONTRACT VALUES(71, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(72, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(73, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(74, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(75, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(76, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(77, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(78, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(79, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(80, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(82, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(83, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(84, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(85, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(86, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(87, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(88, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(89, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(90, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(91, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(92, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(93, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(94, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(95, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(96, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(97, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(98, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(99, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(100, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(101, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(102, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(103, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(104, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(105, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(106, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(107, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(108, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(109, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(110, 'contract4', '2000-02-10', 'active');


INSERT INTO MEMBER_CONTRACT VALUES(111, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(112, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(113, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(114, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(115, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(116, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(117, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(118, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(119, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(120, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(121, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(122, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(123, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(124, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(125, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(126, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(127, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(128, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(129, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(130, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(131, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(132, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(133, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(134, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(135, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(136, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(137, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(138, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(139, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(140, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(141, 'contract1', '2000-01-20', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(142, 'contract2', '2000-01-15', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(143, 'contract3', '2000-01-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(144, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(145, 'contract4', '2000-02-10', 'active');

INSERT INTO MEMBER_CONTRACT VALUES(146, 'contract4', '2000-02-10', 'active');
INSERT INTO MEMBER_CONTRACT VALUES(147, 'contract4', '2000-02-10', 'active');

INSERT INTO PLAYER_SCORE VALUES(1999, 1, 1, 2, 3, 4, 5);
INSERT INTO PLAYER_SCORE VALUES(1998, 1, 1, 2, 3, 4, 5);
INSERT INTO PLAYER_SCORE VALUES(1998, 2, 1, 2, 3, 4, 5);

INSERT INTO COACH_SCORE VALUES(1997, 3, 1, 2, 3, 4, 5, 6);
INSERT INTO COACH_SCORE (c_year, cscore_id) VALUES(1995, 4);


INSERT INTO TEAM_SCORE VALUES(2000, 'Buffalo Bills', 1, 2, 3, 4, 5, 6);
INSERT INTO TEAM_SCORE VALUES(2001, 'Dallas Cowboys', 1, 2, 3, 4, 5, 6);

INSERT INTO [MATCH] VALUES(1234, 'Buffalo Bills', 'Dallas Cowboys', '2021-05-02', '6-1', 'venue1', '60%-40%', '40%-60%');
INSERT INTO [MATCH] VALUES(1235, 'Denver Broncos', 'Dallas Cowboys', '2022-05-02', null, 'venue1', '60%-40%', '40%-60%');

INSERT INTO ADMINISTRATOR VALUES('Manny', 'admin@blog.com', 'adminPassword');

INSERT INTO FAN VALUES('Manny', 'Buffalo Bills', 'Washington Commanders', 'Tenson89', 'Jesse', 'Nguyen', 'jessenguyen38@gmail.com', 'Ilovebilly');
INSERT INTO FAN VALUES(null, null, null, 'Jasontran', 'Jason', 'Tran',  'johncanther@gmail.com', 'passwordiscool');


INSERT INTO NOTIFIES VALUES(1234, 56);
INSERT INTO NOTIFIES VALUES(1235, 57);

INSERT INTO POLLS VALUES(78, 'Manny', 3600, '2000-02-28', 'Who Will Win this Match?', 10, 40, 'Buffalo Bills', 'Dallas Cowboys');

INSERT INTO PETITIONS VALUES(56, 'Manny');

INSERT INTO INTERACTS VALUES(78, 56, 1, 'Win');
INSERT INTO INTERACTS VALUES(78, 56, 2, 'Nope');
INSERT INTO INTERACTS VALUES(78, 56, 3, 'Lols');
INSERT INTO INTERACTS VALUES(78, 56, 4, 'Not happening');
INSERT INTO INTERACTS VALUES(78, 56, 5, 'Billy for the wing');
