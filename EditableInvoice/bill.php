<?php
session_start();
extract($_POST);
$conn = mysql_connect("127.0.0.1","root","");
if(!$conn)
		{
			die("Could not establish connection to MYSQL");
		}
		else{
		
			$db=mysql_select_db("sales", $conn);
			//$username=$_SESSION['name']; 
			//$sql = "INSERT INTO billing (itemid,username,item,quantity,amount,time) VALUES ('','$username','$product','$qty','$total','$date')";
			//mysql_query($sql, $conn);
			if(!$db)
			{
				
				die("Cannot connect to DB".mysql_error());
			}
			else
			{
					print $_POST['product'];
					// foreach($_POST['product'] as $p){
						// print $p;
					// }
			       //echo "<script> location.href='http://localhost/lavemp/input.php'; </script>";
        exit;
				
			}
		}
?>