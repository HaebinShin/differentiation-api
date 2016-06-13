from math import sin, cos, tan, exp, log, e
from regex import Regex
from factor import *
from term import Term
from expression import Expression
from exception import NotSupportFormula

class Function(Factor):
	def __init__(self, name=None, param=None, base=None, exponential=None):
		Factor.__init__(self, param, "function")
		self.name=name
		self.param=param
		self.base=base
		self.exponential=exponential
		
		if base!=None and exponential!=None:
			if name=='pow' and len(base.getVariables())>0 and len(exponential.getVariables())>0:
				raise NotSupportFormula(self.name+"("+base.toString()+','+exponential.toString()+")")
			elif name=='log' and len(base.getVariables())>0:
				raise NotSupportFormula(self.name+"("+base.toString()+','+exponential.toString()+")")
				
		

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

	def toString(self):
		if self.param!=None:
			return self.name+'('+self.param.toString()+')'
		else:
			return self.name+'('+self.base.toString()+','+self.exponential.toString()+')'

	def getVariables(self):
		#print self.base, self.exponential
		if self.param!=None:
			return self.param.getVariables()
		elif len(self.base.getVariables())>len(self.exponential.getVariables()):
			return self.base.getVariables()
		else:
			return self.exponential.getVariables()

	def setVariable(self, variable, value):
		return self.param.setVariable(variable, value)

	def getName(self):
		return self.name

	def getParam(self):
		return self.param

	def getBase(self):
		return self.base

	def getExponential(self):
		return self.exponential

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
		csc=Regex.csc()
		sec=Regex.sec()
		cot=Regex.cot()
		exp=Regex.exp()
		pow=Regex.pow()
		log=Regex.log()

		if sin.match(name)!=None:
			return Sin(param)
		elif cos.match(name)!=None:
			return Cos(param)
		elif tan.match(name)!=None:
			return Tan(param)
		elif csc.match(name)!=None:
			return Csc(param)
		elif sec.match(name)!=None:
			return Sec(param)
		elif cot.match(name)!=None:
			return Cot(param)
		elif exp.match(name)!=None:
			return Exp(param)
		elif pow.match(name)!=None:
			return Pow(base, exponential)
		elif log.match(name)!=None:
			return Log(base, exponential)
		else:
			return None
		


class Sin(Function):
	def __init__(self, param):
		Function.__init__(self, name="sin", param=param)

	def getAnswer(self):
		try:
			return sin(self.param.getAnswer())
		except ZeroDivisionError:
			return 1e10

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Cos(self.param))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		return Paranthesis(Expression([Term(factors,ops)], []))


class Cos(Function):
	def __init__(self, param):
		Function.__init__(self, name="cos", param=param)

	def getAnswer(self):
		try:
			return cos(self.param.getAnswer())
		except ZeroDivisionError:
			return 1e10

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Number(-1))
		ops.append('*')
		factors.append(Sin(self.param))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		aa=Paranthesis(self.param.getDerivativeBy(by_variable))
		print "asdf",aa 
		a=Paranthesis(Expression([Term(factors,ops)], []))
		print "asdf ",a
		return Paranthesis(Expression([Term(factors,ops)], []))

class Tan(Function):
	def __init__(self, param):
		Function.__init__(self, name="tan", param=param)

	def getAnswer(self):
		try:
			return tan(self.param.getAnswer())
		except ZeroDivisionError:
			return 1e10

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Pow(Sec(self.param),Number(2)))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		return Paranthesis(Expression([Term(factors,ops)], []))

class Csc(Function):
	def __init__(self, param):
		Function.__init__(self, name="csc", param=param)

	def getAnswer(self):
		try:
			return 1.0/sin(self.param.getAnswer())
		except ZeroDivisionError:
			return 1e10

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Number(-1))
		ops.append('*')
		factors.append(Csc(self.param))
		ops.append('*')
		factors.append(Cot(self.param))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		return Paranthesis(Expression([Term(factors,ops)], []))

class Sec(Function):
	def __init__(self, param):
		Function.__init__(self, name="sec", param=param)

	def getAnswer(self):
		try:
			return 1.0/cos(self.param.getAnswer())
		except ZeroDivisionError:
			return 1e10

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Sec(self.param))
		ops.append('*')
		factors.append(Tan(self.param))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		return Paranthesis(Expression([Term(factors,ops)], []))

class Cot(Function):
	def __init__(self, param):
		Function.__init__(self, name="cot", param=param)

	def getAnswer(self):
		try:
			return 1.0/tan(self.param.getAnswer())
		except ZeroDivisionError:
			return 1e10

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Number(-1))
		ops.append('*')
		factors.append(Pow(Csc(self.param),Number(2)))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		return Paranthesis(Expression([Term(factors,ops)], []))

class Exp(Function):
	def __init__(self, param):
		Function.__init__(self, name="exp", param=param)

	def getAnswer(self):
		try:
			return exp(self.param.getAnswer())
		except ZeroDivisionError:
			return 1e10
	
	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Exp(self.param))
		ops.append('*')
		factors.append(Paranthesis(self.param.getDerivativeBy(by_variable)))
		return Paranthesis(Expression([Term(factors, ops)], []))


class Log(Function):
	def __init__(self, base, exponential):
		Function.__init__(self, name="log", base=base, exponential=exponential)

	def getAnswer(self):
		try:
			if self.exponential.getAnswer()>0:
				return log(self.exponential.getAnswer(), self.base.getAnswer())
		except ZeroDivisionError:
			return 1e10

	def setVariable(self, variable, value):
		return (self.base.setVariable(variable, value) | self.exponential.setVariable(variable, value))

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		factors.append(Number(1))
		ops.append('*')
		factors.append(Pow(self.exponential, Number(-1)))
		ops.append('/')
		factors.append(Log(Number(e), self.base))
		ops.append('*')
		factors.append(Paranthesis(self.exponential.getDerivativeBy(by_variable)))

		return Paranthesis(Expression([Term(factors, ops)], []))


class Pow(Function):
	def __init__(self, base, exponential):
		Function.__init__(self, name="pow", base=base, exponential=exponential)

	def getAnswer(self):
		try:
			print self.base.getAnswer(), self.exponential.getAnswer()
			return pow(self.base.getAnswer(), self.exponential.getAnswer())
		except ZeroDivisionError:
			return 1e10
		except ValueError:
			return 0

	def setVariable(self, variable, value):
		return (self.base.setVariable(variable, value) | self.exponential.setVariable(variable, value))

	def getDerivativeBy(self, by_variable):
		factors=[]
		ops=[]
		if len(self.base.getVariables())>0 and len(self.exponential.getVariables())==0:

			factors.append(Number(self.exponential.getAnswer()))
			ops.append('*')
			factors.append(Pow(self.base, Number(self.exponential.getAnswer()-1)))
			ops.append('*')
			factors.append(Pow(self.base.getDerivativeBy(by_variable), Number(1)))

		elif len(self.base.getVariables())==0 and len(self.exponential.getVariables())>0:
			
			factors.append(Log(Number(e), Number(self.base.getAnswer())))
			ops.append('*')
			factors.append(Pow(self.base, self.exponential))
			ops.append('*')
			factors.append(Paranthesis(self.exponential.getDerivativeBy(by_variable)))
		elif len(self.base.getVariables())==0 and len(self.exponential.getVariables())==0:
			factors.append(Number(0))
		return Paranthesis(Expression([Term(factors, ops)], []))


