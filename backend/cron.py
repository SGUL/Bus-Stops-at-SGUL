import pycurl, simplejson, datetime, MySQLdb, re
from config import USER, PASS, STOPLIST, MYSQLHOST, MYSQLUSER, MYSQLPASS, MYSQLDBNAME

BASE_URI = 'http://countdown.api.tfl.gov.uk/interfaces/ura/stream_V1'
QUERY_SECTION = '?StopCode1='+STOPLIST+'&ReturnList=StopCode1,Stoppointname,VehicleID,LineName,DestinationText,EstimatedTime,ExpireTime,RegistrationNumber' 

con = None

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
  	print data
  	self.buffer += data
	# Handle complete line
	if data.endswith("]") and self.buffer.strip():
		t = self.buffer.split("\r\n")
		for i in t:
			try:
				row = simplejson.loads(i)
				if len(row) > 4:
					#row[5] = datetime.datetime.fromtimestamp( row[5] / 1000 )
					try:
					    con = MySQLdb.connect(host=MYSQLHOST, user=MYSQLUSER, passwd=MYSQLPASS, db=MYSQLDBNAME)
					    if row[8] <> 0:
							#[1,"St George's Hospital / Lanesborough Wing","57302","493","Richmond",9226,"SN12AUY",1367490314000,1367490314000]
							query="""REPLACE INTO predictions(stopid, vehicleid, stopname, timestamp, busname, destination) 
VALUES ('%s', '%s', '%s', %s, '%s', '%s');""" % (row[2], row[6], re.escape(row[1]), row[7], row[3], re.escape(row[4]))
					    else:
				  	        query="""DELETE FROM predictions WHERE stopid='%s' and vehicleid='%s';""" % (row[2], row[6])
					    cur = con.cursor()
					    cur.execute(query)
					    con.commit()
					except MySQLdb.Error, exception:
					   pass
  					   con.rollback()
					finally:
    					    if con:
 				    	        con.close()					   

			except simplejson.decoder.JSONDecodeError, e:
				pass
			except TypeError, e:
				pass

		self.buffer = ""


def main():
	client = Client()

if __name__ == '__main__':
	main()

