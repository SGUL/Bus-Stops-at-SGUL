<?php 
class MyStream {
    protected $buffer;

    function stream_open($path, $mode, $options, &$opened_path) {
        // Has to be declared, it seems...
        return true;
    }

    public function stream_write($data) {
        // Extract the lines ; on y tests, data was 8192 bytes long ; never more
        $lines = explode("\n", $data);

        // The buffer contains the end of the last line from previous time
        // => Is goes at the beginning of the first line we are getting this time
        $lines[0] = $this->buffer . $lines[0];

        // And the last line os only partial
        // => save it for next time, and remove it from the list this time
        $nb_lines = count($lines);
        $this->buffer = $lines[$nb_lines-1];
        unset($lines[$nb_lines-1]);

        // Here, do your work with the lines you have in the buffer
        //var_dump($lines);
	foreach ($lines as $line) {
		echo $line;
		$dataarray=explode(",", $line);
		$StopPointName=$dataarray[1];
		$StopID=$dataarray[2];
		$StopCode1=$dataarray[3];
		$StopCode2=$dataarray[4];
		$StopPointState=$dataarray[5];
		$StopPointType=$dataarray[6];
		$StopPointIndicator=$dataarray[7];
		$Towards=$dataarray[8];
		$Bearing=$dataarray[9];
		$Latitude=$dataarray[10];
		$Longitude=$dataarray[11];
		$VisitNumber=$dataarray[12];
		$TripID=$dataarray[13];
		$VehicleID=$dataarray[14];
		$RegistrationNumber=$dataarray[15];
		$LineID=$dataarray[16];
		$LineName=$dataarray[17];
		$DirectionID=$dataarray[18];
		$DestinationText=$dataarray[19];
		$DestinationName=$dataarray[20];
		$EstimatedTime=$dataarray[21];
		$ExpireTime=$dataarray[22];
		// now work on data array
	}
        return strlen($data);
    }
}

stream_wrapper_register("test", "MyStream")
    or die("Failed to register protocol");

$ReturnList='StopPointName,StopID,StopCode1,StopCode2,StopPointState,StopPointType,StopPointIndicator,Towards,Bearing,Latitude,Longitude,VisitNumber,TripID,VehicleID,RegistrationNumber,LineID,LineName,DirectionID,DestinationText,DestinationName,EstimatedTime,MessageUUID,MessageText,MessageType,MessagePriority,ExpireTime,BaseVersion';

$Stops='77501';

$json_url = 'http://countdown.api.tfl.gov.uk/interfaces/ura/stream_V1?StopCode1='.$Stops.'&ReturnList='.$ReturnList; 


include('config.php');

// Open the "file"
$fp = fopen("test://MyTestVariableInMemory", "r+");

// Configuration of curl
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $json_url);
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_DIGEST);
curl_setopt($ch, CURLOPT_USERPWD, $username.":".$password);
curl_setopt($ch, CURLOPT_READFUNCTION, 'read_callback');
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_BUFFERSIZE, 256);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FILE, $fp);    // Data will be sent to our stream ;-)

 
curl_exec($ch); // Getting jSON result string

curl_close($ch);
fclose($fp);




?>
