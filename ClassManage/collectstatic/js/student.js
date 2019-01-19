$(function () {
	var error_name = false;
	var error_gender = false;
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
			if (age<0||age>80) {
				$('#age').parent().parent().next().html('请输入正确的年龄').show()
				error_age = true
			}
			else{
				$('#age').parent().parent().next().hide()
				error_age = false
			}
		}
	};

	function check_gender(){
		if ($('#gender').val()=='') {
			
		}
	}

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
				url: 'http://127.0.0.1:8888',
				// contentType: "application/json; charset=utf-8",
				// data: JSON.stringify({
				// 	'name': name, 
				// 	'gender': gender, 
				// 	'grade': grade, 
				// 	'age': age
				// }),
				data: {
					'name': name, 
					'gender': gender, 
					'grade': grade, 
					'age': age
				},
				success: function(data){
					alert('haha')
				
				},
				error: function(data){
					console.log(data)
					alert(data)
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