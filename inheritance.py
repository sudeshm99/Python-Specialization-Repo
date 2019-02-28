class partyAnimal:
	x = 0
	name = ""
	def __init__(self,name):
		self.name = name
		print("i am constructude my name is",name)		

	def party(self):
		self.x = self.x + 1
		print("x val:",self.x)

	def __del__(self):
		print(self.name,"is distructed x is",self.x)


class FootballFan(partyAnimal):
	points = 0
	def touchDown(self):
		self.points = self.points + 7
		self.party()
		print(self.name,"points:",self.points)

obj1=partyAnimal("Sudesh")
obj2=partyAnimal("Madu")

obj1.party()
obj1.party()
obj2.party()