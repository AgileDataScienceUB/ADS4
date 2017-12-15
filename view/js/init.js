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
