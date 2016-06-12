from factor import Number, Variable
#from functions import Pow
import functions as func
import ds
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

		multiply_variable_map={}
		divide_variable_map={}
		last_operator='*'
		coeff=1
		#idx=0
		for factor in reduced:
			if factor not in ['*', '/']:
				print "\tfactor", factor
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
							#multiply_variable.append(factor)
							exponential=multiply_variable_map.get(factor.toString())
							if exponential==None:
								multiply_variable_map[factor.toString()]=[1,factor]
							else:
								multiply_variable_map[factor.toString()][0]+=1
						else:
							#divide_variable.append(factor)
							exponential=divide_variable_map.get(factor.toString())
							if exponential==None:
								divide_variable_map[factor.toString()]=[1,factor]
							else:
								divide_variable_map[factor.toString()][0]+=1
			else:
				last_operator=factor
			#idx+=1
		
		for mval in multiply_variable_map.keys():
			for dval in divide_variable_map.keys():
				if mval==dval:
					multiply_variable_map[mval][0]-=1
					divide_variable_map[dval][0]-=1




		#multiply_variable.sort()
		#divide_variable.sort()
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


		print "\tmultiply_var", multiply_variable
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
				print "\t\tfactor coeff 1 : ", self.terms[0]
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
						deri_factors.append(func.Pow(self.factors[j+1], Number(-1)).getDerivativeBy(by_variable))
					else:
						deri_factors.append(func.Pow(self.factors[j+1], Number(-1)))
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

			
