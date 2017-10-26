# __date__    = "2017.10.24"
# __author__  = "Shihao Li"
# __env__     = "Python 2.7.12 (default, Nov 19 2016, 06:48:10) | Ubuntu 16.04 LTS"

from __future__ import print_function
from record import record
from structured import structured
from Queue import PriorityQueue
import sys

"""
the core processor that handling data streams
"""
class processor:

	def __init__(self, type):
		if type not in ["zip","date"]:
			raise KeyError('processor type must be one of "zip" and "date"')
		self._type_ = type
		# mapping from something to class<record>
		self._database_ = {}
		# the last modified index of database
		self._recent_ = None

	@property
	def recent(self):
		if self._recent_ is None:
			raise ValueError("processor is empty")
		else:
			return self._recent_

	@property
	def length(self):
		return len(self._database_)

	def total(self, itm):
		if itm not in self._database_:
			raise KeyError("itm not exist in database")
		else:
			return self._database_[itm].total

	def median(self, itm):
		if itm not in self._database_:
			raise KeyError("itm not exist in database")
		else:
			return self._database_[itm].median

	def amount(self, itm):
		if itm not in self._database_:
			raise KeyError("itm not exist in database")
		else:
			return self._database_[itm].amount

	def put(self, line):
		line = structured(line)
		if self._type_ == "zip" and line.isvalidzip:
			self._recent_ = (line.CMTE_ID,line.ZIP_CODE)
			if (line.CMTE_ID,line.ZIP_CODE) not in self._database_:
				self._database_[(line.CMTE_ID,line.ZIP_CODE)] = record()
			self._database_[(line.CMTE_ID,line.ZIP_CODE)].push(line.TRANSACTION_AMT)
			return True
		if self._type_ == "date" and line.isvaliddate:
			self._recent_ = (line.CMTE_ID,line.TRANSACTION_DT)
			if (line.CMTE_ID,line.TRANSACTION_DT) not in self._database_:
				self._database_[(line.CMTE_ID,line.TRANSACTION_DT)] = record()
			self._database_[(line.CMTE_ID,line.TRANSACTION_DT)].push(line.TRANSACTION_AMT)
			return True
		return False

	def getrecent(self):
		return (self.recent[0],
			self.recent[1],
			str(int(self.median(self.recent))),
			str(int(self.amount(self.recent))),
			str(int(self.total(self.recent))))

	# returns a generator, neet next to aquire each tuple
	# since sorting is needed, we need PriorityQueue again
	def getall(self):
		if self._type_ == "date":
			Q = PriorityQueue()
			for item in self._database_:
				Q.put((item[0].lower(), item[1][-4:], item[1][:2], item[1][2:-4], item))
			while not Q.empty():
				_, _, _, _, item = Q.get()
				yield (item[0],
					item[1],
					str(int(self.median(item))),
					str(int(self.amount(item))),
					str(int(self.total(item)))) 
		else:
			raise ValueError("getall only available for 'date' processor")

def printable(formatteddata = None):
	if isinstance(formatteddata, tuple):
		return "|".join(formatteddata)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filepath    = sys.argv[1]
		output_zip  = sys.argv[2]
		output_date = sys.argv[3]
	else:
		filepath    = "../input/itcont.txt"
		output_zip  = "../output/medianvals_by_zip.txt"
		output_date = "../output/medianvals_by_date.txt"
	date_processor = processor("date")
	zip_processor = processor("zip")
	# get total number of lines
	with open(filepath,'r') as f:
		total = 0
		for line in f:
			total += 1
	with open(filepath,'r') as f, open(output_date,'w') as ODate, open(output_zip,'w') as OZip:
		i= 0
		for line in f:
			i += 1
			if i%17 == 0 or i == total:
				print("\r precessing %6d\%d line"%(i,total),end = '')
			date_processor.put(line)
			success = zip_processor.put(line)
			if success:
				OZip.write(printable(zip_processor.getrecent())+'\n')
		date_gen = date_processor.getall()
		for _ in xrange(date_processor.length):
			line = date_gen.next()
			ODate.write(printable(line)+'\n')
		print("\nfinished")