import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

##-------------------create database and tables---------------------------------


conn = sqlite3.connect('spider.sqlite')#create spider database
cur = conn.cursor()#db handler

cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
    error INTEGER, old_rank REAL, new_rank REAL)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Links
    (from_id INTEGER, to_id INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Webs (url TEXT UNIQUE)''')#url table

##---------------------------------------enter new url to db if new url are not exsisting in the db-----------------------------------------------

cur.execute('''SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1''')
row = cur.fetchone()

if row is not None:
	print('Restarting existing crawl.  Remove spider.sqlite to start a fresh crawl.')
else:
    starturl = input('Enter now url or enter:')
    if len(starturl)<1 : starturl = 'http://www.dr-chuck.com/'
    if starturl.endswith('/') : starturl = starturl[:-1]
    web = starturl
    if starturl.endswith('.html') or starturl.endswith('.htm'):
	    pos = starturl.rfind('/')
	    web = starturl[:pos]

    if len(web) > 1 :
        cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES ( ? )', ( web, ) )
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( starturl, ) )
        conn.commit()

##----------------------------------------------select all urls form db and add to a list---------------------------------------------

cur.execute('''SELECT url FROM Webs''')
webs = list()
for row in cur:
    webs.append(str(row[0]))

print(webs)

many = 0
while True:
	##--------------------------------get url of unritrived pages-------------------------------------------------
    if many<1:
        sval = input('How many pages:')
        if len(sval)<1:break
        try:
	        many = int(sval)
        except:
	        print('Please enter correct page number')
	        break
    many-=1
    cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
    try:
        row = cur.fetchone()
        page_id = row[0]
        page_url = row[1]
    except:
	    print('Not unritrivaled pages found')
	    many = 0
	    break
    print(page_id, page_url, end=' ')

	# If we are ritriving a page there should not be links from same page
    cur.execute('DELETE from Links WHERE from_id=?', (page_id, ) )
    #-----------------------------get data from internate-------------------------------------
    try:
        document = urlopen(page_url, context=ctx)
        html = document.read()
        #---------------if page return error ----------------------
        if document.getcode() != 200:
            print("Error on page",document.getcode())
       	    cur.execute('UPDATE Pages SET error = ? WHERE url = ?',(document.getcode(),page_url))
       	    continue
       	# if page type is not html and it is png or something else 
       	if 'text/html' != document.info().get_content_type():
            print("Ignore non text/html page")
            cur.execute('DELETE FROM Pages WHERE url=?', ( page_url, ) )
            cur.execute('UPDATE Pages SET error=0 WHERE url=?', (page_url, ) )
            conn.commit()
            #print('many',str(many))
            continue
        print('('+str(len(html))+')', end=' ')
        # convert html string page to html objects tree
        soup = BeautifulSoup(html, "html.parser")
    #key board interrupt
    except KeyboardInterrupt:
    	print('')
    	print('Program interrupt by user')
    	break
    #any other exception
    except:
        print("Unable to retrieve or parse page")
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (page_url, ) )
        conn.commit()
        #print('many',str(many))
        continue
    #---------------------------------- insert data into db--------------------------        		
    cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( page_url, ) )
    cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), page_url ) )
    conn.commit()
    
	# retrive all ancher tags
    tags = soup('a')
    count = 0
    for tag in tags:
        href = tag.get('href',None)
        if href is None:continue
        #resolve retrvie reference like "/contact"
        up = urlparse(href)
        print(up)
        if len(up.scheme)<1:
            href = urljoin(page_url,href)
        ipos = href.find('#')
        if ipos>1:href=href[:ipos]
        if href.endswith('.jpg') or href.endswith('.png') or href.endswith('.gif'):continue
        if href.endswith('/'):href = href[:-1]
        if ( len(href) < 1 ) : continue

        # check if url is exsisiting in the webs table

        found = False
        for web in webs:
            if href.startswith(web):
                found = True
                break
        if not found:continue
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( href, ) )
        count = count + 1
        conn.commit()        
        
        cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', ( href, ))
        try:
            row = cur.fetchone()
            toid = row[0]
        except:
            print('Could not retrieve id')
            continue
        # print fromid, toid
        cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( page_id, toid ) )


    print(count)

cur.close()        




