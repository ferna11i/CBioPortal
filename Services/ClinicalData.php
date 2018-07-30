<?php

	require_once "login.php";
	
	$conn = new mysqli($hostname, $username , $password, $database);
	if(!$conn) die ("Database access failed: " . $conn->error);
	
	//Get the RAW content from the request
	$content = file_get_contents("php://input");
 
	//Decode the json data to get the command and query
	$data = json_decode($content, true);
	$response = "";		//Clear response for use
	
	if($data['cmd'] == 'getData') $response = getData($conn,$data['query']);
	
	else if($data['cmd'] == 'updateData') $response = updateData($conn,$data['query']);

	header('Content-type: application/json');	
	echo $response;

	
	//Function to get the data
	function getData($conn, $query){

		$rows = array();
		
		$result = $conn->query($query);
		
		if(!$result) die($conn->error);
		
		while($row = $result->fetch_assoc()){
			$rows[] = $row;  
		}
		
		return json_encode($rows);
	}
	
	//Function to update the data in a table
	function updateData($conn, $query){
		
		$result = $conn->query($query);
		
		if(!$result) die($conn->error);
		
		return $result;
	}	
	
?>