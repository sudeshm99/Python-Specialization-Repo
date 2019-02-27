import json

data='''{
	"name": "Sudesh",
	"phone": {
		"type": "intl",
		"number": "+94774299424"
	},
	"email": {
		"hide": "yes"
	}
}'''
info=json.loads(data)

print(info)
print(info["email"]["hide"])


data2='''
	[{
		"id": "1",
		"name": "Sudesh",
		"x": "11"
	},{
		"id": "2",
		"name": "Madu",
		"x": "22"
	}
	]
'''

info2=json.loads(data2)
for dic in info2:
	print(dic["id"])
	print(dic["name"])