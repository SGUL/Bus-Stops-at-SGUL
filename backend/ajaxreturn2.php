<?php
header('Access-Control-Allow-Origin: *');
header('Content-type: application/json');

function mySQLquery($query) {
	include('config.php');
	mysql_connect($MYSQLHOST, $MYSQLUSER, $MYSQLPASS) or die(mysql_error()." | HOST ".$MYSQLHOST." USER ".$MYSQLUSER." PASS ".$MYSQLPASS ." NAME ".$MYSQLDBNAME." | Error on connect ");
	mysql_select_db($MYSQLDBNAME) or die(mysql_error()." | HOST ".$MYSQLHOST." USER ".$MYSQLUSER." PASS ".$MYSQLPASS ." NAME ".$MYSQLDBNAME." | Error on select db ");

	$result = mysql_query("$query") or die(mysql_error()." | HOST ".$MYSQLHOST." USER ".$MYSQLUSER." PASS ".$MYSQLPASS ." NAME ".$MYSQLDBNAME. " | Error on query " );

	// keeps getting the next row until there are no more to get
	#while($row = mysql_fetch_array( $result )) {
	# // Print out the contents of each row into a table
	#}
	return $result;
}

if (isset($_GET['stopid'])) {
	$busstop=$_GET['stopid'];
	$query = "SELECT * from predictions WHERE stopid='$busstop' ORDER by timestamp asc;";
} else {
	$query = "SELECT * from predictions ORDER by timestamp asc;";
}

$result = mySQLquery($query);

$dict = array();
$dict['time'] =  mktime();
$dict['buses'] = array();
while ($row = mysql_fetch_assoc ( $result )) {
	$out = array();
	$out['stopid'] = $row['stopid'];
	$out['vehicleid'] = $row['vehicleid'];
	$out['stopname'] = $row['stopname'];
	$out['busname'] = $row['busname'];
	$out['timestamp'] = $row['timestamp'];
	$out['destination'] = $row['destination'];
	$dict['buses'][] = $out;
}


print json_encode($dict);

?>
