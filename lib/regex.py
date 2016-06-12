import re

class Regex:
	#__special=re.compile("[`~!@#$%^&\*()\-_=\+\\|[]{};:\'\",\n.\n<>\/?]")
	__special=re.compile("[\+\-\*\/\,\.\`\~\!\@\#\$\%\^\&\(\)\_\=\?\<\>\[\]\{\}]")

	__e  =re.compile("e",re.I)
	__pi =re.compile("pi", re.I)
	__num=re.compile("-*\d*\.\d+|-*\d+", re.I)
	
	__sin=re.compile("sine?", re.I)
	__cos=re.compile("cos|cosine", re.I)
	__tan=re.compile("tan|tangent", re.I)
	__csc=re.compile("csc|cosecant", re.I)
	__sec=re.compile("sec|secant", re.I)
	__cot=re.compile("cot|cotangent", re.I)

	__exp=re.compile("exp|exponential", re.I)
	__pow=re.compile("pow|power", re.I)
	__log=re.compile("log", re.I)

	@classmethod
	def singleParamFunctions(cls):
		 func=[]
		 func.append(cls.__sin)
		 func.append(cls.__cos)
		 func.append(cls.__tan)
		 func.append(cls.__csc)
		 func.append(cls.__sec)
		 func.append(cls.__cot)
		 func.append(cls.__exp)
		 return func

	@classmethod
	def doubleParamFunctions(cls):
		 func=[]
		 func.append(cls.__pow)
		 func.append(cls.__log)
		 return func

	@classmethod
	def e(cls):
		return cls.__e

	@classmethod
	def pi(cls):
		return cls.__pi

	@classmethod
	def pi(cls):
		return cls.__pi
	
	@classmethod
	def number(cls):
		return cls.__num

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
	def csc(cls):
		return cls.__csc
	
	@classmethod
	def sec(cls):
		return cls.__sec
	
	@classmethod
	def cot(cls):
		return cls.__cot

	@classmethod
	def exp(cls):
		return cls.__exp

	@classmethod
	def pow(cls):
		return cls.__pow
	
	@classmethod
	def log(cls):
		return cls.__log

	@classmethod
	def special(cls):
		return cls.__special
