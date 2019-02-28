import urllib.request, urllib.parse, urllib.error
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#api_key = False
#api_key = 'AIzaSy___IDByT70'

serviceurl="http://python-data.dr-chuck.net/geojson?"
url2="http://py4e-data.dr-chuck.net/json?"
while True:
	add=input("Enter the location: ")
	if len(add)<1:break
	parms=dict()
	parms["address"]=add
	parms["key"]=42
	url=url2+urllib.parse.urlencode(parms)
	print('Retriving from:',url)
	##fh=urllib.request.urlopne(url)
	fh = urllib.request.urlopen(url, context=ctx)
	data = fh.read().decode()
	##print(data)
	##print(type(data))
	##print("=================")
	try:
		js = json.loads(data)
	except:
		js = None
	##print(js)
	if not js or 'status' not in js or js['status'] != 'OK':
		print("========= Fialer to retrive ===========")
		print(data)
		continue
	place_id=js["results"][0]["place_id"]
	print(place_id)