$(document).ready(function() { 
	bars_orig = $('#bars div span').map(function() {
		return parseInt($(this).css('height').split('%')[0]);
	});

	$('#header').hover(
		function() {
			bars_animate = true;
			animate_bars();
		},
		function() {
			bars_animate = false;
			stop_bars();
		}
	);
});

function stop_bars() {
	$('#bars div span').each(function(i, val) {
		nh = bars_orig[i];
		$(this).stop().animate({'height': nh + '%'}, 200, 'linear');
	});
}

function animate_bars() {
	$('#bars div span').each(function() {
		update_bar(this);
	});
}

function update_bar(bar) {
		if(!bars_animate)
			return false;

		h = parseInt($(bar).css('height').split('%')[0]);

		min = 10;
		max = 100;
		delta = 40;
		time = 200;

		if(h > min+delta)
			dmin = -delta;
		else
			dmin = 0;
		if(h < max-delta)
			dmax = delta;
		else
			dmax = 0;

		nh = h + (Math.floor(Math.random() * (dmax-dmin)) + dmin);
		//console.log('h = ' + h + ', nh = ' + nh);
		
		$(bar).animate({'height': nh + '%'}, time, 'linear',
						function() { update_bar(bar); });
}
