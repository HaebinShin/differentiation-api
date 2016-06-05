import re
from functions import *
from math import e, pi
class Parser:
	def __init__(self):
		self.tree=[]
		#self.variables=set([])
		#self.variables={}
		self.functions=set([])

	def __str__(self):
		return "%s" % self.tree
	
	def __repr__(self):
		return "%s" % self.tree
	
	def parse(self, tokens):
		self.tree=self.takeExpression(tokens)
		return Ast(self.tree, self.functions)
	
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
			#print tokens.front()
			exp = self.takeExpression(tokens)
			tokens.popFront()
			#return Factor([now, '(', exp, ')'], "function")
			return Function.determine(now, param=exp)
		elif Function.isDoubleParamFunction(now)==True:
			self.functions.add(now)
			tokens.popFront()
			tokens.popFront()	
			#print "tokens front : ", tokens.front()
			exp1 = self.takeExpression(tokens)
			tokens.popFront()
			#print "tokens front : ", tokens.front()
			exp2 = self.takeExpression(tokens)
			tokens.popFront()
			return Function.determine(now, base=exp1, exponential=exp2)
		else:
			#self.variables.add(now)
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

	def getVariables(self):
		return list(self.variable)

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

	def canonicalize(self):
		return self.getAnswer()

class Number:
	def __init__(self, number):
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

	def getVariables(self):
		return list()

	def setVariable(self, variable, value):
		return False

	def getDerivativeBy(self, by_variable):
		return Number(0)

	def canonicalize(self):
		return self.getAnswer()


class Negative:
	def __init__(self, factor):
		self.factor=factor

	def getAnswer(self):
		#print self.factor
		if self.factor.getAnswer()==None:
			return None
		else:
			return eval('-'+repr(self.factor.getAnswer()))

	def __str__(self):
		if self.factor.getVariables()!=None:
			return "-%s" % self.factor
		else:
			#return "%s" % str(eval('-'+repr(self.factor.getAnswer())))
			return "-%s" % self.factor

	def __repr__(self):
		if self.factor.getVariables()!=None:
			return "-%s" % self.factor
		else:
			#return "%s" % str(eval('-'+repr(self.factor.getAnswer())))
			return "-%s" % self.factor

	def getVariables(self):
			return self.factor.getVariables()

	def setVariable(self, variable, value):
		return self.factor.setVariable(variable, value)

	def getDerivativeBy(self, by_variable=None):
		#return eval('-'+str(self.factor.getDerivativeBy(by_variable)))
		return Negative(self.factor.getDerivativeBy(by_variable))

	def canonicalize(self):
		return self.factors.canonicalize()

class Paranthesis:
	def __init__(self, expression):
		self.expression=expression

	def getAnswer(self):
		return self.expression.getAnswer()
	
	def __str__(self):
		return "(%s)" % self.expression

	def __repr__(self):
		return "(%s)" % self.expression

	def getVariables(self):
		return self.expression.getVariables()

	def setVariable(self, variable, value):
		return self.expression.setVariable(variable, value)

	def getDerivativeBy(self, by_variable):
		return self.expression.getDerivativeBy(by_variable)

	def canonicalize(self):
		return self.expression.canonicalize()

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
		if len(factors[0].getVariables())==0 and eval(repr(factors[0].getAnswer()))==0:
			self.terms=[Number(0)]
		else:
			for i in range(len(ops)):
				#if len(factors[i+1].getVariables())==0:
					#print factors[i+1].getAnswer()
				if ops[i]=='*' and len(factors[i+1].getVariables())==0 and eval(repr(factors[i+1].getAnswer()))==0:
					self.terms=[Number(0)]
					break
				elif ops[i]=='*' and len(self.terms[-1].getVariables())==0 and eval(repr(self.terms[-1].getAnswer()))==1:
					self.terms.pop()
					self.terms.append(factors[i+1])
					continue
				elif len(factors[i+1].getVariables())==0 and eval(repr(factors[i+1].getAnswer()))==1:
					continue
				else:
					self.terms.append(ops[i])
					self.terms.append(factors[i+1])

	#	self.terms=[]
	#	if len(self.reduce_terms)!=1:
	#		for i in range(len(self.reduce_terms)):
	#			if self.reduce_terms[i]=='*':
	#				if self.reduce_terms[i+1].getVariables()==None and eval(repr(self.reduce_terms[i+1]))==1:
	#					self.terms.append(self.reduce_terms[i-1])


	#def __reduceOne(self, terms):
	#	for factor in terms:


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
				#print "aa : ", factor
				reduced+=str(factor.getAnswer())
		#print "term : ", eval(reduced)
		return eval(reduced)

	def getVariables(self):
		variables=set([])
		for factor in self.terms:
			if factor not in ['*', '/']:
				#print factor
				var=factor.getVariables()
				if var!=None:
					for now in var:
						variables.add(now)
		#if len(variables)==0:
		#	return None
		#else:
		return list(variables)

	def setVariable(self, variable, value):
		is_set=False
		for factor in self.terms:
			if factor not in ['*', '/']:
				#print "factor : ", factor
				is_set |= factor.setVariable(variable, value)
		return is_set

	def getDerivativeBy(self, by_variable):
		deri_terms=[]
		deri_terms_ops=[]
		for i in range(len(self.factors)):
			deri_factors=[]
			deri_factors_ops=[]
			if i==0:
				deri_factors.append(self.factors[0].getDerivativeBy(by_variable))
			else:
				deri_factors.append(self.factors[0])
				deri_terms_ops.append('+')
			for j in range(len(self.factors[1:])):
				deri_factors_ops.append('*')
				if self.ops[j]=='*':
					if j+1==i:
						deri_factors.append(self.factors[j+1].getDerivativeBy(by_variable))
					else:
						deri_factors.append(self.factors[j+1])
				elif self.ops[j]=='/':
					if j+1==i:
						deri_factors.append(Pow(self.factors[j+1], Number(-1)).getDerivativeBy(by_variable))
					else:
						deri_factors.append(Pow(self.factors[j+1], Number(-1)))
			deri_terms.append(Term(deri_factors, deri_factors_ops))
		
		#return Expression(deri_terms, deri_terms_ops)
		return deri_terms, deri_terms_ops

	def canonicalize(self):
		string=""
		for i in range(len(self.terms)):
			if self.terms[i]=='*':
				if self.terms[i-1].canonicalize()==1:
					string+=self.terms[i+1].canonicalize()
				elif self.terms[i+1].canonicalize()==1:
					string+=self.terms[i-1].canonicalize()
				elif self.terms[i+1].canonicalize()==0 or self.terms[i-1].canonicalize()==0:
					string+=0
			elif self.terms[i]=='/':
				if self.terms[i+1].canonicalize()==1:
					string+=self.terms[i-1].canonicalize()
				elif self.terms[i-1].canonicalize()==0:
					continue	
			string+=self.terms[i-1].canonicalize()
			string+=self.terms[i].canonicalize()
			string+=self.terms[i+1].canonicalize()
		return string

			

