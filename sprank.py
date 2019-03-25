import sqlite3

conn = sqlite3.connect('spider.sqlite')#connection to the db
cur = conn.cursor()#db handler

# Find the ids that send out page rank - we only are interested
# in pages in the SCC that have in and out links
cur.execute('''SELECT DISTINCT from_id FROM Links''')
from_ids = list()
for row in cur: 
    from_ids.append(row[0])


# Find the ids that receive page rank 
to_ids = list()#to id list
links = list()# from id to to id link list
cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')# get all distent from id and to id list
for row in cur:
    from_id = row[0]# get from id from query
    to_id = row[1]# get to id from query
    if from_id == to_id : continue# if page link to same page continue
    if from_id not in from_ids : continue#if from page not in from id list continue
    if to_id not in from_ids : continue# to page id not in from page id list continue because we dont need pages that links to pages still not retrive 
    links.append(row)# link list
    if to_id not in to_ids : to_ids.append(to_id)#create to ids list
print(from_ids)
print('-----------------')
print(to_ids)
print('-----------------')
print(links)

# Get latest page ranks for strongly connected component
prev_ranks = dict()# initiate dictionary for put page and rank
for node in from_ids:#get rank for every page in from ids list
    cur.execute('''SELECT new_rank FROM Pages WHERE id = ?''', (node, ))
    row = cur.fetchone()
    prev_ranks[node] = row[0]# create page rank array
print(prev_ranks)
sval = input('How many iterations:')
many = 1
try:
    if ( len(sval) > 0 ) : many = int(sval)
except:
    print('please enter integer number')

# Sanity check
if len(prev_ranks) < 1 : # if there no page ranking quit
    print("Nothing to page rank.  Check data.")
    quit()

# page ranking algo

for i in range(many):#?
    next_ranks = dict();# new rank dic
    total = 0.0#?
    #get previous id and rank as tuple list
    for (node, old_rank) in list(prev_ranks.items()):
        total = total + old_rank# calulate rank totle
        next_ranks[node] = 0.0# put new rank as 0
    # print total    
    print(total)