import sqlite3

conn = sqlite3.connect('emaildb.sqlite')##Connection to the database
cur = conn.cursor()## database handler

cur.execute('''
	DROP TABLE IF EXISTS Counts
	''')##drop if such table exsists

cur.execute('''
	CREATE TABLE Counts (email TEXT,count INTEGER)
	''')## create table

fname = input("Enter file name: ")
if len(fname) < 1: fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
	if not line.startswith('From:'):
		continue
	pieces = line.split()
	email=pieces[1]## get email from text file
	cur.execute('SELECT count FROM Counts WHERE email=?',(email,))## get each email count
	row = cur.fetchone()## featch data
	if row is None:## if email count is None enter email with 1 count to the db
		cur.execute('''INSERT INTO Counts (email,count) VALUES (?,1)''',(email,))
	else:## increse exsiting email count by 1
		cur.execute('''UPDATE Counts SET count=count+1 WHERE email=?''',(email,))
	conn.commit()##

sqlstr = "SELECT * FROM Counts ORDER BY count DESC"

for row in cur.execute(sqlstr):
	print(row)

