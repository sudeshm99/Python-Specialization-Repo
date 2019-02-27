import urllib.request, urllib.parse, urllib.error
import json

serviceurl="https://maps.googleapis.com/maps/api/geocode/json?"

while True:
	address = input("Enter the address: ")
	if len(address)<1:
		break
	url=serviceurl+urllib.parse.urlencode({"address": address})
	print("Retreving url: "+url)
	url_handler=urllib.request.urlopen(url)
	data=url_handler.read().decode()
	print("Resived ",len(data),"charactors")
	try:
		js=json.loads(data)
	except:
		js=None
	
	if not js or 'status' not in js or js['status']!='OK':
		print("fialer to resive ===============")
		print(data)
		continue
	print("resive data")
	print(jason.dumps(js, indent=4))
	

