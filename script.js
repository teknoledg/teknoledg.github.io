window.onload = function() {
	var images = document.querySelectorAll('.ai img');
	var index = 0;

	function toggleImages() {
		images[index].classList.remove('visible');
		index = (index + 1) % images.length;
		images[index].classList.add('visible');
	}

	setTimeout(function() {
		toggleImages();
		setInterval(toggleImages, 5000); // Change images every 5 seconds
	}, 5000); // Start the second image 5 seconds after the first
	
	toggleImages();
};
