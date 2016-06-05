"""
Galois.py --- Utilities for handling Galois fields in multiple
dimensions.
"""

class GaloisArray():
	"""
	Class for a galois array, with 2^N elements.
	"""

	def __init__(self,order=None,vals=np.zeros((1,1))):
		"""
		Initialize a galois array. Optional parameters are:

		> Order : positive integer <= 16
		> vals  : numpy array
		"""
		self.order = order
		self.vals = vals

	def something(self):
		"""
		Figure this out.
		"""
		pass