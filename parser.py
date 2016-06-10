import re
from functions import *
from math import e, pi
from vector import Vector
from collections import Counter
import ds
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


class Factor:
	def __init__(self, param, __type):
		self.param=param
		self.__type=__type

	def setVarable(self):
		return False
	
	def getType(self):
		return self.__type
	
	def getCoeff(self):
		return 1
	
	def getWithoutCoeffFactor(self):
		return []

		
class Variable(Factor):
	def __init__(self, variable):
		Factor.__init__(self, variable, "variable")
		self.variable=variable

		self.value=None

	def __str__(self):
		return "%s" % self.variable

	def __repr__(self):
		return "%s" % self.variable

	def getCoeff(self):
		return 1

	def toString(self):
		return self.variable

	def getAnswer(self):
		return self.value

	def getVariables(self):
		var=[]
		var.append(self.variable)
		return var

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

class Number(Factor):
	def __init__(self, number):
		Factor.__init__(self, number, "number")
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
	
	def getCoeff(self):
		return self.getAnswer()

	def toString(self):
		return str(self.number)

	def getVariables(self):
		return list()

	def setVariable(self, variable, value):
		return False

	def getDerivativeBy(self, by_variable):
		#return Term([Number(0)], [])
		return Number(0)

	def canonicalize(self):
		return self.getAnswer()

	@staticmethod
	def isNumber(token):
		e  =Regex.e()
		pi =Regex.pi()
		num=Regex.number()
		if e.match(token)==None and pi.match(token)==None and num.match(token)==None:
			return False
		else:
			return True

	@staticmethod
	def determine(token):
		rg_e  =Regex.e()
		rg_pi =Regex.pi()
		rg_num=Regex.number()
		if rg_e.match(token)!=None:
			return Number(e)
		elif rg_pi.match(token)!=None:
			return Number(pi)
		else:
			return Number(token)


class Negative(Factor):
	def __init__(self, factor):
		Factor.__init__(self, factor, factor.getType())
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
	
	def getBase(self):
		#print self.factor.getType(), self.factor.getName()
		if self.factor.getType()=="function" and (self.factor.getName()=="pow" or self.factor.getName()=="log"):
			return self.factor.getBase()
		return None
	
	def getExponential(self):
		if self.factor.getType()=="function" and (self.factor.getName()=="pow" or self.factor.getName()=="log"):
			return self.factor.getExponential()
		return None

	def getName(self):
		return self.factor.getName()
	
	def getCoeff(self):
		return self.factor.getCoeff()*-1

	def getWithoutCoeffFactor(self):
		return self.factor.getWithoutCoeffFactor()
	
	def toString(self):
		return '-'+self.factor.toString()

	def getVariables(self):
		return self.factor.getVariables()

	def setVariable(self, variable, value):
		return self.factor.setVariable(variable, value)

	def getDerivativeBy(self, by_variable=None):
		#return eval('-'+str(self.factor.getDerivativeBy(by_variable)))
		return Negative(self.factor.getDerivativeBy(by_variable))

	def canonicalize(self):
		return self.factors.canonicalize()

class Paranthesis(Factor):
	def __init__(self, expression):
		Factor.__init__(self, expression, "paranthesis")
		self.expression=expression

	def getAnswer(self):
		return self.expression.getAnswer()
	
	def __str__(self):
		return "(%s)" % self.expression

	def __repr__(self):
		return "(%s)" % self.expression

	def toString(self):
		return '('+self.expression.toString()+')'

	def getVariables(self):
		return self.expression.getVariables()

	def setVariable(self, variable, value):
		return self.expression.setVariable(variable, value)

	def getDerivativeBy(self, by_variable):
		return self.expression.getDerivativeBy(by_variable)

	def getWithoutCoeffFactor(self):
		#wcf=self.expression.getWithoutCoeffFactor()
		#if wcf!=False:
		#	return wcf
		#else:
		#	return False
		return self.expression

	def getCoeff(self):
		#return self.expression.getCoeff()
		return 1


	def canonicalize(self):
		return self.expression.canonicalize()


