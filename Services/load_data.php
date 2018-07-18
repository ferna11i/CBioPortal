<?php
 require_once "login.php";
 
 $conn = new mysqli($hostname,$username,$password,$database);

 if ($conn->connect_error) die($conn->connect_error);
	
$query = "SELECT * from data_objects where tag = 'gleason'";
$result = $conn->query($query);

if(!$result){
	die($conn->error);
}
	
 $json = $result->fetch_assoc()['data'];
// header('Content-type: application/json');
// echo $json;
 
 $data = json_decode($json,true);
 
 foreach($data as $item){ //row
	//echo $item['CASE_ID'] . " " . $item['CLINICAL_GLEASON']. "<br>"; 
	
	foreach($item as $key => $val){ //column
		echo $val . "  " ;
	}	
	echo "<br>";
 }	 
 
// echo $data[0]['Name'] . "<br>";
// echo $data[1]['Name'] . "<br>";

?>