import pycurl, simplejson, datetime
import _mysql
from config import USER, PASS, STOPLIST, MYSQLHOST, MYSQLUSER, MYSQLPASS, MYSQLDBNAME

BASE_URI = 'http://countdown.api.tfl.gov.uk/interfaces/ura/stream_V1'
QUERY_SECTION = '?StopCode1='+STOPLIST+'&ReturnList=StopCode1,Stoppointname,VehicleID,LineName,DestinationText,EstimatedTime,ExpireTime,RegistrationNumber' 


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
				if len(row) > 4:
					#row[5] = datetime.datetime.fromtimestamp( row[5] / 1000 )
					#row[6] = datetime.datetime.fromtimestamp( row[6] / 1000 )
					print row
					#try:
					    #pass
					    #con = _mysql.connect(MYSQLHOST, MYSQLUSER, MYSQLPASS, MYSQLDBNAME)
					    #if row[8] <> 0:
					#	pass
						#[1, 'Alexandra Palace Station', '77501', 'W3', 'Nthumberland Pk', 624, 'LJ61CHX', 1367321689000, 1367321689000]
						#query="""INSERT INTO predictions (stopid, vehicleid, stopname, timestamp, busname) VALUES '%s', '%s', '%s', '%s', '%s'""" % (row[2], row[6], row[1], row[7], row[3])
					        #print query
					 #   else:
					#	pass
				  	        #query="""DELETE FROM predictions WHERE stopid='%s' and vehicleid='%s'""" % (row[2], row[6])
						#print query
					#except _mysql.Error, e:
  					#   pass
					#finally:
    					#    if con:
 				    	#        con.close()					   

			except simplejson.decoder.JSONDecodeError, e:
				print i
			except TypeError, e:
				print 'Type Error', e

		self.buffer = ""


def main():
	client = Client()

if __name__ == '__main__':
	main()

