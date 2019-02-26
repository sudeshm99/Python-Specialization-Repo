import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup 
fh= urllib.request.urlopen('http://www.dr-chuck.com/page1.htm').read()
soup=BeautifulSoup(fh,'html.parser')
tags=soup('a')
for tag in tags:
	print(tag.get('href',None))