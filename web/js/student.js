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

		if (error_name==false && error_age==false) {
			var name = $('#name').val();
			var gender = $('#gender').val();
			var grade = $('#grade').val();
			var age = $('#age').val();
	
			$.ajax({
				type: 'POST',
				url: 'https://www.baidu.com',
				contentType: "application/json; charset=utf-8",
				data: JSON.stringify(GetJsonData({'name': name, 'gender': gender, 'grade': grade, 'age': age})),
				success: function(success){
					alert('haha')
				
				},
				error: function(error){
					alert('error')
				}
			  });
			// $.post('http://www.baidu.com', {'name': name, 'gender': gender, 'grade': grade, 'age': age}, function(data) {
			// 	alert('result')
			// 	$('.modal').hide()
			// 	$('.modal-backdrop').hide()
			// }).error(function(){
			// 	alert('error')
			// })
		}
		// else{
		// 	$('.modal').show();
		// 	alert('false');
		// }
	})
})