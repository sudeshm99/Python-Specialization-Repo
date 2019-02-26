import urllib.request, urllib.parse, urllib.error
fh= urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
dic=dict()
for l in fh:
	line=l.decode().split()
	for word in line:
		dic[word]=dic.get(word,0)+1
print(dic)
