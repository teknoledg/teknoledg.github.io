function toggleImages() {
    images.forEach((img, i) => {
        if (i === index) {
            img.style.opacity = 1;
        } else {
            img.style.opacity = 0;
        }
    });
    index = (index + 1) % images.length;
}

function numberFlowSimulator() {
    var numberElement = document.createElement('span');
    numberElement.id = 'number-element';
    var numberText = document.createTextNode('1,106,021');
    numberElement.appendChild(numberText);
    document.getElementById('tagline-container').appendChild(numberElement);

    let speed = 1000;
    let increment = 1000;

    function updateNumber() {
        let currentNumber = parseInt(numberText.textContent.replace(/,/g, ''));
        currentNumber += increment;
        let numberStr = currentNumber.toLocaleString();
        numberText.textContent = numberStr;
    }

    setInterval(function() {
        updateNumber();
        speed = Math.floor(Math.random() * 1000) + 500;
        increment = Math.floor(Math.random() * 1000) + 500;
    }, speed);
}

setTimeout(function() {
    setInterval(toggleImages, 2500);
    toggleImages();
    numberFlowSimulator();
}, 2500);
