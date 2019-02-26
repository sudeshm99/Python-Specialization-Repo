import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url=' http://py4e-data.dr-chuck.net/known_by_Ada.html'
i=0
while i<7:
	fh= urllib.request.urlopen(url,context=ctx).read()
	soup=BeautifulSoup(fh,'html.parser')
	tags=soup('a')
	tag=tags[17]
	url=tag.get('href',None)
	print(url)
	print(tag.contents[0])
	i+=1