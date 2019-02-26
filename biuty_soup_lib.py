import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup 
fh= urllib.request.urlopen('http://www.dr-chuck.com').read()
soup=BeautifulSoup(fh,'html.parser')
tags=soup('a')
for tag in tags:
	print(tag.get('href',None))