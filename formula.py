from tokenizer import Tokenizer
from parser import *

class Formula:
	def __init__(self, equation):
		self.formula=equation

		tker=Tokenizer()
		tokens=tker.tokenize(equation)
		
		p=Parser()
		self.parse_tree=p.parse(tokens)

	def __str__(self):
		return "%s" % self.formula

	def notation(self):
		return self.formula

	def parseTree(self):
		return self.parse_tree

	def derivative(self):
		return self.__diff(self.parse_tree)

	def __diff(self, node):
		result=[]
		tree=eval(repr(node))
		#print "in diff type parsetree : ", type(tree)
		for node in list(tree):
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
		pass

	def getSymbols(self):
		pass

	def getFunctions(self):
		pass


if __name__=="__main__":
	f=Formula("x*(2+1)")
	print f.notation()
	print f.parseTree()
	print f.derivative()
