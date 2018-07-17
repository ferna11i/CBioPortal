<html>
<head>   
   <link rel="stylesheet" href="../css/table.css">
</head>
<body>
<?php 
  #connect to server
  require_once "login.php";
 
  $conn = new mysqli($hostname, $username , $password, $database);
  if ($conn->connect_error) die($conn->connect_error);
  

  display($conn);

  #print from DB
  function display(&$conn){
      $query  = "SELECT * FROM studies";
      $result = $conn->query($query);
      if (!$result) die ("Database access failed: " . $conn->error);

      $query2  = "DESCRIBE studies";
      $result2 = $conn->query($query2);
      if (!$result2) die ("Database access failed: " . $conn->error);
      
      echo '<table><thead>';

      $num_cols = 0;
      while($i = mysqli_fetch_assoc($result2)){
          echo "<th>{$i['Field']}</th>";
          $num_cols++;
      }

      echo '</thead>';
      
      $rows = $result->num_rows;
      for ($j = 0 ; $j < $rows ; ++$j)
      {
          $result->data_seek($j);
          $row = $result->fetch_array(MYSQLI_NUM);
          
          echo "<tr>";
          for ($i = 0; $i < $num_cols; ++$i) #print all data from DB
              echo "<td>{$row[$i]}</td>";
          echo"</tr>";  #close table row
              
      }
      echo"</table>"; #close table
      $result->close();
      $result2->close();
      $conn->close();

  }
  
?>
</body>
</html>
