import re
from functions import *
class Parser:
	def __init__(self):
		self.tree=[]
		self.variables=set([])
		self.functions=set([])

	def __str__(self):
		return "%s" % self.tree
	
	def __repr__(self):
		return "%s" % self.tree
	
	def parse(self, tokens):
		self.tree=self.takeExpression(tokens)
		return Ast(self.tree, self.variables, self.functions)
	
	def takeExpression(self, tokens):
		terms = []
		ops = []
		terms.append(self.takeTerm(tokens))
		while tokens.isEmpty()==False and tokens.front() in ['+','-']:
			ops.append(tokens.front())
			tokens.popFront()
			terms.append(self.takeTerm(tokens))
		return Expression(terms, ops)

	def takeTerm(self, tokens):
		factors = []
		ops = []
		factors.append(self.takeFactor(tokens))
		while tokens.isEmpty()==False and tokens.front() in ['*', '/']:
			ops.append(tokens.front())
			tokens.popFront()
			factors.append(self.takeFactor(tokens))
		return Term(factors, ops)

	def takeFactor(self, tokens):
		now = tokens.front()
		if now == '(':
			tokens.popFront()
			exp = self.takeExpression(tokens)
			tokens.popFront()
			#return Factor(['(',exp,')'],"paranthesis")
			#return exp	
			return Paranthesis(exp)
		elif now == '-':
			tokens.popFront()
			#fac = tokens.front()
			fac = self.takeFactor(tokens)
			#tokens.popFront()
			#return Factor(['-',fac], "negative")
			return Negative(fac)
		elif re.match("\d*\.\d+|\d+", now)!=None:
			tokens.popFront()
			#return Factor(now, "number")
			return Number(now)
		#elif re.match("sin|cos|tan|log|exp", now)!=None:
		elif Function.isSingleParamFunction(now)==True:
			self.functions.add(now)
			tokens.popFront()
			tokens.popFront()
			print tokens.front()
			exp = self.takeExpression(tokens)
			tokens.popFront()
			#return Factor([now, '(', exp, ')'], "function")
			return Function.determine(now, param=exp)
		elif Function.isDoubleParamFunction(now)==True:
			self.functions.add(now)
			tokens.popFront()
			tokens.popFront()	
			print "tokens front : ", tokens.front()
			exp1 = self.takeExpression(tokens)
			tokens.popFront()
			print "tokens front : ", tokens.front()
			exp2 = self.takeExpression(tokens)
			tokens.popFront()
			return Function.determine(now, base=exp1, exponential=exp2)
		else:
			self.variables.add(now)
			tokens.popFront()
			#return Factor(now, "variable")
			return Variable(now)


class Variable:
	def __init__(self, variable):
		self.variable=variable

		self.value=None

	def __str__(self):
		return "%s" % self.variable

	def __repr__(self):
		return "%s" % self.variable

	def getAnswer(self):
		return self.value

	def setVariable(self, variable, value):
		if self.variable==variable:		
			self.value=float(value)
			return True
		else:
			return False

class Number:
	def __init__(self, number):
		self.number=number
		

	def getAnswer(self):
		return float(self.number)


	def __str__(self):
		return "%s" % self.number

	def __repr__(self):
		return "%s" % self.number

	def setVariable(self, variable, value):
		return False


class Negative:
	def __init__(self, factor):
		self.factor=factor

	def getAnswer(self):
		return eval('-'+str(self.factor.getAnswer()))

	def __str__(self):
		return "-%s" % self.factor

	def __repr__(self):
		return "-%s" % self.factor

	def setVariable(self, variable, value):
		return self.factor.setVariable(variable, value)

class Paranthesis:
	def __init__(self, expression):
		self.expression=expression

	def getAnswer(self):
		return self.expression.getAnswer()
	
	def __str__(self):
		return "(%s)" % self.expression

	def __repr__(self):
		return "(%s)" % self.expression

	def setVariable(self, variable, value):
		return self.expression.setVariable(variable, value)

class Factor:
	def __init__(self, param, typename):
		self.factors=[]
		if type(param)==list:
			for i in range(len(param)):
				if typename=="function" and i==0:
					instruction={}
					instruction[typename]=param[i]
					self.factors.append(instruction)
				else:
					self.factors.append(param[i])

		#else:
								#self.factors.append(param)
			#instruction={}
			#instruction[typename]=param
			#self.factors.append(instruction)

	def __str__(self):
		return "%s" % self.factors
	
	def __repr__(self):
		return "%s" % self.factors

	def setVarable(self):
		return False
		

