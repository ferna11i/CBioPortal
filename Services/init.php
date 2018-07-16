<?php
 require_once "login.php";
 
$conn = new mysqli($hostname, $username , $password, $database);
 
 /*if($conn->connect_error){
	echo "Problem with connection !! ";
 }else{
	echo "All good !";
 }*/
 
 $query = "SELECT * FROM studies";
 $result = $conn->query($query);
 
 if(!$result) die ("Database access failed: " . $conn->error);
 
  //$num_rows = $result->num_rows;
  $rows = array();
  
/*  for ($j = 0 ; $j < $num_rows ; ++$j)
  {
    $result->data_seek($j);
    $row = $result->fetch_array(MYSQLI_NUM);

    //echo $row[0] . "  " . $row[1];
	$rows[$j] = $row;
  }	*/

  while($row = $result->fetch_assoc()){
	$rows[] = $row;  
  }	  
  
  echo json_encode($rows);	
?>