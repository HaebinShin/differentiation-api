class Error(Exception):
	pass

class InvalidFormula(Error):
	def __str__(self):
		return "Invalid Formula"

class NotSupportFormula(Error):
	def __init__(self, formula):
		self.formula=formula

	def  __str__(self):
		return "Not support '%s'" % self.formula
