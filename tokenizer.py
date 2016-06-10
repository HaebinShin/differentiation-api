import re

class Tokens:
	def __init__(self, tokens):
		self.arr=tokens

	def __str__(self):
		return "%s" % (self.arr)

	def __repr__(self):
		return "%s" % (self.arr)

	def popFront(self):
		return self.arr.pop(0)

	def front(self):
		return self.arr[0]

	def size(self):
		return len(self.arr)

	def isEmpty(self):
		if self.size()==0:
			return True
		else:
			return False
	

class Tokenizer:

	def __init__(self):
		self.tokens=[]

	def tokenize(self, input_string):
		input_string=input_string.replace(" ", "")
		self.tokens=re.findall("-*\d+\.\d+|-*\d+|[\+\-\*\/\(\)]|\w+|\,", input_string)
		return Tokens(self.tokens)



if __name__ == "__main__":
	tker=Tokenizer()
	tokens=tker.tokenize("xy+sin(x+cos(x))-(x+x)")
	print tokens
	tokens=tker.tokenize("2x")
	print tokens
