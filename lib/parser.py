from factor import Number, Variable, Paranthesis
from functions import Function
from term import Term
from expression import Expression
from exception import InvalidFormula
class Parser:
	def __init__(self):
		self.tree=[]
		self.functions=set([])

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
		try:
			terms.append(self.takeTerm(tokens))
			while tokens.isEmpty()==False and tokens.front() in ['+','-']:
				ops.append(tokens.front())
				tokens.popFront()
				terms.append(self.takeTerm(tokens))
		except IndexError:
			raise InvalidFormula()
		return Expression(terms, ops)

	def takeTerm(self, tokens):
		factors = []
		ops = []
		try:
			factors.append(self.takeFactor(tokens))
			while tokens.isEmpty()==False and tokens.front() in ['*', '/']:
				ops.append(tokens.front())
				tokens.popFront()
				factors.append(self.takeFactor(tokens))
		except IndexError:
			raise InvalidFormula()
		return Term(factors, ops)

	def takeFactor(self, tokens):
		now = tokens.front()
		if now == '(':
			try:
				tokens.popFront()
				exp = self.takeExpression(tokens)
				tokens.popFront()
			except IndexError:
				raise InvalidFormula()
			return Paranthesis(exp)
		elif Function.isSingleParamFunction(now)==True:
			try:
				self.functions.add(now)
				tokens.popFront()
				lparan=tokens.popFront()
				exp = self.takeExpression(tokens)
				rparan=tokens.popFront()
				if (lparan=='(' and rparan==')')==False:
					raise InvalidFormula()
			except IndexError:
				raise InvalidFormula()
			return Function.determine(now, param=exp)
		elif Function.isDoubleParamFunction(now)==True:
			try:
				self.functions.add(now)
				tokens.popFront()
				lparan=tokens.popFront()	
				exp1 = self.takeExpression(tokens)
				tokens.popFront()
				exp2 = self.takeExpression(tokens)
				rparan=tokens.popFront()
				if (lparan=='(' and rparan==')')==False:
					raise InvalidFormula()
			except IndexError:
				raise InvalidFormula()
			return Function.determine(now, base=exp1, exponential=exp2)
		elif Number.isNumber(now)==True:
			tokens.popFront()
			return Number.determine(now)
		elif now == '-':
			try:
				tokens.popFront()
				fac = self.takeFactor(tokens)
				term=Term([Number(-1),fac],['*'])
				expr=Expression([term],[])
			except IndexError:
				raise InvalidFormula()
			return Paranthesis(expr)
		elif Variable.isVariable(now)==True:
			tokens.popFront()
			return Variable(now)
		else:
			raise InvalidFormula()


