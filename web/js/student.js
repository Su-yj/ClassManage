$(function () {
	var error_name = false;
	var error_age = false;

	var age = $('#age')

	$('#name').blur(function () {
		check_name();
	})

	$('#age').blur(function () {
		check_age();
	})

	function check_age(){
		if(age=='') {
			return
		}
		else{
			if (!(/(^[1-9]\d*$)/.test(age))) {
				error_age = true
			}
		}
	};
})