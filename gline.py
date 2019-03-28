import sqlite3
import time
import zlib

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

# get all sender with id put into dic
cur.execute('SELECT id, sender FROM Senders')
senders = dict()
for message_row in cur :
    senders[message_row[0]] = message_row[1]

# select * from massage put it into a dic as tuples
cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
messages = dict()
for message_row in cur :
    messages[message_row[0]] = (message_row[1],message_row[2],message_row[3],message_row[4])

#print count of emails and senders
print("Loaded messages=",len(messages),"senders=",len(senders))

#get send org count and put into a dic
sendorgs = dict()
for (message_id, message) in list(messages.items()):
    sender = message[1]
    pieces = senders[sender].split("@")
    if len(pieces) != 2 : continue
    dns = pieces[1]
    sendorgs[dns] = sendorgs.get(dns,0) + 1

# sort org dic and pull out top 10
orgs = sorted(sendorgs, key=sendorgs.get, reverse=True)
orgs = orgs[:10]
print("Top 10 Organizations")
print(orgs)

counts = dict()
months = list()
# cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
#get msg and id
for (message_id, message) in list(messages.items()):
    sender = message[1]#sender email
    pieces = senders[sender].split("@")#get email pieces
    if len(pieces) != 2 : continue
    dns = pieces[1]# get org domain
    if dns not in orgs : continue# org domian is not in orgs list continue
    month = message[3][:4]# get year and month
    print(month)
    if month not in months : months.append(month)# new month is not in months list put it into counts dic key as tuple
    key = (month, dns)# get count dic key as month and org domian tuple
    counts[key] = counts.get(key,0) + 1# put it into counts

months.sort()
# print counts
# print months

fhand = open('gline.js','w')
fhand.write("gline = [ ['Month'")
for org in orgs:
    fhand.write(",'"+org+"'")
fhand.write("]")

for month in months:
    fhand.write(",\n['"+month+"'")
    for org in orgs:
        key = (month, org)
        val = counts.get(key,0)
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to gline.js")
print("Open gline.htm to visualize the data")
