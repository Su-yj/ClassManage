$(function () {
	var error_name = false;
	var error_age = false;

	$('#name').blur(function () {
		check_name();
	})

	$('#age').blur(function () {
		check_age();
	})

	function check_name(){
		if($('#name').val()==''){
			$('#name').parent().parent().next().html('请输入学生名').show()
			error_name = true;
		}
		else{
			$('#name').parent().parent().next().hide()
			error_name = false;
		}
	}

	function check_age(){
		if (!(/^\d*$/).test($('#age').val())) {
			$('#age').parent().parent().next().html('请输入整数').show()
			error_age = true
		}
		else{
			var age = Number($('#age').val())
			if (age<0||age>800) {
				$('#age').parent().parent().next().html('请输入正确的年龄').show()
				error_age = true
			}
			else{
				$('#age').parent().parent().next().hide()
				error_age = false
			}
		}
	};

	$('#refer_to').click(function() {
		check_name();
		check_age();

		var name = $('#name').val();
		var gender = $('#gender').val();
		var grade = $('#grade').val();
		var age = $('#age').val();

		$.post('url', {'name': name, 'gender': gender, 'grade': grade, 'age': age}, function(result) {
			alert(result);
		})
	})
})