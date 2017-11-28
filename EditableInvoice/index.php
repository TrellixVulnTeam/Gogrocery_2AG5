<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
	
	<title>LAVENIR TECHNOLOGIES</title>	
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"></script>
	<link rel='stylesheet' type='text/css' href='css/style.css' />
	<link rel='stylesheet' type='text/css' href='css/print.css' media="print" />
	<link rel='stylesheet' type='text/css' href='css/bootstrap.min.css'/>
	<link rel='stylesheet' type='text/css' href='css/font-awesome.min.css' />
	<script type='text/javascript' src='js/jquery-1.3.2.min.js'></script>
	<script type='text/javascript' src='js/example.js'></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.3.4/jspdf.min.js"></script>
	<script src="https://getbootstrap.com/dist/js/bootstrap.min.js"></script>
	
    <script>
	var xhr1;
	function getItems(){
		xhr1=new XMLHttpRequest();
		xhr1.open("GET","items.php",false);
		xhr1.onreadystatechange=putItems;
		xhr1.send();
	}
	
	function putItems(){
		if(xhr1.readyState==4 && xhr1.status==200){
			document.getElementById("products").innerHTML=xhr1.responseText;
		}
	}
	var xhr2;
	var i=0;
	function Autofill(){
		var product = document.getElementsByClassName("products")[i];
		xhr2 = new XMLHttpRequest();
		xhr2.open("GET","fill.php?product="+product.value,false);
		xhr2.onreadystatechange=fillAttr;
		xhr2.send();
	}
	function decrement(){
		//console.log(i);
		i--;
		sum();
		return true;
	}
	function increment(){
		//console.log(i);
		i++;
		return true;
	}
	function fillAttr(){
		
		if(xhr2.readyState==4 && xhr2.status==200){
			//console.log("hi");
			var res = xhr2.responseText;
			var arr = res.split(";");				
			var qnt = document.getElementsByClassName("qty")[i];
			var cost = document.getElementsByClassName("cost")[i];
			var cgst = document.getElementsByClassName("cgst")[i];
			var sgst = document.getElementsByClassName("sgst")[i];
			var price = document.getElementsByClassName("pri")[i];
			var q = qnt.value;
			//console.log(qnt);
			cost.innerHTML = q*arr[0];
			cgst.innerHTML = arr[1];
			sgst.innerHTML = arr[2];
			var p = (q*arr[0])+(((arr[1]/100)*(q*arr[0]))+((arr[2]/100)*(q*arr[0])));
			price.innerHTML = p.toPrecision(8);
			sum();
		}
	}
	
	function sum(){
		var pr=document.getElementsByClassName("pri");
		var sum=0;
		for(var j=0;j<i+1;j++){
			console.log(j);
			sum+=parseFloat(pr[j].value);
		}
		console.log(sum);
		document.getElementById("total").innerHTML=sum.toPrecision(8);
		return;
	}
	</script>
	<script>
function printData()
{
  //window.open();
   window.print();
 //  window.download();
}



</script>
</head>

<body id="body">
<?php
/* Set the default timezone */
date_default_timezone_set("Asia/Kolkata");

/* Set the date */
$date = strtotime(date("Y-m-d"));
$abc = date('Y-m-d ');
?>
<form action="bill.php" method="POST">
	<div id="content">
	<div id="page-wrap">

		<textarea id="header">INVOICE</textarea>
		
		<div id="identity">
		
            <textarea id="address" >3rd floor
JP Nagar 7th Phase
Bangalore-560078

