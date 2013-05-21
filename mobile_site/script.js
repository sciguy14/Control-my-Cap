$(document).ready(function() {
	//Init popup.
	$('#reply').popup();
	$('#about').popup();
});

$(document).on('pageinit', function() {

	$('.minicolors').minicolors({
		animationSpeed: 100,
		animationEasing: 'swing',
		change: null,
		changeDelay: 0,
		control: 'hue',
		defaultValue: '',
		hide: null,
		hideSpeed: 100,
		inline: true,
		letterCase: 'lowercase',
		opacity: false,
		position: 'default',
		show: null,
		showSpeed: 100,
		swatchPosition: 'left',
		textfield: true,
		theme: 'default'
	});
	
	$('#add').submit(function() {
		/* stop form from submitting normally */
		event.preventDefault();
 
		/* get some values from elements on the page: */
		var $form = $( this );
		var twitter = $form.find( 'input[name="twitter"]' ).val();
		var color = $form.find( 'input[name="color"]' ).val();
		var info = {
			"twitter":twitter,
			"color"  :color}
			
		/* Send the data using ajax post */
		$.ajax({
			url:  		"cgi-bin/add.py",
			type: 		"post",
			data: 		JSON.stringify(info),
			contentType: 'application/json',
			dataType: 	"json",
			success: 	function(response)
			{
				var status_title_text = "Oh No!";
				var status_message_text = response.message;
				if (response.success == "true")
				{
					
					status_title_text = "Success!";					
				}
				/* Put the results in a popup and show it. */
				$('#status_title').text(status_title_text); 
				$('#status_message').text(status_message_text);
				$('#reply').popup("open");
			}
		});
 	  
		return false; //So the form doesn't actually submit.
	});
});   

