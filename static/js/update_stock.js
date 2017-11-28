var dict = {}
function fetch1(){
		$.ajax({
			url: '/fetch_categories',
			type: 'GET',
			success: function(response){
				//console.log(response.list_of_data); //	IF using the jasonify
				console.log(response); //if using json.dumps({object})
				var s = "<option>NONE</option>";
				response = JSON.parse(response)
				for(var i =0;i < response.length;i++){
					s += "<option>" + response[i] + "</option>";
				}
				document.getElementById("category").innerHTML=s;
			},
			error: function(error){
				console.log(error);
			}
		});
	
}
function fetch2(){
	var val1 = document.getElementById("category").value;
	$.ajax({
			url: '/fetch_sub_categories?val='+val1,
			type: 'GET',
			success: function(response){
				//console.log(response.list_of_data); //	IF using the jasonify
				console.log(response); //if using json.dumps({object})
				response = JSON.parse(response);
				var s = "<option>NONE</option>";

				for(var i =0;i < response.length;i++){
					s += "<option>" + response[i] + "</option>";
				}
				document.getElementById("sub_category").innerHTML=s;
			},
			error: function(error){
				console.log(error);
			}
		});
}
function fetch3(){
	var val1 = document.getElementById("category").value;
	var val2 = document.getElementById("sub_category").value;
	$.ajax({
			url: '/fetch_products?val1='+val1+'&val2='+val2,
			type: 'GET',
			success: function(response){
				//console.log(response.list_of_data); //	IF using the jasonify
				
				console.log(response); //if using json.dumps({object})
				response = JSON.parse(response);
				dict = {};
				var s = "<option>NONE</option>";
				for(var i =0;i < response.length;i++){
					
					s += "<option>" + response[i][0] + "</option>";
					dict[response[i][0]] = response[i][1];
				}
				document.getElementById("product").innerHTML=s;
			},
			error: function(error){
				console.log(error);
			}
		});
}
// function fetch4(){
// 	var val1 = document.getElementById("category").value;
// 	var val2 = document.getElementById("sub_category").value;
// 	var val3 = document.getElementById("product").value;
// 	$.ajax({
// 			url: '/fetch_supplier?val1='+val1+'&val2='+val2+'&val3='+val3,
// 			type: 'GET',
// 			success: function(response){
// 				//console.log(response.list_of_data); //	IF using the jasonify
// 				console.log(response); //if using json.dumps({object})
// 				var s = "<option>NONE</option>";
// 				response = JSON.parse(response)
// 				for(var i =0;i < response.length;i++){
// 					s += "<option>" + response[i] + "</option>";
// 				}
// 				document.getElementById("supplier_alt").innerHTML=s;
// 			},
// 			error: function(error){
// 				console.log(error);
// 			}
// 		});
// }
function save_pid(){
	var s = $('#select3').val();
	$('#pid_key').val(dict[s]);
	console.log($('#pid_key').val());
}