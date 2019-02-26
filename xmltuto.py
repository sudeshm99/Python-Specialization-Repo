import xml.etree.ElementTree as ET
data='''
<person>
	<name>
		Sudesh
	</name>
	<phone type="intl">
		+94774299424
	</phone>
	<email hide="yes"/>
</person>
'''
data2='''
<stuff>
	<users>
		<user x="2">
			<id>001</id>
			<name>Sudesh</name>
		</user>
		<user x="7">
			<id>002</id>
			<name>Madushanka</name>
		</user>
	</users>
</stuff>
'''

tree=ET.fromstring(data)
print(tree)
print('Name:',tree.find('name').text)
print('Attr:',tree.find('email').get('hide'))
print('--------------------------------------')
tree2=ET.fromstring(data2)
x=tree2.findall('users/user')
for v in x:
	print('User id',v.find('id').text)
	print('User name',v.find('name').text)
	print('Attribute:',v.get('x'))
print(x)