class Expression:
	def __init__(self, terms, ops):
		self.variables={}

		self.expressions=[]
		self.expressions.append(terms[0])
		for i in range(len(ops)):
			if ops[i]=='+' and len(self.expressions[-1].getVariables())==0 and eval(repr(self.expressions[-1].getAnswer()))==0:
				self.expressions.pop()
				self.expressions.append(terms[i+1])
				continue
			elif len(terms[i+1].getVariables())==0 and eval(repr(terms[i+1].getAnswer()))==0:
				continue
			else:
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
				#print "asfd : ", term
				reduced+=str(term.getAnswer())
		return eval(reduced)

	def getVariables(self):
		#return list(self.variables.keys())
		variables=set([])
		for term in self.expressions:
			if term not in ['+', '-']:
				var=term.getVariables()
				if var!=None:
					for now in var:
						variables.add(now)
		#if len(variables)==0:
		#	return None
		#else:
		return list(variables)

	def setVariable(self, variable, value):
		is_set=False
		for term in self.expressions:
			if term not in ['+', '-']:
				is_set |= term.setVariable(variable, value)
		return is_set

	def getDerivativeBy(self, by_variable):
		#print "expression derivativeby"
		deri_terms=[]
		deri_ops=[]
		for term in self.expressions:
			#deri_ops.append(term)
			if term in ['+', '-']:
				deri_ops.append(term)
			else:
				#print "now term in expressions : ", term
				deri_term, deri_op = term.getDerivativeBy(by_variable)
				for each_term in deri_term:				
					deri_terms.append(each_term)
				for each_op in deri_op:
					deri_ops.append(each_op)
			
			#print "deri term : ", deri_terms
			#print "deri ops  : ", deri_ops
		
		return Expression(deri_terms, deri_ops)
		#return deri_tree

	def canonicalize(self):
		pass	

class Ast:
	def __init__(self, expression, functions):
		self.expression=expression
		self.variables=expression.getVariables()
		self.functions=functions

		self.setted_variable={}

	def __str__(self):
		return "tree : %s\nvariable : %s\nfunctions : %s" % (self.getTree(), self.getVariables(), self.getFunctions())
	
	def getTree(self):
		return self.expression

	def getVariables(self):
		if self.variables==None:
			return None
		else:
			return list(self.variables)

	def getFunctions(self):
		return list(self.functions)

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
		return Ast(deri_expression, ["adsf"])

	def getGradient(self):
		pass # Vector(tree, variable)


if __name__ == "__main__":

	from tokenizer import Tokenizer

	tker=Tokenizer()
	#tokens=tker.tokenize("x+sin(x+cos(x))+(x+x)")
	#tokens=tker.tokenize("x+cos(x)")
	#tokens=tker.tokenize("x+pow(2*x,2)")
	#tokens=tker.tokenize("1--(y*(x-z))")
	#tokens=tker.tokenize("x+y+sin(x+sin(z))")
	#tokens=tker.tokenize("1+2+pow(2,x)")
	#tokens=tker.tokenize("x/z")
	#tokens=tker.tokenize("pow(2*x, 2)/x")
	tokens=tker.tokenize("y+log(2, x)")

	
	print tokens
#	print type(tokens)
	p=Parser()
	ast = p.parse(tokens)
	print ast
	print ast.setVariable("x", 2)
	#print ast.setVariable("y", 3)
	print ast.setVariable("z", 4)
	print ast.getAnswer()
	

	deri_ast = ast.getDerivativeBy('x')
	print deri_ast
	print deri_ast.setVariable("x", 2)
	print deri_ast.setVariable("y", 3)
	print deri_ast.setVariable("z", 4)
	print deri_ast.getAnswer()

'''
c = Calculator()
c.getAnswer(ast)
'''
