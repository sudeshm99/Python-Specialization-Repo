import json
import sqlite3

conn = sqlite3.connect('/home/sudesh/git/Python-Specialization-Repo/db/rosterdb.sqlite')
cur = conn.cursor()

cur.executescript('''

	DROP TABLE IF EXISTS User;
	DROP TABLE IF EXISTS Course;
	DROP TABLE IF EXISTS Member;

	create table User (
		id integer not null primary key autoincrement unique,
		name text unique 
	);
	create table Course (
		id integer not null primary key autoincrement unique,
		title text unique
	);
	create table Member (
		course_id integer,
		user_id integer,
		role integer,
		primary key (user_id,course_id)
	)
	''')

fname = 'roster_data.json'
file = open(fname)
data = json.load(file)
for obj in data:
    name = obj[0]
    course = obj[1]
    role = obj[2]

    if name is None or course is None: continue

    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)',(name,))
    cur.execute('SELECT id FROM User WHERE name = ?',(name,))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)',(course,))
    cur.execute('SELECT id FROM Course WHERE title = ?',(course,))
    course_id = cur.fetchone()[0]    
    
    cur.execute('INSERT OR REPLACE INTO Member (course_id,user_id,role) VALUES (?,?,?)',(course_id,user_id,role))
    conn.commit()