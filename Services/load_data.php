<html>
<head>   
   <link rel="stylesheet" href="../css/table.css">
</head>
<body>
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
$data = json_decode($json,true); #json table

      echo '<table>';


      echo '<thead>';

      foreach($data[0] as $key => $val){ //column headers
	     echo "<th>$key</th>" ;
	}	
      echo '</thead>';

 
 
 foreach($data as $item){ //row
	
	echo '<tr>';
	foreach($item as $key => $val){ //column
	     echo "<td>$val</td>" ;
	}	
	echo "</tr>";
 }	 
      echo '</table>';
      $result->close();
      $conn->close();

?>
</body>
</html>
