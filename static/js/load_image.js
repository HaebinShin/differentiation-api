function loadImg(id, src){
	src_time=src+(new Date()).getTime();
	$('#'+id).attr('src', src_time)
}