class Term:
	def __init__(self, factors, ops):
		self.factors=factors
		self.ops=ops

		self.terms=[]
		self.terms.append(factors[0])
		for i in range(len(ops)):
			self.terms.append(ops[i])
			self.terms.append(factors[i+1])

	def __str__(self):
		return "%s" % self.terms

	def __repr__(self):
		return "%s" % self.terms
	
	def getAnswer(self):
		reduced=""
		for factor in self.terms:
			if factor in ['*', '/']:
				reduced+=str(factor)
			else:
				print "aa : ", factor
				reduced+=str(factor.getAnswer())
		print "term : ", eval(reduced)
		return eval(reduced)

	def setVariable(self, variable, value):
		is_set=False
		for factor in self.terms:
			if factor not in ['*', '/']:
				print "factor : ", factor
				is_set |= factor.setVariable(variable, value)
		return is_set

	def getDerivative(self):
		deri_terms=[]
		for i in range(len(self.factors)):
			if i==0:
				self.factors[i].getDerivate()
			else:
				self.factors[j]
			for j in range(len(self.factors[1:])):
				if self.ops[j]=='*':
					if j+1==i:
						self.factors[j+1].getDerivative()
					else:
						self.factors[j+1]
				elif self.ops[j]=='/':
					if j+1==i:
						Pow(self.factors[j+1], Number(-1)).getDerivative()
					else:
						Pow(self.factors[j+1], Number(-1))

class Expression:
	def __init__(self, terms, ops):
		self.expressions=[]
		self.expressions.append(terms[0])
		for i in range(len(ops)):
			self.expressions.append(ops[i])
			self.expressions.append(terms[i+1])

	def __str__(self):
		return "%s" % self.expressions

	def __repr__(self):
		return "%s" % self.expressions

	def getAnswer(self):
		reduced=""
		for term in self.expressions:
			if term in ['+', '-']:
				reduced+=str(term)
			else:
				print "asfd : ", term
				reduced+=str(term.getAnswer())
		return eval(reduced)

	def setVariable(self, variable, value):
		is_set=False
		for term in self.expressions:
			if term not in ['+', '-']:
				is_set |= term.setVariable(variable, value)
		return is_set

	def getDerivative(self):
		deri_expressions=[]
		for term in self.expressions:
			if term in ['+', '-']:
				deri_expressions.append(term)
			else:
				deri_expressions.append(term.getDerivative())


class Ast:
	def __init__(self, tree, variables, functions):
		self.tree=tree
		self.variables=variables
		self.functions=functions

		self.setted_variable={}

	def __str__(self):
		return "tree : %s\nvariable : %s\nfunctions : %s" % (self.getTree(), self.getVariables(), self.getFunctions())
	
	def getTree(self):
		return self.tree

	def getVariables(self):
		return list(self.variables)

	def getFunctions(self):
		return list(self.functions)

	def getAnswer(self):
		for variable in self.variables:
			if self.__isInitVariable(variable)==False:
				return "error - not initialize variable"
		return self.tree.getAnswer()

	def setVariable(self, variable, value):
		#self.value[variable]=value
		if self.tree.setVariable(variable, value)==True:	
			self.setted_variable[variable]=value
			return True
		else:
			return False

	def __isInitVariable(self,variable):
		if self.setted_variable.get(variable)==None:
			return False
		else:
			return True

	def getDerivative(self):
		return self.tree.getDerivative()


if __name__ == "__main__":

	from tokenizer import Tokenizer

	tker=Tokenizer()
	tokens=tker.tokenize("x+sin(x+cos(x))+(x+x)+pow(x,z)")
	#tokens=tker.tokenize("1--(y*(x-z))")
	#tokens=tker.tokenize("x+y+sin(x+sin(z))")
	#tokens=tker.tokenize("1+2+pow(x,y)")
	#tokens=tker.tokenize("x*y/z")
	
	print tokens
#	print type(tokens)
	p=Parser()
	ast = p.parse(tokens)
	print ast
	print ast.setVariable("x", 2)
	print ast.setVariable("y", 3)
	print ast.setVariable("z", 4)
	print ast.getAnswer()

	print ast.getDerivative()

'''
c = Calculator()
c.getAnswer(ast)
'''
