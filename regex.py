import re

class Regex:
	__sin=re.compile("sine?", re.I)
	__cos=re.compile("cos|cosine", re.I)
	__tan=re.compile("tan|tangent", re.I)
	__exp=re.compile("exp|exponential", re.I)
	__pow=re.compile("pow|power", re.I)
	__log=re.compile("log", re.I)

	@classmethod
	def singleParamFunctions(cls):
		 func=[]
		 func.append(cls.__sin)
		 func.append(cls.__cos)
		 func.append(cls.__tan)
		 func.append(cls.__exp)
		 return func

	@classmethod
	def doubleParamFunctions(cls):
		 func=[]
		 func.append(cls.__pow)
		 func.append(cls.__log)
		 return func
	
	@classmethod
	def sin(cls):
		return cls.__sin

	@classmethod
	def cos(cls):
		return cls.__cos

	@classmethod
	def tan(cls):
		return cls.__tan

	@classmethod
	def exp(cls):
		return cls.__exp

	@classmethod
	def pow(cls):
		return cls.__pow
	
	@classmethod
	def log(cls):
		return cls.__log
