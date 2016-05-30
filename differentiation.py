import re
from parser import *

class Differentiation:
#def diff(self, parsetree):
#if b=='x':
#return singleDiff(a,b)
#return singleDiff(parsetree[0], parsetree[1])*combiDiff(parsetree[1], parsetree[2])

#	def __init__(self):
#		self.result=[]

#	def __str__(self):
#		return "%s" % self.result

#	def __repr__(self):
#		return "%s" % self.result

	def diff(self, tree):
		result=[]
		tree=eval(repr(tree))
		print "in diff type parsetree : ", type(tree)
		for node in list(tree):
			print "nownode : ", node
			if type(node)==list:
				result.append(self.diff(node))
			elif node=='x':					# symbol
				return Factor(1, "number")
			elif node in ['+', '-', '*', '/']:		# operators
				result.append(node)
				print "operator position : ", result
			elif re.match("\d*\.\d+|\d+", node)!=None:
				return Factor(None, "none")
			else:						# parenthesis
				result.append(node)	
		print result
		return result	


if __name__=="__main__":
	from tokenizer import Tokenizer
	from parser import Parser

	tker=Tokenizer()
	#tokens=tker.tokenize("x+sin(x+cos(x))+(x+x)")
	tokens=tker.tokenize("x*(2+1)")
	p=Parser()
	parsetree=p.parse(tokens)
	print "string parsetree : ", parsetree
	#print "type parsetree : ", type(repr(parsetree))
	df=Differentiation()
	diffresult=df.diff(parsetree)
	print diffresult
