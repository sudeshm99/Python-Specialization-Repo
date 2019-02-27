import urllib.request, urllib.parse, urllib.error
import json

sumofcunts=0
count=0
while True:
	inpt=input("Enter url here: ")
	if len(inpt)<1:
		break
	data=''
	try:
		fh=urllib.request.urlopen(inpt)
		data=fh.read().decode()
	except:
		print("Unknown url type",inpt)
		break
	print("Retriving from:",inpt)
	print("Retrived",len(data),"charactors")
	js=json.loads(data)
	comments=js["comments"]
	for comment in comments:
		val=int(comment["count"])
		sumofcunts+=val
		count+=1
	print("counts:",count)
	print("sum:",sumofcunts)



