<?php
session_start();
$dbcon=mysqli_connect("localhost","root","");
mysqli_select_db($dbcon,"sales");
extract($_GET);
$sql = "select cost,cgst,sgst from item where item='$product'";
$res=mysqli_query($dbcon,$sql);
$row=mysqli_fetch_assoc($res);
echo "{$row['cost']};{$row['cgst']};{$row['sgst']}";