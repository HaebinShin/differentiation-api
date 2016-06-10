from factor import Number, Variable, Paranthesis
from functions import Function
from term import Term
from expression import Expression
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
		#return Ast(self.tree, self.functions)
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
			#return Factor(['(',exp,')'],"paranthesis")
			#return exp	
			return Paranthesis(exp)
		#elif re.match("\d*\.\d+|\d+", now)!=None:
		elif Number.isNumber(now)==True:
			tokens.popFront()
			#return Factor(now, "number")
			#return Number(now)
			return Number.determine(now)
		elif now == '-':
			tokens.popFront()
			#fac = tokens.front()
			fac = self.takeFactor(tokens)
			#tokens.popFront()
			#return Factor(['-',fac], "negative")
			#return Negative(fac)
			term=Term([Number(-1),fac],['*'])
			expr=Expression([term],[])
			return Paranthesis(expr)
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


