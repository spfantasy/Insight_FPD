# __date__    = "2017.10.24"
# __author__  = "Shihao Li"
# __env__     = "Python 2.7.12 (default, Nov 19 2016, 06:48:10) | Ubuntu 16.04 LTS"

import time
"""
each instance is the cleaned data
after reading a whole line from data
it is not judged to be valid or not, as long as it has 21 itms
be aware of utf-8/unicode characters, they are not considered in this class
May it's an alternative solution to run this in python3
Although not examined, most functions are compatible with both version
"""
class structured:
	def __init__(self, line, FEC_FORMAT_ITMS = 21, zipfilter = 5):
		info = line.split("|")
		if len(info) != FEC_FORMAT_ITMS:
			raise ValueError("unexpected line format : ",line)
		self.CMTE_ID 			= info[0 ]#recipient	string
		self.ZIP_CODE 			= info[10]#zipcode 		string
		self.TRANSACTION_DT 	= info[13]#date 		string
		self.OTHER_ID 			= info[15]#				string
		self.TRANSACTION_AMT 	= info[14]#value 		string
		if zipfilter > 0:
			self.ZIP_CODE = self.ZIP_CODE[:zipfilter]

	@property
	def isvalid(self):
		if len(self.OTHER_ID) != 0 or len(self.CMTE_ID) == 0 or len(self.TRANSACTION_AMT) == 0:
			return False
		# mentioned by official description
		elif int(self.TRANSACTION_AMT) <= 200:
			return False
		else:
			return True

	@property		
	def isvaliddate(self):
		if self.isvalid is False:
			return False
		if len(self.TRANSACTION_DT) != 8:
			return False
		try:
			time.strptime(self.TRANSACTION_DT, "%m%d%Y")
		except:
			return False
		return True

	@property
	def isvalidzip(self):
		if self.isvalid is False:
			return False
		if len(self.ZIP_CODE) < 5:
			return False
		return True

	def printer(self):
		print(self.CMTE_ID
			,self.ZIP_CODE
			,self.TRANSACTION_DT
			,self.TRANSACTION_AMT
			,self.OTHER_ID)


if __name__ == "__main__":
	testcase = [
				 "C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783"
				,"C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|384||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337"
				,"C00384818|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|028956146|CVS HEALTH|VP, RETAIL PHARMACY OPS|01122017|250||2017020211435-887|1147467|||4020820171370030285"
				,"C00177436|N|M2|P|201702039042410893|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|307502818|UNUM|SVP, CORPORATE COMMUNICATIONS|01312017|230||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335"
				,"C00177436|N|M2|P|201702039042410895|15|IND|JEROME, CHRISTOPHER|FALMOUTH|ME|041051896|UNUM|EVP, GLOBAL SERVICES|01312017|384||PR2283905245050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029342"
				,"C00384818|N|M2|P|201702039042412112|15|IND|BAKER, SCOTT|WOONSOCKET|RI|028956146|CVS HEALTH|EVP, HEAD OF RETAIL OPERATIONS|01122017|333||2017020211435-910|1147467|||4020820171370030287"
				,"C00177436|N|M2|P|201702039042410894|15|IND|FOLEY, JOSEPH|FALMOUTH|ME|041051935|UNUM|SVP, CORP MKTG & PUBLIC RELAT.|01312017|384||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339"
				]
	for line in testcase:
		A = structured(line)
		print(A.isvaliddate)