class Term:
	def __init__(self, factors, ops):

		self.factors=factors
		self.ops=ops

			
		for i in range(len(self.factors)):
			if self.factors[i].getType()=="function":
				print "function reduce : ", self.factors[i]
				if self.factors[i].getName()=="log":
					if self.factors[i].getBase().getType()=="number" and self.factors[i].getExponential().getType()=="number" and str(self.factors[i].getBase().getAnswer())==str(self.factors[i].getExponential().getAnswer()):
						self.factors[i]=Number(1)
					elif self.factors[i].getExponential().getType()=="number" and self.factors[i].getExponential().getAnswer()==1:
						self.factors[i]=Number(0)
				elif self.factors[i].getName()=="pow":
					print self.factors[i].getBase()
					if self.factors[i].getBase().getType()=="number" and self.factors[i].getBase().getAnswer()==0:
						self.factors[i]=Number(0)
					elif self.factors[i].getExponential().getType()=="number" and self.factors[i].getExponential().getAnswer()==0:
						self.factors[i]=Number(1)


		reduced=self.__reduceMulDiv(factors, ops)

		self.terms=[]

#		self.terms.append(factors[0])
#		if len(factors[0].getVariables())==0 and eval(repr(factors[0].getAnswer()))==0:
#			self.terms=[Number(0)]
#		else:
#			for i in range(len(ops)):
#				#if len(factors[i+1].getVariables())==0:
#					#print factors[i+1].getAnswer()
#				if ops[i]=='*' and len(factors[i+1].getVariables())==0 and eval(repr(factors[i+1].getAnswer()))==0:
#					self.terms=[Number(0)]
#					break
#				elif ops[i]=='*' and len(self.terms[-1].getVariables())==0 and eval(repr(self.terms[-1].getAnswer()))==1:
#					self.terms.pop()
#					self.terms.append(factors[i+1])
#					continue
#				elif len(factors[i+1].getVariables())==0 and eval(repr(factors[i+1].getAnswer()))==1:
#					continue
#				else:
#					self.terms.append(ops[i])
#					self.terms.append(factors[i+1])
		
	
		print "\tnow terms : ", reduced

		
		#self.coeff=dict((key, value) for key, value in Counter(reduced).iteritems())
		#print "coeff : ", self.coeff	

		multiply_variable=[]
		divide_variable=[]
		last_operator='*'
		coeff=1
		#idx=0
		for factor in reduced:
			if factor not in ['*', '/']:
				if len(factor.getVariables())==0:	# number
					#if multiply_variable!=None:
						#self.coeff[last_variable]*=factor.Answer()
						if last_operator=='*':
							coeff*=factor.getAnswer()
						else:
							coeff/=factor.getAnswer()
				else:					# variable
					#if len(multiply_variable)==0:
					#	multiply_variable.append(factor.toString())
					#else:
						if last_operator=='*':
							multiply_variable.append(factor)
						else:
							divide_variable.append(factor)
			else:
				last_operator=factor
			#idx+=1
		
		#multiply_variable.sort()
		#divide_variable.sort()
		multiply_variable=ds.class_sort(multiply_variable)
		divide_variable=ds.class_sort(divide_variable)

		print "\tin term coeff : ", coeff
		print "\tmultiply_variable : ", multiply_variable
		print "\tdivide_variable : ", divide_variable


		_reduced=[]
		if ((len(multiply_variable)>0 or len(divide_variable)>0) and coeff==1)==False:
			_reduced.append(Number(coeff))

#		mul_idx=0
#		div_idx=0
#		ops_idx=0
		self.only_factor_list=[]
		for var in multiply_variable:
			if len(_reduced)!=0:
				_reduced.append('*')
			if len(self.only_factor_list)!=0:
				self.only_factor_list.append('*')
			self.only_factor_list.append(var)
			_reduced.append(var)
		for var in divide_variable:
			if len(_reduced)!=0:
				_reduced.append('/')
			if len(self.only_factor_list)!=0:
				self.only_factor_list.append('/')
			self.only_factor_list.append(var)
			_reduced.append(var)

		
