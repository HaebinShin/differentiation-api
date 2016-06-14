from math import e, pi
from regex import Regex
class Factor:
	def __init__(self, param, __type):
		self.param=param
		self.__type=__type

	def setVarable(self):
		return False
	
	def getType(self):
		return self.__type
	
	def getCoeff(self):
		return 1
	
	def getWithoutCoeffFactor(self):
		return []

		
class Variable(Factor):
	def __init__(self, variable):
		Factor.__init__(self, variable, "variable")
		self.variable=variable

		self.value=None

	def __str__(self):
		return "%s" % self.variable

	def __repr__(self):
		return "%s" % self.variable

	def getCoeff(self):
		return 1

	def toString(self):
		return self.variable

	def getAnswer(self):
		return self.value

	def getVariables(self):
		var=[]
		var.append(self.variable)
		return var

	def setVariable(self, variable, value):
		if self.variable==variable:		
			self.value=float(value)
			return True
		else:
			return False

	def getDerivativeBy(self, by_variable):
		if self.variable==by_variable:	
			return Number(1)
		else:
			return Number(0)


	@staticmethod
	def isVariable(token):
		special=Regex.special()
		if special.match(token)==None:
			print token
			return True
		else:
			return False

class Number(Factor):
	def __init__(self, number):
		Factor.__init__(self, number, "number")
		self.number=number
		

	def getAnswer(self):
		return float(self.number)


	def __str__(self):
		if self.number==e:
			return "e"
		elif self.number==pi:
			return "pi"
		else:
			return "%s" % self.number

	def __repr__(self):
		if self.number==e:
			return "e"
		elif self.number==pi:
			return "pi"
		else:
			return "%s" % self.number
	
	def getCoeff(self):
		return self.getAnswer()

	def toString(self):
		return str(self.number)

	def getVariables(self):
		return list()

	def setVariable(self, variable, value):
		return False

	def getDerivativeBy(self, by_variable):
		return Number(0)

	@staticmethod
	def isNumber(token):
		e  =Regex.e()
		pi =Regex.pi()
		num=Regex.number()
		if e.match(token)==None and pi.match(token)==None and num.match(token)==None:
			return False
		else:
			return True

	@staticmethod
	def determine(token):
		rg_e  =Regex.e()
		rg_pi =Regex.pi()
		rg_num=Regex.number()
		if rg_e.match(token)!=None:
			return Number(e)
		elif rg_pi.match(token)!=None:
			return Number(pi)
		else:
			return Number(token)



class Paranthesis(Factor):
	def __init__(self, expression):
		Factor.__init__(self, expression, "paranthesis")
		self.expression=expression

	def getAnswer(self):
		return self.expression.getAnswer()
	
	def __str__(self):
		return "(%s)" % self.expression

	def __repr__(self):
		return "(%s)" % self.expression

	def toString(self):
		return '('+self.expression.toString()+')'

	def getVariables(self):
		return self.expression.getVariables()

	def setVariable(self, variable, value):
		return self.expression.setVariable(variable, value)

	def getDerivativeBy(self, by_variable):
		return self.expression.getDerivativeBy(by_variable)

	def getWithoutCoeffFactor(self):
		return self.expression

	def getCoeff(self):
		return 1

