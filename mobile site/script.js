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
});   