Phone: (555) 555-5555</textarea>

            <div id="logo">

              <div id="logoctr">
                <a href="javascript:;" id="change-logo" title="Change logo">Change Logo</a>
                <a href="javascript:;" id="save-logo" title="Save changes">Save</a>
                |
                <a href="javascript:;" id="delete-logo" title="Delete logo">Delete Logo</a>
                <a href="javascript:;" id="cancel-logo" title="Cancel changes">Cancel</a>
              </div>

              <div id="logohelp">
                <input id="imageloc" type="text" size="50" value="" /><br />
                (max width: 540px, max height: 100px)
              </div>
              <img id="image" src="images/logo.png" alt="logo" />
            </div>
		
		</div>
		
		<div style="clear:both"></div>
		
		<div id="customer">

            <textarea id="customer-title">Lavenir Technologies</textarea>

            <table id="meta">
                <tr>
                    <td class="meta-head">Invoice #</td>
                    <td><textarea></textarea></td>
                </tr>
                <tr>

                    <td class="meta-head">Date</td>
                    <td><textarea id="date"></textarea><input type="hidden" id="date" name="date" value="<?php echo $abc ?>"/></td>
                </tr>
                <tr>
                    <td class="meta-head">Amount Due</td>
                    <td><div class="due"></div></td>
                </tr>

            </table>
		
		</div>
		
		<table id="items">
		
		  <tr>
		      <th colspan="1">Item</th>
			  <th>Quantity</th>
		      <th>Cost</th>		      
			  <th>CGST</th>
			  <th>SGST</th>
		      <th colspan="2">Price</th>
		  </tr>
		  
		  <tr class="item-row">
		      <td class="item-name"><div class="delete-wpr">
			  <input list="products" class="products" name="product[]" onclick="getItems()">
			  <datalist id="products">
			  </datalist>
			  </input><a class="delete" href="javascript:;" onclick="return decrement();" title="Remove row">X</a></div></td>
			  <td><input class="qty" name="qty[]" onblur="Autofill()"></input></td>
		      <td><input class="cost" name="cost[]"></input></td>
			  <td><input class="cgst" name="cgst[]"></input></td>
			  <td><input class="sgst" name="sgst[]"></input></td>
		      <td><input class="pri" name="total[]" ></input></td>
		  </tr>
		  
		  <tr id="hiderow">
		    <td colspan="8"><a id="addrow" href="javascript:;" onclick="return increment();" title="Add a row">Add an item</a></td>
		  </tr>
		  
		  <tr>

		      <td colspan="3" class="blank"> </td>
		      <td colspan="3" class="total-line">Total</td>
		      <td class="total-value"><div id="total"></div></td>
		  </tr>
		  <tr>
		      <td colspan="3" class="blank"> </td>
		      <td colspan="3" class="total-line">Amount Paid</td>

		      <td class="total-value"><textarea id="paid"></textarea></td>
		  </tr>
		  <tr>
		      <td colspan="3" class="blank"> </td>
		      <td colspan="3" class="total-line balance">Balance Due</td>
		      <td class="total-value balance"><div class="due"></div></td>
		  </tr>
		
		</table>
		</div>
		<div id="editor"></div>
		<br/>
		<div id="hiderow"> <button type="button" style="left:275px;position:relative" class="btn btn-warning" onclick="printData()">Print</button></div>
		<br/><div id="hiderow"> <button type="button" style="left:275px;position:relative" class="btn btn-success" id="cmd">Download</button> </div>
		<br/><div id="hiderow"> <input type="submit" style="left:275px;position:relative" class="btn btn-success" id="cmd2" value="SendToServer" /> </div>
		<!--<button onclick="printData()">Print me</button>-->
		<div id="terms">
		  <h5>Terms</h5>
		  <textarea>Products can be returned within 30 days</textarea>
		</div>
		</div>
	</form>
</body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.3.3/jspdf.min.js"></script>
        <script>
		$(document).ready(function(){
		var doc = new jsPDF();
var specialElementHandlers = {
    '#editor': function (element, renderer) {
        return true;
    }
};

$('#cmd').click(function () {
    doc.fromHTML($('#content').html(), 15, 15, {
        'width': 170,
            'elementHandlers': specialElementHandlers
    });
    doc.save('sample-file.pdf');
});
});
        </script>
</html>