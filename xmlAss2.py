import urllib.request, urllib.parse, urllib.error
import ssl
import xml.etree.ElementTree as ET 

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

sumVal=0
url='http://py4e-data.dr-chuck.net/comments_195306.xml'
fh=urllib.request.urlopen(url,context=ctx)
data=''''''
for f in fh:
	data+=f.decode()
tree=ET.fromstring(data)
comments=tree.findall('comments/comment')
for comment in comments:
	count=comment.find('count').text
	sumVal+=int(count)
print(sumVal)	