/**
 * ai-build.log
 * 
 * Log of changes made by AI:
 * - Updated the JavaScript code to align with CSS animations.
 * - Ensured the animation loops infinitely with one image coming in and the other fading/blurring out.
 * - Adjusted the script to display the second image coming into focus for 2.5 seconds.
 * - Delayed the animation of the second image by 2.5 seconds at the start.
 * - Alternated images to switch between front visible and back blurred/invisible with transitions.
 * - Added number flow simulator to show a large number flowing up and down infinitely.
 */
window.onload = function() {
    var images = document.querySelectorAll('.ai-img');
    var index = 0;

    function toggleImages() {
        images.forEach((img, i) => {
            if (i === index) {
                img.style.opacity = 1;
                img.style.filter = 'blur(0px)'; // Fix for errors
            } else {
                img.style.opacity = 0;
                img.style.filter = 'blur(5px)'; // Fix for errors
            }
        });
        index = (index + 1) % images.length;
    }

    function numberFlowSimulator() {
        var numberElement = document.createElement('div');
        numberElement.classList.add('number-flow');
        numberElement.textContent = '1,106,021';
        document.body.appendChild(numberElement);

        setInterval(function() {
            numberElement.style.transform = 'translateY(-50px)';
            setTimeout(function() {
                numberElement.style.transform = 'translateY(0)';
            }, 1000);
        }, 2000);
    }

    // Delay the animation of the second image by 2.5 seconds at the start
    setTimeout(function() {
        setInterval(toggleImages, 2500); // Change images every 2.5 seconds
        toggleImages(); // Ensure one image is visible on load
        numberFlowSimulator(); // Start the number flow simulation
        var tagline = document.createElement('p');
        tagline.textContent = 'Secure, Live, Personal data streams, traded on PDX.';
        document.body.appendChild(tagline); // Add tagline after the numbers
    }, 2500);
}