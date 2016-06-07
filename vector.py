from math import sqrt
class Vector:
	def __init__(self, *args):
		self.args=[]
		if type(args[0])==list:
			self.args=args[0]
		else:
			for arg in args:
				self.args.append(arg)

	def __str__(self):
		return "%s" % self.args

	def getVector(self):
		return self.args

	def getDimension(self):
		return len(self.args)

	def getScala(self, index):
		return self.args[index]
	
	def getUnitVector(self):
		sq_sum=0
		unit_vector=[]
		for arg in self.args:
			if type(arg)==str:
				return "error - components are not number"
			sq_sum+=pow(arg, 2)
		for i in range(len(self.args)):
			unit_vector.append(self.args[i]/sqrt(sq_sum))
		return Vector(unit_vector)
	
if __name__=="__main__":
	vec=Vector(3, 4)
	print vec
	print vec.getUnitVector()
	for i in range(vec.getDimension()):
		print vec.getScala(i)
