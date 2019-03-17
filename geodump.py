import sqlite3
import json
import codecs

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
#print(cur.fetchone())
fhand = codecs.open('where.js','w',"utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur:
    data = row[1].decode()
    try:
    	js = json.loads(str(data))
    	#print(js['results'])
    except:
        print('worng data format')
        continue
    if 'status' not in js or js['status'] != 'OK': continue

    lat = js['results'][0]['geometry']['location']['lat']  
    print("++++++++++++")
    lng = js['results'][0]['geometry']['location']['lng']
    if lat == 0 and lng == 0: continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'","")
    try:
        print(where, lat, lng)
        count+=1
        if count>1: fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
    	continue
fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")