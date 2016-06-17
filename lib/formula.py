from tokenizer import Tokenizer
from parser import Parser
from vector import Vector
from expression import Expression
from term import Term
from factor import Number, Paranthesis
from exception import InvalidPlotRange, InvalidVectorInput, ImaginaryValue
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as m
import sympy as sp
import re
import math


class Formula:
	def __init__(self, expression):
		if type(expression)==str or type(expression)==unicode:
			expression=str(expression)
			
			tknr=Tokenizer()
			tokens=tknr.tokenize(expression)

			p=Parser()
			expr=p.parse(tokens)

			expression=expr
		
		self.expression=expression
		self.variables=self.expression.getVariables()

		self.setted_variable=dict((var, None) for var in self.variables)

	def __str__(self):
		return "tree : %s\nvariable : %s" % (self.getTree(), self.getVariables())

	def toString(self):
		return self.expression.toString()
	
	def getTree(self):
		return self.expression

	def getVariables(self):
		return list(self.variables)
	
	def getSettedVariables(self):
		return self.setted_variable

	def getAnswer(self):
		for variable in self.variables:
			if self.__isInitVariable(variable)==False:
				return "error - not initialize variable"
		return self.expression.getAnswer()

	def setVariable(self, variable, value):
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
		deri_expression=self.expression.getDerivativeBy(by_variable)
		return Formula(deri_expression)

	def isContinuous(self):
		for variable in self.variables:
			if self.__isInitVariable(variable)==False:
				return "error - not initialize variable"

		mid=self.expression.getAnswer()
		alpha=float(0.00000001)
		tolerance=float(0.0000001)

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
		if self.expression.isContinuous()!=True:
			return False

		result=True
		for variable in self.variables:
			derivate=self.expression.getDerivativeBy(variable)
			derivate.setVariable(variable, self.setted_variable[variable])
			try:
				val=derivate.getAnswer()
				result=True
			except:
				result=False
		return result
			


	def getGradient(self):
		vec_list=[]
		for variable in self.variables:
			vec_list.append(self.expression.getDerivativeBy(variable))
		return Vector(vec_list)
	
	def getDirectionalDerivative(self, vector):
		grad_vec=self.getGradient()
		unit_vec=vector.getUnitVector()

		if grad_vec.getDimension()!=unit_vec.getDimension():
			raise InvalidVectorInput()
		
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
		return Formula(Expression(terms, terms_ops))

	def getPlotImage(self, start, end, file_name):

		var_cnt=len(self.variables)
		xs=[]
		ys=[]
		max_y=1e-20
		min_y=1e20

		max_y_limit=1000
		min_y_limit=-1000
		if var_cnt>1:
			return "error - it's not one variable function"
		for x in np.arange(start, end, math.pi/2000):
			if var_cnt==1 and self.setVariable(self.variables[0], x)==False:
				return "error"
			try:
				saved_setting=self.setted_variable
				variables=self.variables
				if len(variables)>0:
					variable=variables[0]
				else:
					variable="constant"
				self.setVariable(variable, x)

				is_continue=self.isContinuous()
				if is_continue==True:
					y=self.getAnswer()
					max_y=max(max_y, y)
					min_y=min(min_y, y)
				else:
					y=np.nan
				xs.append(x)
				ys.append(y)
			except ImaginaryValue:
				pass
		maxy=max_y
		miny=min_y


		
		plt.plot(xs, ys)
		if max_y>max_y_limit:
			max_y=max_y_limit
		if min_y<min_y_limit:
			min_y=min_y_limit
		if min_y>max_y:
			max_y=maxy
			min_y=miny
	#	print miny, maxy
		#plt.ylim(min_y, max_y)
		plt.savefig(file_name)
		plt.close()
		return True
				
	
	def getLatexString(self):
		try:
			st=self.toString()
			re_st=re.sub(r"log\((?P<base>[^,;]+),{1}(?P<exponent>.*)\)", r"log(\g<exponent>,\g<base>)", st)
			latex_string=sp.latex(sp.sympify(re_st))
		except:
			latex_string=""
		return latex_string
		

if __name__ == "__main__":


	tker=Tokenizer()
	tokens=tker.tokenize("x+y")
	#tokens=tker.tokenize("sin(x,x)")
	#tokens=tker.tokenize("x+sin(x+cos(x))+(x+x)+z*(x)*(y)")
	#tokens=tker.tokenize("x+cos(x)")
	#tokens=tker.tokenize("x+sin(x+x)+pow(2*x,2)")
	#tokens=tker.tokenize("1--(y*(x-z))")
	#tokens=tker.tokenize("x+y+sin(x+sin(z))")
	#tokens=tker.tokenize("1+2+pow(2,x)")
	#tokens=tker.tokenize("1")
	#tokens=tker.tokenize("pow(2*x, 2)/x")
	#tokens=tker.tokenize("y+log(2, x)")
	#tokens=tker.tokenize("-(pow(x+x+4*x-x,2))")
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
	p=Parser()
	expr = p.parse(tokens)

	formula=Formula(expr)
	print formula
	print formula.getVariables()
	print formula.setVariable("x", 0.5)
	print formula.setVariable("z", 4)
	print formula.getAnswer()
	#formula.getPlotImage(-1.3,1.3, 'plot.png')
	#print formula.isContinuous()
	#print formula.getGradient()
	#print formula.getDirectionalDerivative(Vector(3,4))

	deri_formula = formula.getDerivativeBy('x')
	print deri_formula
	#print deri_formula.getSettedVariables()
	#print deri_formula.setVariable("x", 2)
	#print deri_formula.setVariable("y", 3)
	#print deri_formula.setVariable("z", 4)
	print deri_formula.getAnswer()
	#deri_formula.getPlotImage(-0.3, 0.3, 'deri_plot.png')