#		_reduced.append(multiply_variable[mul_idx])
#		mul_idx+=1
#		for i in range(len(multiply_variable)+len(divide_variable)+len(ops)-1):
#			if i%2==0:
#				_reduced.append(ops[ops_idx])
#				ops_idx+=1
#			else:
#				if ops[ops_idx-1]=='*':
#					_reduced.append(multiply_variable[mul_idx])
#					mul_idx+=1
#				else:
#					_reduced.append(divide_variable[div_idx])
#					div_idx+=1
#
	
		self.terms=_reduced
		self.coeff=coeff	
						
		print "\t_reduced : ", self.terms
		print "\tcoeff : ", coeff


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


	def __reduceMulDiv(self, factors, ops):
		reduced=[]

		reduced.append(factors[0])
		if len(factors[0].getVariables())==0 and eval(repr(factors[0].getAnswer()))==0:
			reduced=[Number(0)]
		else:
			for i in range(len(ops)):
				#if len(factors[i+1].getVariables())==0:
					#print factors[i+1].getAnswer()
				if ops[i]=='*' and len(factors[i+1].getVariables())==0 and eval(repr(factors[i+1].getAnswer()))==0:
					reduced=[Number(0)]
					break
				elif ops[i]=='*' and len(reduced[-1].getVariables())==0 and eval(repr(reduced[-1].getAnswer()))==1:
					reduced.pop()
					reduced.append(factors[i+1])
					continue
				elif len(factors[i+1].getVariables())==0 and eval(repr(factors[i+1].getAnswer()))==1:
					continue
				else:
					reduced.append(ops[i])
					reduced.append(factors[i+1])
		return reduced
	
	def getWithoutCoeffFactor(self):
		#if len(self.only_factor_list)==1 and self.only_factor_list[0].getType()=="paranthesis":
			#wcf=self.only_factor_list[0].getWithoutCoeffFactor()
			#if wcf!=False:
			#	return wcf
			#else:
			#	return self.only_factor_list

		return self.only_factor_list
	
		
	def getCoeff(self):
		#if len(self.only_factor_list)==1 and self.only_factor_list[0].getType()=="paranthesis":
		#	return self.only_factor_list[0].getCoeff()
		#print "self : ", self.only_factor_list
		
		
		# if only_factor_list is empty: 1(self.coeff)
		# else: 
		#    number must be front 
		# if front is number: return that number (self.terms[0].getCoeff())
		# elif front is factor which contain number: return 1(self.coeff)

		if len(self.only_factor_list)==0:
			#print "12341234", self.coeff
			return self.coeff
		else:
			#if len(self.terms[0].getWithoutCoeffFactor())==0:
				print "\t\tfactor coeff 1 : ", self.terms[0].getCoeff()
				return self.terms[0].getCoeff()
			#else:
				print "\t\tfactor coeff 2 : ", self.terms[0].getCoeff()
				return self.terms[0].getCoeff()



	def toString(self):
		string=""
		for factor in self.terms:
			#print factor
			if factor in ['*', '/']:
				string+=factor
			else:
				string+=factor.toString()
		return string
	
	def getType(self):
		_type=self.terms[0].getType()
		for fac in self.terms:
			if fac in ['*', '/'] or _type!=fac.getType():
				_type="equation"
		return _type

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
		print "deri_terms : ",deri_terms
		print "deri_terms_ops : ",deri_terms_ops
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
#		self.expressions.append(terms[0])
#		for i in range(len(ops)):
#			if ops[i]=='+' and len(self.expressions[-1].getVariables())==0 and eval(repr(self.expressions[-1].getAnswer()))==0:
#				self.expressions.pop()
#				self.expressions.append(terms[i+1])
#				continue
#			elif len(terms[i+1].getVariables())==0 and eval(repr(terms[i+1].getAnswer()))==0:
#				continue
#			else:
#				self.expressions.append(ops[i])
#				self.expressions.append(terms[i+1])

		reduced=self.__reducePlusMinus(terms, ops)

		print "reduced : ", reduced

		coeff_map={}
		plus_factors=[]
		minus_factors=[]
		last_operator='+'
		#coeff=0
		for term in reduced:
			print "expressions term : ", term
			#if Number.isNumber(str(term[0].getAnswer()))==True:
			if term not in ['+', '-']:
				#for fac in term.getOnlyFactor():
				#	print fac

				coeff=term.getCoeff()
				#varlist=term.getVariables()
				#varst=str(varlist)
				without_coeff_factor=term.getWithoutCoeffFactor()
				print "term : ",term
				print "term coeff : ",coeff
				print "term without coeff factor : ", without_coeff_factor
				without_coeff_factor_term=None
				facs=[]
				ops=[]
				if len(without_coeff_factor)!=0:
					for fac in without_coeff_factor:
						if fac not in ['*','/']:
							facs.append(fac)
						else:
							ops.append(fac)
					without_coeff_factor_term=Term(facs, ops)
				#real_term=term
				#print type(without_coeff_factor)
				#for var in varlist:
				#	varst+=str(var)
				#	print varst
				#print "in expression term : ", coeff, varst
				if without_coeff_factor_term==None:
					key="NONE"
				else:
					key=without_coeff_factor_term.toString()

				if coeff_map.get(key)==None:
					coeff_map[key]=[eval(last_operator+repr(coeff)),without_coeff_factor]
				else:
					#coeff_map[varst]+=(eval(last_operator+str(coeff)), real_term)
					coeff_map[key][0]+=eval(last_operator+repr(coeff))
			else:
				last_operator=term


		print "coeff_map : ", coeff_map	
		

		faclist=coeff_map.keys()
		#faclist.sort()
		faclist=ds.class_sort(faclist)
		_reduced=[]

		for fac in faclist:
			to_term=[]
			to_term_ops=[]
			coeff=coeff_map[fac][0]
			real_factor=coeff_map[fac][1]
			
			minus_flag=False
			if coeff<0:
				minus_flag=True
			to_term.append(Number(coeff))
			if len(real_factor)>0:
				to_term_ops.append('*')

			for each_factor in real_factor:
				#print type(each_factor)
				if each_factor in ['*', '/']:
					to_term_ops.append(each_factor)
				else:
					to_term.append(each_factor)
			#if minus_flag==True:
			#	_reduced.append('-')

			if len(_reduced)>0:
			#	if minus_flag==False:	
					_reduced.append('+')
	
			_reduced.append(Term(to_term, to_term_ops))


		self.expressions=_reduced
		print "expressions : ", self.expressions

	def __str__(self):
		return "%s" % self.expressions

	def __repr__(self):
		return "%s" % self.expressions


	def __reducePlusMinus(self, terms, ops):
		reduced=[]
		reduced.append(terms[0])
		for i in range(len(ops)):
			if ops[i]=='+' and len(reduced[-1].getVariables())==0 and eval(repr(reduced[-1].getAnswer()))==0:
				reduced.pop()
				reduced.append(terms[i+1])
				continue
			elif len(terms[i+1].getVariables())==0 and eval(repr(terms[i+1].getAnswer()))==0:
				continue
			else:
				reduced.append(ops[i])
				reduced.append(terms[i+1])
		return reduced
		
	def getWithoutCoeffFactor(self):
		if len(self.expressions)==1:
			return self.expressions[0].getWithoutCoeffFactor()
		else:
			return False

	def getCoeff(self):
		if len(self.expressions)==1:
			return self.expressions[0].getCoeff()
		else:
			return 1
	

	def toString(self):
		string=""
		for term in self.expressions:
			if term in ['+', '-']:
				string+=term
			else:
				string+=term.toString()
		return string

	def getType(self):
		_type=self.expressions[0].getType()
		for term in self.expressions:
			if term in ['+', '-'] or _type!=term.getType():
				_type="equation"
		return _type

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
				#print deri_term, deri_op
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

		self.setted_variable=dict((var, None) for var in self.variables)

	def __str__(self):
		return "tree : %s\nvariable : %s\nfunctions : %s" % (self.getTree(), self.getVariables(), self.getFunctions())

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
		return Ast(Expression(terms, terms_ops), [])



if __name__ == "__main__":

	from tokenizer import Tokenizer
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
	ast = p.parse(tokens)
	print ast
	print "AASDFASDFSADFSDFSDFSFD", ast.toString()
	print ast.setVariable("x", 2)
	#print ast.setVariable("y", 3)
	print ast.setVariable("z", 4)
	print ast.getAnswer()
	#print ast.isContinuous()
	#print ast.getGradient()
	#print ast.getDirectionalDerivative(Vector(3,4))

	deri_ast = ast.getDerivativeBy('x')
	print deri_ast
	print "AASDFASDFSADFSDFSDFSFD", deri_ast.toString()
#	print deri_ast.getSettedVariables()
#	#print deri_ast.setVariable("x", 2)
#	print deri_ast.setVariable("y", 3)
#	print deri_ast.setVariable("z", 4)
	print deri_ast.getAnswer()

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
