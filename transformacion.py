class Transformacion(object):
	def __init__(self, qFrom,qTo,symbol):
		self.qFrom = qFrom
		self.qTo = qTo
		self.symbol = symbol
	def __str__(self):
		return "q"+str(self.qFrom) + " -> " + "q" + str(self.qTo) + " [label = \"" + self.symbol + "\"];"

	def pasos_limpios(self):
		return str(self.qFrom) + "," + self.symbol + ","  + str(self.qTo)