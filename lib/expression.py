from factor import *
from term import Term
import ds
class Expression:
	def __init__(self, terms, ops):
		self.variables={}
		self.expressions=[]

		reduced=self.__reduceZero(terms, ops)
		_reduced=self.__reduceCoeff(reduced)
		self.expressions=_reduced


	def __str__(self):
		return "%s" % self.expressions


	def __repr__(self):
		return "%s" % self.expressions


	def __reduceZero(self, terms, ops):
		reduced=[]
		reduced.append(terms[0])
		for i in range(len(ops)):
			if ops[i]=='+' and len(reduced[-1].getVariables())==0 and eval(repr(reduced[-1].getAnswer()))==0:		
				# zero in reduced
				reduced.pop()
				reduced.append(terms[i+1])
				continue
			elif len(terms[i+1].getVariables())==0 and eval(repr(terms[i+1].getAnswer()))==0:						
				# zero now watching
				continue
			else:						
				# just push
				reduced.append(ops[i])
				reduced.append(terms[i+1])
		return reduced


	def __reduceCoeff(self, reduced):
		coeff_map={}
		last_operator='+'
		# x+x -> coeff_map[x]=2
		for term in reduced:
			if term not in ['+', '-']:
				coeff=term.getCoeff()
				without_coeff_factor=term.getWithoutCoeffFactor()
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
				if without_coeff_factor_term==None:
					key="NONE"
				else:
					key=without_coeff_factor_term.toString()

				if coeff_map.get(key)==None:
					coeff_map[key]=[eval(last_operator+repr(coeff)),without_coeff_factor]
				else:
					coeff_map[key][0]+=eval(last_operator+repr(coeff))
			else:
				last_operator=term

		faclist=coeff_map.keys()
		faclist=ds.class_sort(faclist)
		_reduced=[]

		# coeff_map[x*y*z]=2 -> 2*x*y*z
		for fac in faclist:
			to_term=[]
			to_term_ops=[]
			coeff=coeff_map[fac][0]
			real_factor=coeff_map[fac][1]
			
			to_term.append(Number(coeff))
			if len(real_factor)>0:
				to_term_ops.append('*')
			# x*y*z 
			for each_factor in real_factor:
				if each_factor in ['*', '/']:
					to_term_ops.append(each_factor)
				else:
					to_term.append(each_factor)

			if len(_reduced)>0:
					_reduced.append('+')
	
			_reduced.append(Term(to_term, to_term_ops))
		return _reduced

		
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
				reduced+=str(term.getAnswer())
		return eval(reduced)

	def getVariables(self):
		variables=set([])
		for term in self.expressions:
			if term not in ['+', '-']:
				var=term.getVariables()
				if var!=None:
					for now in var:
						variables.add(now)
		return list(variables)

	def setVariable(self, variable, value):
		is_set=False
		for term in self.expressions:
			if term not in ['+', '-']:
				is_set |= term.setVariable(variable, value)
		return is_set

	def getDerivativeBy(self, by_variable):
		deri_terms=[]
		deri_ops=[]
		for term in self.expressions:
			if term in ['+', '-']:
				deri_ops.append(term)
			else:
				deri_term, deri_op = term.getDerivativeBy(by_variable)
				for each_term in deri_term:				
					deri_terms.append(each_term)
				for each_op in deri_op:
					deri_ops.append(each_op)
			
		return Expression(deri_terms, deri_ops)

