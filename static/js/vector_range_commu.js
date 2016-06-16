$(function() {
	$('button#vector_input').bind('click', function() {
		$.getJSON($SCRIPT_ROOT + '/_vector_input', {
			vector: $('input[name="vector"]').val()
		}, function(data) {
			$("#dir_deri").text(data.dir_deri);
		});
		return false;
	});
	$('#range_input').bind('click', function() {
		$.getJSON($SCRIPT_ROOT + '/_range_input', {
			start: $('input[name="start"]').val(),
			end: $('input[name="end"]').val()
		}, function(data) {
			loadImg('plot', '/static/plot.png?')
			loadImg('deri_plot', '/static/deri_plot.png?')
		});
		return false;
	});

});
