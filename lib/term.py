from factor import Number, Variable
import functions as func
import ds
class Term:
	def __init__(self, factors, ops):

		self.factors=factors
		self.ops=ops

			
		for i in range(len(self.factors)):
			if self.factors[i].getType()=="function":
				if self.factors[i].getName()=="log":
					if self.factors[i].getBase().getType()=="number" and self.factors[i].getExponential().getType()=="number" and str(self.factors[i].getBase().getAnswer())==str(self.factors[i].getExponential().getAnswer()):
						self.factors[i]=Number(1)
					elif self.factors[i].getExponential().getType()=="number" and self.factors[i].getExponential().getAnswer()==1:
						self.factors[i]=Number(0)
				elif self.factors[i].getName()=="pow":
					if self.factors[i].getBase().getType()=="number" and self.factors[i].getBase().getAnswer()==0:
						self.factors[i]=Number(0)
					elif self.factors[i].getExponential().getType()=="number" and self.factors[i].getExponential().getAnswer()==0:
						self.factors[i]=Number(1)


		reduced=self.__reduceZeroOne(factors, ops)

		self.terms=[]

		_reduced, coeff=self.__reduceCoeff(reduced)
		self.terms=_reduced
		self.coeff=coeff	
						

	def __str__(self):
		return "%s" % self.terms

	def __repr__(self):
		return "%s" % self.terms


	def __reduceZeroOne(self, factors, ops):
		reduced=[]

		reduced.append(factors[0])
		if len(factors[0].getVariables())==0 and eval(repr(factors[0].getAnswer()))==0:					# number 0
			reduced=[Number(0)]
		else:
			for i in range(len(ops)):
				if ops[i]=='*' and len(factors[i+1].getVariables())==0 and eval(repr(factors[i+1].getAnswer()))==0:		# number 0
					reduced=[Number(0)]
					break
				elif ops[i]=='*' and len(reduced[-1].getVariables())==0 and eval(repr(reduced[-1].getAnswer()))==1:		# number 1
					reduced.pop()
					reduced.append(factors[i+1])
					continue
				elif len(factors[i+1].getVariables())==0 and eval(repr(factors[i+1].getAnswer()))==1:					# (aa * 1) or (aa / 1)
					continue
				else:							# just push
					reduced.append(ops[i])
					reduced.append(factors[i+1])
		return reduced


	def __reduceCoeff(self, reduced):
		multiply_variable_map={}
		divide_variable_map={}
		last_operator='*'
		coeff=1
		for factor in reduced:
			if factor not in ['*', '/']:
				if len(factor.getVariables())==0:	# number
					if last_operator=='*':
						coeff*=factor.getAnswer()
					else:
						coeff/=factor.getAnswer()
				else:								# variable
					if last_operator=='*':
						exponential=multiply_variable_map.get(factor.toString())
						if exponential==None:
							multiply_variable_map[factor.toString()]=[1,factor]
						else:
							multiply_variable_map[factor.toString()][0]+=1
					else:
						exponential=divide_variable_map.get(factor.toString())
						if exponential==None:
							divide_variable_map[factor.toString()]=[1,factor]
						else:
							divide_variable_map[factor.toString()][0]+=1
			else:
				last_operator=factor
		
		# abbrevi
		for mval in multiply_variable_map.keys():
			for dval in divide_variable_map.keys():
				if mval==dval:
					multiply_variable_map[mval][0]-=1
					divide_variable_map[dval][0]-=1



		# x*x -> pow(x,2)
		multiply_variable=[]
		divide_variable=[]
		for var in multiply_variable_map.keys():
			exponential=multiply_variable_map[var][0]
			real_factor=multiply_variable_map[var][1]
			if exponential>1:
				multiply_variable.append(func.Pow(Variable(var), Number(exponential)))
			elif exponential==1:
				multiply_variable.append(real_factor)
		for var in divide_variable_map.keys():
			exponential=divide_variable_map[var][0]
			real_factor=divide_variable_map[var][1]
			if exponential>1:
				divide_variable.append(func.Pow(Variable(var), Number(exponential)))
			elif exponential==1:
				divide_variable.append(real_factor)


		multiply_variable=ds.class_sort(multiply_variable)
		divide_variable=ds.class_sort(divide_variable)

		_reduced=[]
		if (len(multiply_variable)>0 and coeff==1)==False:
			_reduced.append(Number(coeff))

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
				_reduced.append('*')
			if len(self.only_factor_list)!=0:
				self.only_factor_list.append('*')
			self.only_factor_list.append(func.Pow(var, Number(-1)))		# for avoid ambiguity coeff
			_reduced.append(var)
		return (_reduced, coeff)
	
	def getWithoutCoeffFactor(self):
		return self.only_factor_list
	
		
	def getCoeff(self):
		if len(self.only_factor_list)==0:		# constant
			return self.coeff
		else:
			return self.terms[0].getCoeff()		# 2*x*y, x*y



	def toString(self):
		string=""
		for factor in self.terms:
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
				reduced+=str(factor.getAnswer())
		return eval(reduced)

	def getVariables(self):
		variables=set([])
		for factor in self.terms:
			if factor not in ['*', '/']:
				var=factor.getVariables()
				if var!=None:
					for now in var:
						variables.add(now)
		return list(variables)

	def setVariable(self, variable, value):
		is_set=False
		for factor in self.terms:
			if factor not in ['*', '/']:
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
						deri_factors.append(func.Pow(self.factors[j+1], Number(-1)).getDerivativeBy(by_variable))
					else:
						deri_factors.append(func.Pow(self.factors[j+1], Number(-1)))
			deri_terms.append(Term(deri_factors, deri_factors_ops))
			
		return deri_terms, deri_terms_ops

