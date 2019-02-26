import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url=' http://py4e-data.dr-chuck.net/comments_195304.html'
fh= urllib.request.urlopen(url,context=ctx).read()
soup=BeautifulSoup(fh,'html.parser')
tags=soup('span')
sumofVal=0
for tag in tags:
	val=int(tag.contents[0])
	sumofVal+=val
print(sumofVal)