(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();

    $('.modal').modal();

  }); // end of document ready
})(jQuery); // end of jQuery name space



function check(form) { /*function to check userid & password*/
	/*the following code checkes whether the entered userid and password are matching*/
	if(form.email.value == "eloi@focus2hit.com" && form.password.value == "eloi@focus2hit.com") {
 		window.open('./uploadData.html')/*opens the target page while Id & password matches*/

	}else {
		window.alert("Wrong credentials, try again!");
	}
}


//actual handler
$("#submitbutton").on("click", function(){

	//arguments
	var myfile = $("#csvfile")[0].files[0];

	if(!myfile){
		alert("Please select a file");
		return;
	}

	//disable the button during upload
	$("#submitbutton").attr("disabled", "disabled");
	$("#loader").attr("active", "active");
	


	var form = new FormData();
	form.append("file", myfile);

	var settings = {
			"async": true,
			"crossDomain": true,
			"url": "http://34.243.4.122:3031/create-predictor",
			"method": "POST",
			"headers": {
			"cache-control": "no-cache",
			"postman-token": "890f1954-eb41-8e3d-90a0-7e6f5a284141"
		},
		"processData": false,
		"contentType": false,
		"mimeType": "multipart/form-data",
		"data": form
	}


	$.ajax(settings).done(function (response) {
		console.log(response);
	});

});
