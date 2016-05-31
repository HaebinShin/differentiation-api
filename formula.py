from tokenizer import Tokenizer
from parser import *

class Formula:
	def __init__(self, equation):
		self.formula=equation

		tker=Tokenizer()
		tokens=tker.tokenize(equation)
		
		p=Parser()
		ast=p.parse(tokens)

		self.parse_tree = ast.getTree()
		self.variables  = ast.getVariables()
		self.functions  = ast.getFunctions()
		
		self.value={}
		

	def __str__(self):
		return "%s" % self.formula

	def notation(self):
		return self.formula

	def setVariable(self, symbol, value):
		self.value[symbol]=value

	def parseTree(self):
		return self.parse_tree


	def derivative(self):
		return self.__diff(self.parse_tree)

	def __diff(self, node):
		result=[]
		tree=eval(repr(node))
		#print "in diff type parsetree : ", type(tree)
		for node in tree:
		#	print "nownode : ", node
			if type(node)==list:
				result.append(self.__diff(node))
			elif node=='x':					# symbol
				return Factor(1, "number")
			elif node in ['+', '-', '*', '/']:		# operators
				result.append(node)
		#		print "operator position : ", result
			elif re.match("\d*\.\d+|\d+", node)!=None:
				return Factor(None, "none")
			else:						# parenthesis
				result.append(node)	
		#print result
		return result

	def getAnswer(self):
		for variable in self.variables:
			if self.__isInitVariable(variable)==False:
				return "error - not initialize variable"
		return self.__calc(self.parse_tree)

	def __calc(self, node):
		node_value=""
		node_function=None
		tree=eval(repr(node))
		for node in tree:
			print "node : ", node
			if type(node)==list:
				#calced=self.__calc(node)
				node_value=node_value+self.__calc(node)
			elif type(node)==dict:
				if node.get('variable')!=None:
					node_value=self.value[node['variable']]
					break
				elif node.get('function')!=None:
					node_function=node.get('function')
				elif node.get('number')!=None:
					node_value=node['number']
					break
			else:
				node_value=node_value+node
		print "node_value : ", node_value
		return str(eval(str(node_value)))
			

				
		


	def __isInitVariable(self, variable):
		if self.value.get(variable)==None:
			return False
		else:
			return True

	def getVariables(self):
		return self.variables

	def getFunctions(self):
		return self.functions


if __name__=="__main__":
	#f=Formula("x*(2+1)-y")
	f=Formula("x+sin(x+cos(x))+(x+x)")
	print f.notation()
	print f.parseTree()
	#print f.derivative()
	f.setVariable("x", 4)
	f.setVariable("y", 10)
	print f.getAnswer()



'''
f=Formula("x+y+1")
f.setVariable("x", 1)
f.getAnswer()
	-> error : not initialize variable
f.setVariable("y", 2)
f.getAnswer()
	-> 4
f.derivate()

f.partialDerivate("x")
f.partialDerivate("y")
'''
