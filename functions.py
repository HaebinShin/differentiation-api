from math import sin, cos, tan, exp, log
from regex import Regex
from parser import *
#import regex as Regex

class Function:
	def __init__(self, name=None, param=None, base=None, exponential=None):
		self.name=name
		self.param=param
		self.base=base
		self.exponential=exponential
		

	def __str__(self):
		if self.param!=None:
			return "%s(%s)" % (self.name, self.param)
		else:
			return "%s(%s,%s)" % (self.name, self.base, self.exponential)

	def __repr__(self):
		if self.param!=None:
			return "%s(%s)" % (self.name, self.param)
		else:
			return "%s(%s,%s)" % (self.name, self.base, self.exponential)

	def getVariables(self):
		if self.param!=None:
			return self.param.getVariables()
		else:
			return self.base.getVariables()

	def setVariable(self, variable, value):
		return self.param.setVariable(variable, value)

	@staticmethod
	def isSingleParamFunction(name):
		for now_regex in Regex.singleParamFunctions():
			if now_regex.match(name)!=None:
				return True
		return False

	@staticmethod
	def isDoubleParamFunction(name):
		for now_regex in Regex.doubleParamFunctions():
			if now_regex.match(name)!=None:
				return True
		return False

	@staticmethod
	def determine(name, param=None, base=None, exponential=None):
		sin=Regex.sin()
		cos=Regex.cos()
		tan=Regex.tan()
		exp=Regex.exp()
		pow=Regex.pow()

		if sin.match(name)!=None:
			return Sin(param)
		elif cos.match(name)!=None:
			return Cos(param)
		elif tan.match(name)!=None:
			return Tan(param)
		elif exp.match(name)!=None:
			return Exp(param)
		elif pow.match(name)!=None:
			return Pow(base, exponential)
		else:
			return None
		


class Sin(Function):
	def __init__(self, param):
		Function.__init__(self, name="sin", param=param)

	def getAnswer(self):
		return sin(self.param.getAnswer())

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Cos(self.param))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		return Term(factors,ops)


class Cos(Function):
	def __init__(self, param):
		Function.__init__(self, name="cos", param=param)

	def getAnswer(self):
		return cos(self.param.getAnswer())

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Number(-1))
		ops.append('*')
		factors.append(Sin(self.param))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		return Term(factors,ops)

class Tan(Function):
	def __init__(self, param):
		Function.__init__(self, name="tan", param=param)

	def getAnswer(self):
		return tan(self.param.getAnswer())


class Exp(Function):
	def __init__(self, param):
		Function.__init__(self, name="exp", param=param)

	def getAnswer(self):
		return exp(self.param.getAnswer())


class Pow(Function):
	def __init__(self, base, exponential):
		Function.__init__(self, name="pow", base=base, exponential=exponential)

	def getAnswer(self):
		return pow(self.base.getAnswer(), self.exponential.getAnswer())

	def setVariable(self, variable, value):
		return (self.base.setVariable(variable, value) | self.exponential.setVariable(variable, value))

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Number(self.exponential.getAnswer()))
		ops.append('*')
		factors.append(Pow(self.base, Number(self.exponential.getAnswer()-1)))
		ops.append('*')
		#factors.append(Pow(self.base.getDerivativeBy(by_variable), Number(self.exponential.getAnswer())))
		factors.append(Pow(self.base.getDerivativeBy(by_variable), Number(1)))
		print factors, ops
		return Term(factors, ops)
		#return Term([Number(self.exponential.getAnswer()), Pow(self.base.getDerivativeBy(by_variable), Number(self.exponential.getAnswer()-1))], ['*', '*'])
