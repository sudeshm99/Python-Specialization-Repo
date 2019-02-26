import urllib.request, urllib.parse, urllib.error
fh= urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
for line in fh:
	print(line.decode().strip())