# __date__    = "2017.10.24"
# __author__  = "Shihao Li"
# __env__     = "Python 2.7.12 (default, Nov 19 2016, 06:48:10) | Ubuntu 16.04 LTS"

"""
each instance maintain a set of values in the database
with method of
total  - O(1)
amount - O(1)
median - O(1)
insert - O(lgn)
"""
from Queue import PriorityQueue


class record:
	def __init__(self):
		# all numbers smaller than median
		self._maxheap_   	= PriorityQueue()
		# all numbers greater than median
		self._minheap_   	= PriorityQueue()
		self._medianlow_ 	= None
		self._medianlarge_	= None
		self._sum_ 			= 0
		self._amount_ = 0

	@property
	def amount(self):
		return self._amount_


	@property
	def total(self):
		return self._sum_

	@property
	def median(self):
		if self.amount == 0:
			raise ValueError("Empty record")
		else:
			return round((self._medianlow_ + self._medianlarge_)/2.0)

	def push(self,value):
		value = float(value)
		# have even num of elements before insertion
		if self._amount_ % 2 == 0:
			# empty record
			if self._amount_ == 0:
				self._medianlow_ = self._medianlarge_ = value
			# insert current and lower, larger become median
			elif value > self._medianlarge_:
				self._minheap_.put((value, value))
				self._maxheap_.put((-self._medianlow_, self._medianlow_))
				self._medianlow_ = self._medianlarge_
			# insert current and larger, lower become median
			elif value < self._medianlow_:
				self._maxheap_.put((-value, value))
				self._minheap_.put((self._medianlarge_, self._medianlarge_))
				self._medianlarge_ = self._medianlow_
			# insert current and larger, lower become median
			else:
				self._maxheap_.put((-self._medianlow_, self._medianlow_))
				self._minheap_.put((self._medianlarge_, self._medianlarge_))
				self._medianlarge_ = self._medianlow_ = value
		# have odd num of elements before insertion(medianlow = medianlarge = median)
		else:
			if value < self._medianlow_:
				self._maxheap_.put((-value, value))
				_, self._medianlow_ = self._maxheap_.get()
			else:
				self._minheap_.put((value, value))
				_, self._medianlarge_ = self._minheap_.get()
		self._amount_ += 1
		self._sum_ += value

if __name__ == "__main__":
	A = record()
	A.push(3)
	print(A.median,A.amount,A.total)
	A.push(3.9)
	print(A.median,A.amount,A.total)
	A.push(2)
	print(A.median,A.amount,A.total)
	A.push(5)
	print(A.median,A.amount,A.total)
	A.push(1)
	print(A.median,A.amount,A.total)