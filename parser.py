import re

class Parser:
	def __init__(self):
		self.tree=[]

	def __str__(self):
		return "%s" % self.tree
	
	def __repr__(self):
		return "%s" % self.tree
	
	def parse(self, tokens):
		self.tree=self.takeExpression(tokens)
		return self.tree
	
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
			return Factor(['(',exp,')'],"paran")
		elif now == '-':
			tokens.popFront()
			fac = tokens.front()
			tokens.popFront()
			return Factor(['-',fac], "negative")
		elif re.match("\d*\.\d+|\d+", now)!=None:
			tokens.popFront()
			return Factor(now, "number")
		elif re.match("sin|cos|tan|log|exp", now)!=None:
			tokens.popFront()
			tokens.popFront()
			exp = self.takeExpression(tokens)
			tokens.popFront()
			return Factor([now, '(', exp, ')'], "trigo")
		else:
			tokens.popFront()
			return Factor(now, "symbol")

	
class Factor:
	def __init__(self, param, typename):
		self.factors=[]
		if type(param)==list:
			for i in param:
				self.factors.append(i)
		else:
			self.factors.append(param)


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


if __name__ == "__main__":

	from tokenizer import Tokenizer

	tker=Tokenizer()
	#tokens=tker.tokenize("x+sin(x+cos(x))+(x+x)")
	tokens=tker.tokenize("x+y")
#	print tokens
#	print type(tokens)
	p=Parser()
	p.parse(tokens)
	print type(p)
	print p
