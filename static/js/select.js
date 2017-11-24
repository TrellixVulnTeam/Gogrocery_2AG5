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
				document.getElementById("select1").innerHTML=s;
			},
			error: function(error){
				console.log(error);
			}
		});
	
}
function fetch2(){
	var val1 = document.getElementById("select1").value;
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
				document.getElementById("select2").innerHTML=s;
			},
			error: function(error){
				console.log(error);
			}
		});
}
function fetch3(){
	var val1 = document.getElementById("select1").value;
	var val2 = document.getElementById("select2").value;
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
				document.getElementById("select3").innerHTML=s;
			},
			error: function(error){
				console.log(error);
			}
		});
}
function save_pid(){
	var s = $('#select3').val();
	$('#pid_key').val(dict[s]);
	console.log($('#pid_key').val());
}