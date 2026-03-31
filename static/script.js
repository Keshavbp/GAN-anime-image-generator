document.getElementById('generate-btn').addEventListener('click', function() {
    fetch('/generate')
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.image) {
                const imgElement = document.getElementById('generated-image');
                imgElement.src = 'data:image/png;base64,' + data.image;
                console.log('Image src set to:', imgElement.src.substring(0, 50) + '...');
                imgElement.style.display = 'block';
            } else {
                console.error('No image data in response');
                alert('No image data received. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to generate image. Please try again.');
        });
});