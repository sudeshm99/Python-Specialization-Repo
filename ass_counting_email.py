import sqlite3

conn = sqlite3.connect('Countsemaildb.sqlite')## connect to the database if database not exsisting db will be created
cur = conn.cursor()#connection handler

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT,count INTEGER)')
fh=open('mbox.txt')
for line in fh:
	if not line.startswith('From: '):continue
	lineLst = line.split()
	email = lineLst[1]
	pieces = email.split('@')
	domain = pieces[1]
	print(domain)
	cur.execute('SELECT count FROM Counts WHERE org=?',(domain,))
	row = cur.fetchone()
	if row is None:
		cur.execute('INSERT INTO Counts (org,count) VALUES (?,1)',(domain,))
	else:
		cur.execute('UPDATE Counts SET count=count+1 WHERE org=?',(domain,))
	conn.commit()

