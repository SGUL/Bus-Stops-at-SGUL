import pycurl, simplejson, datetime
from config import USER, PASS, STOPLIST

BASE_URI = 'http://countdown.api.tfl.gov.uk/interfaces/ura/stream_V1'
QUERY_SECTION = '?StopCode1='+STOPLIST+'&ReturnList=Stoppointname,VehicleID,LineName,DestinationName,EstimatedTime,ExpireTime' 



class Client:
  def __init__(self):
  	
  	auth = (USER, PASS)

	self.buffer = ""
	self.conn = pycurl.Curl()
	self.conn.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST)
	self.conn.setopt(pycurl.USERPWD, "%s:%s" % auth )
	self.conn.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	self.conn.setopt(pycurl.URL, BASE_URI + QUERY_SECTION )
	self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
	self.conn.perform()

	
  def on_receive(self, data):
  	self.buffer += data
	# Handle complete line
	if data.endswith("]") and self.buffer.strip():
		t = self.buffer.split("\r\n")
		for i in t:
			try:
				row = simplejson.loads(i)
				if len(row) > 6:
					row[5] = datetime.datetime.fromtimestamp( row[5] / 1000 )
					row[6] = datetime.datetime.fromtimestamp( row[6] / 1000 )
				print row


			except simplejson.decoder.JSONDecodeError, e:
				print i
			except TypeError, e:
				print 'Type Error', e

		self.buffer = ""
		#print 'Complete'


def main():
	client = Client()

if __name__ == '__main__':
	main()

