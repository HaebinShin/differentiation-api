from tokenizer import Tokenizer
from parser import Parser
class Formula:
	def __init__(self, expression):
		#self.expression=[]
		if type(expression)==str:
			tknr=Tokenizer()
			tokens=tknr.tokenize(expression)

			p=Parser()
			expr=p.parse(tokens)

			expression=expr
		
		self.expression=expression
		self.variables=self.expression.getVariables()
#		self.functions=functions

		self.setted_variable=dict((var, None) for var in self.variables)

	def __str__(self):
		return "tree : %s\nvariable : %s" % (self.getTree(), self.getVariables())

	def toString(self):
		return self.expression.toString()
	
	def getTree(self):
		return self.expression

	def getVariables(self):
		#if self.variables==None:
		#	return None
		#else:
		return list(self.variables)
	
	def getSettedVariables(self):
		return self.setted_variable

#	def getFunctions(self):
#		return list(self.functions)

	def getAnswer(self):
		for variable in self.variables:
			if self.__isInitVariable(variable)==False:
				return "error - not initialize variable"
		return self.expression.getAnswer()

	def setVariable(self, variable, value):
		#self.value[variable]=value
		if self.expression.setVariable(variable, value)==True:	
			self.setted_variable[variable]=value
			return True
		else:
			return False

	def __isInitVariable(self,variable):
		if self.setted_variable.get(variable)==None:
			return False
		else:
			return True

	def getDerivativeBy(self, by_variable):
		#derivatives=[]
		#if by_variable==None:
		#	for variable in self.variable:
		#		derivatives.append(self.tree.getDerivative(by_variable))
		#else:
		#return self.expression.getDerivativeBy(by_variable)
		deri_expression=self.expression.getDerivativeBy(by_variable)
		#print deri_expression
		return Formula(deri_expression)

	def isContinuous(self):
		# f(a-alpha) similar f(a+alpha)
		for variable in self.variables:
			if self.__isInitVariable(variable)==False:
				return "error - not initialize variable"

		mid=self.expression.getAnswer()
		alpha=float(0.0000001)
		tolerance=float(2)

		result=True
		for variable in self.variables:
			self.expression.setVariable(variable, self.setted_variable[variable]-alpha)
			left=self.expression.getAnswer()
			self.expression.setVariable(variable, self.setted_variable[variable]+alpha)
			right=self.expression.getAnswer()

			result&=(abs(left-mid)<tolerance and abs(mid-right)<tolerance)

			self.expression.setVariable(variable, self.setted_variable[variable])
		return result

					

	def isDerivativable(self):
		# f'(a-alpha) similar f'(a+alpha)
		if self.expression.isContinuous()!=True:
			return False

		result=True
		for variable in self.variables:
			derivate=self.expression.getDerivativeBy(variable)
			derivate.setVariable(variable, self.setted_variable[variable])
			result&=derivate.isContinue()
		return result
			


	def getGradient(self):
		vec_list=[]
		print "QWER",self.variables
		for variable in self.variables:
			vec_list.append(self.expression.getDerivativeBy(variable))
		return Vector(vec_list)
	
	def getDirectionalDerivative(self, vector):
		grad_vec=self.getGradient()
		print "asdf", grad_vec
		unit_vec=vector.getUnitVector()

		if grad_vec.getDimension()!=unit_vec.getDimension():
			return "error - not same dimension"
		
		terms=[]
		terms_ops=[]
		for i in range(grad_vec.getDimension()):
			factors=[]
			factors_ops=[]
		
			expression=grad_vec.getScala(i)
			factors.append(Number(unit_vec.getScala(i)))
			factors_ops.append('*')
			factors.append(Paranthesis(expression))
			terms.append(Term(factors, factors_ops))

		for i in range(len(terms)-1):
			terms_ops.append('+')
		return Formula(Expression(terms, terms_ops))



if __name__ == "__main__":


	#import re
	#from functions import *
	#from math import e, pi
	#from vector import Vector
	#from collections import Counter
	#import ds

	#import pdb; pdb.set_trace()
	tker=Tokenizer()
	#tokens=tker.tokenize("x+sin(x+cos(x))+(x+x)")
	tokens=tker.tokenize("x+sin(x+cos(x))+(x+x)+z*(x)*(y)")
	#tokens=tker.tokenize("x+cos(x)")
	#tokens=tker.tokenize("x+sin(x+x)+pow(2*x,2)")
	#tokens=tker.tokenize("1--(y*(x-z))")
	#tokens=tker.tokenize("x+y+sin(x+sin(z))")
	#tokens=tker.tokenize("1+2+pow(2,x)")
	#tokens=tker.tokenize("1")
	#tokens=tker.tokenize("pow(2*x, 2)/x")
	#tokens=tker.tokenize("y+log(2, x)")
	#tokens=tker.tokenize("-(pow(x+x+4*x-y,2))")
	#tokens=tker.tokenize("-log(x+x+4*x-y, 2)")
	#tokens=tker.tokenize("-y+2*x+x")
	#tokens=tker.tokenize("x--x")
	#tokens=tker.tokenize("x*(x*y*-3+x*y)")
	#tokens=tker.tokenize("x+-cos(-2*x)-y-y-2*y")
	#tokens=tker.tokenize("log(e,e)")
	#tokens=tker.tokenize("2*x+sin(3*x+4*x)+x+x")
	#tokens=tker.tokenize("2*x+3*x+y+1/2*x")
	#tokens=tker.tokenize("2/z*x/3*y+x/y*z+z/y*x")


	
	print tokens
#	print type(tokens)
	p=Parser()
	expr = p.parse(tokens)

	formula=Formula("x+sin(x+cos(x))+(x+x)+z*(x)*(y)")
	print formula
	print "AASDFASDFSADFSDFSDFSFD", formula.toString()
	print formula.setVariable("x", 2)
	#print formula.setVariable("y", 3)
	print formula.setVariable("z", 4)
	print formula.getAnswer()
	#print formula.isContinuous()
	#print formula.getGradient()
	#print formula.getDirectionalDerivative(Vector(3,4))

	deri_formula = formula.getDerivativeBy('x')
	print deri_formula
	print "AASDFASDFSADFSDFSDFSFD", deri_formula.toString()
#	print deri_formula.getSettedVariables()
#	#print deri_formula.setVariable("x", 2)
#	print deri_formula.setVariable("y", 3)
#	print deri_formula.setVariable("z", 4)
	print deri_formula.getAnswer()

'''
tker=Tokenizer()
tokens=tker.tokenize(input)

p=Parser()
expr=p.parse(tokens)

ast=Ast("asdfasdf")

ast=Ast(expr)
ast.getVariables("x", 2)
ast.getVariables("y", 2)
ast.getAnswer()

c = Calculator()
c.isContinue(expr, Coordinate)
c.isDifferential(expr, Coordinate)
c.getDerivativeBy(expr, variable)
c.getAnswer(expr, Coordinate)
c.getGradient(expr)


f=Formula("asfd")
f.isValid()
f.notation()
f.canonicalize()
f.getAnswer(Coordinate)
(Formula type)deri_formula==f.getDerivativeBy(variable)
f.getGradient()



'''
