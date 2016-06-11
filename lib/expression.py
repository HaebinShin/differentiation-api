from factor import *
from term import Term
import ds
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
