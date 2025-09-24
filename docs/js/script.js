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
	
	// Handle form submission
	const updateForm = document.getElementById('updateForm');
	if (updateForm) {
		updateForm.addEventListener('submit', async function(e) {
			e.preventDefault();
			
			const email = document.getElementById('email').value;
			const name = document.getElementById('name').value;
			
			// Simple validation
			if (!email) {
				alert('Please enter your email address.');
				return;
			}
			
			// Show loading state
			const submitBtn = updateForm.querySelector('.submit-btn');
			const originalText = submitBtn.textContent;
			submitBtn.textContent = 'Registering...';
			submitBtn.disabled = true;
			
			try {
				// Submit to backend
        // Update this URL to your deployed backend
        const BACKEND_URL = 'https://data.thepersonaldataexchange.com/backend/api.php';
        
        // Create form data for PHP backend
        const formData = new FormData();
        formData.append('action', 'register');
        formData.append('email', email);
        formData.append('name', name);
        
        const response = await fetch(BACKEND_URL, {
					method: 'POST',
					body: formData
				});
				
				const result = await response.json();
				
				if (result.success) {
					alert(result.message);
					updateForm.reset();
				} else {
					alert(result.message || 'Registration failed. Please try again.');
				}
				
			} catch (error) {
				console.error('Registration error:', error);
				alert('Registration failed. Please check your connection and try again.');
			} finally {
				// Reset button state
				submitBtn.textContent = originalText;
				submitBtn.disabled = false;
			}
		});
	}
};