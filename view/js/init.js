(function($){
  $(function(){
  	$("#plots").hide()
	$("#plots2").hide();

    $('.button-collapse').sideNav();
    $('.parallax').parallax();

	$('.modal').modal();
	$('.table-of-contents').pushpin({
		top: 100,
		/*bottom: 200,*/
		offset: 80,

	});

	$('.scrollspy').scrollSpy();



  }); // end of document ready



})(jQuery); // end of jQuery name space

/*
  function(id) {
    return 'a[href="#' + id + '"]';
  }
  */

function check(form) { /*function to check userid & password*/
	/*the following code checkes whether the entered userid and password are matching*/
	if(form.email.value == "eloi@focus2hit.com" && form.password.value == "eloi@focus2hit.com") {
		window.open('./uploadData.html')/*opens the target page while Id & password matches*/
		window.close()

	}else {
		window.alert("Wrong credentials, try again!")
	}
}

        
//actual handler
$("#submitbutton").on("click", function(){


	//arguments
	var myfile = $("#csvfile")[0].files[0]


	if(!myfile){
		alert("Please select a file")
		return;
	} else {

		$("#loader").show()
		

		//disable the button during upload
		$("#submitbutton").attr("disabled", "disabled");

		var form = new FormData();

		form.append("target", "Attrition");
		form.append("file", myfile);
		form.append("employee_id", "EmployeeNumber");
		form.append("job_title", "JobRole");
		form.append("age", "Age");
		form.append("length_of_service", "YearsAtCompany");

		var settings = {
			"async": true,
			"crossDomain": true,
			"url": "http://34.242.186.183:3031/create-predictor",
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

		$.ajax(settings).done(function(response) {
			console.log(response);
			$("#loader").hide();
			$("#submitbutton").removeAttr('disabled');
			$("#plots").show();
			//alert(response)

		});
	}

});


$("#prediction_button").on("click", function(){

	//arguments
	var prediction_csv = $("#prediction_csv")[0].files[0];

	if(!prediction_csv){
		alert("Please select a file");
		return;
	} else {

		//disable the button during upload
		$("#loader2").show()
		$("#plots2").hide();

		$("#prediction_button").attr("disabled", "disabled");

		var form_predict = new FormData();
		form_predict.append("file", prediction_csv);
		form_predict.append("target", "Attrition");
		form_predict.append("employee_id", "EmployeeNumber");
		form_predict.append("job_title", "JobRole");
		form_predict.append("age", "Age");
		form_predict.append("length_of_service", "YearsAtCompany");

		var settings_predict = {
				"async": true,
				"crossDomain": true,
				"url": "http://34.242.186.183:3031/predict",
				"method": "POST",
				"headers": {
				"cache-control": "no-cache",
				"postman-token": "890f1954-eb41-8e3d-90a0-7e6f5a284141"
			},
			"processData": false,
			"contentType": false,
			"mimeType": "multipart/form-data",
			"data": form_predict
		}


		$.ajax(settings_predict).done(function (response_predict) {
			console.log(response_predict);
			//alert("OK!!!")
			$("#loader2").hide();
			$("#prediction_button").removeAttr('disabled');
			$("#plots2").show();

		});
	}


});

$("#download_csv").on("click", function(){
	alert("Not implemented yet!")

});


