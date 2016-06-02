from math import sin, cos, tan, exp, log
from regex import Regex
#import regex as Regex

class Function:
	def __init__(self, name, param):
		self.name=name
		self.param=param
	
		

	def __str__(self):
		return "%s(%s)" % (self.name, self.param)

	def __repr__(self):
		return "%s(%s)" % (self.name, self.param)
	
	def setVariable(self, variable, value):
		return self.param.setVariable(variable, value)

	@staticmethod
	def isFunction(name):
		for now_regex in Regex.functions():
			if now_regex.match(name)!=None:
				return True
		return False

	@staticmethod
	def determine(name, param):
		sin=Regex.sin()
		cos=Regex.cos()
		tan=Regex.tan()
		exp=Regex.exp()

		if sin.match(name)!=None:
			return Sin(param)
		elif cos.match(name)!=None:
			return Cos(param)
		elif tan.match(name)!=None:
			return Tan(param)
		elif exp.match(name)!=None:
			return Exp(param)
		else:
			return None
		


class Sin(Function):
	def __init__(self, param):
		Function.__init__(self, "sin", param)

	def getAnswer(self):
		print self.param
		return sin(self.param.getAnswer())


class Cos(Function):
	def __init__(self, param):
		Function.__init__(self, "cos", param)

	def getAnswer(self):
		return cos(self.param.getAnswer())


class Tan(Function):
	def __init__(self, param):
		Function.__init__(self, "tan", param)

	def getAnswer(self):
		return tan(self.param.getAnswer())


class Exp(Function):
	def __init__(self, param):
		Function.__init__(self, "exp", param)

	def getAnswer(self):
		return exp(self.param.getAnswer())
