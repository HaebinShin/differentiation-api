import re

class Parser:
	def __init__(self):
		self.tree=[]
		self.variables=[]
		self.functions=[]

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
			return Factor(['(',exp,')'],"paranthesis")
		elif now == '-':
			tokens.popFront()
			fac = tokens.front()
			tokens.popFront()
			return Factor(['-',fac], "negative")
		elif re.match("\d*\.\d+|\d+", now)!=None:
			tokens.popFront()
			return Factor(now, "number")
		elif re.match("sin|cos|tan|log|exp", now)!=None:
			self.functions.append(now)
			tokens.popFront()
			tokens.popFront()
			exp = self.takeExpression(tokens)
			tokens.popFront()
			return Factor([now, '(', exp, ')'], "function")
		else:
			self.variables.append(now)
			tokens.popFront()
			return Factor(now, "variable")

	
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
		else:
			#self.factors.append(param)
			instruction={}
			instruction[typename]=param
			self.factors.append(instruction)

	def __str__(self):
		return "%s" % self.factors
	
	def __repr__(self):
		return "%s" % self.factors


class Term:
	def __init__(self, factors, ops):
		self.terms=[]
		self.terms.append(factors[0])
		for i in range(len(ops)):
			self.terms.append(ops[i])
			self.terms.append(factors[i+1])

	def __str__(self):
		return "%s" % self.terms

	def __repr__(self):
		return "%s" % self.terms


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

class Ast:
	def __init__(self, tree, variables, functions):
		self.tree=tree
		self.variables=variables
		self.functions=functions

	def __str__(self):
		return "%s\n%s\n%s" % (self.tree, self.variables, self.functions)
	
	def getTree(self):
		return self.tree

	def getVariables(self):
		return self.variables

	def getFuctions(self):
		return self.functions


if __name__ == "__main__":

	from tokenizer import Tokenizer

	tker=Tokenizer()
	#tokens=tker.tokenize("x+sin(x+cos(x))+(x+x)")
	#tokens=tker.tokenize("x+y")
	tokens=tker.tokenize("x+y+sin(x)")

#	print tokens
#	print type(tokens)
	p=Parser()
	ast=p.parse(tokens)
	print ast
