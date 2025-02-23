const windowReady = (callBack) => {
    if (document.readyState === 'complete') {
      callBack();
    }
    else {
      window.addEventListener('load', callBack);
    }
};

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async position => {
                try {
                    // Use reverse geocoding to get city name
                    const response = await fetch(
                        `https://nominatim.openstreetmap.org/reverse?lat=${position.coords.latitude}&lon=${position.coords.longitude}&format=json`
                    );
                    const data = await response.json();
                    const city = data.address.city || data.address.town || data.address.village;
                    document.getElementById('city').value = city;
                } catch (error) {
                    alert('Error getting location: ' + error.message);
                }
            },
            error => {
                alert('Error getting location: ' + error.message);
            }
        );
    } else {
        alert('Geolocation is not supported by this browser.');
    }
}

windowReady(function () {
    const locationButton = document.getElementById('location');
    locationButton.addEventListener('click', getLocation);

    const goButton = document.getElementById('go');
    document.getElementById('recoForm').addEventListener('submit', function (e) {
        e.preventDefault();
    
        const formData = new FormData(this);
    
        const occasionValue = formData.get("occasion");
        const cityValue = formData.get("city");
    
        localStorage.setItem("occasionVal", occasionValue);
        localStorage.setItem("cityVal", cityValue);
    
        fetch('/recommendations', {
            method: 'POST',
            body: formData,
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            sessionStorage.setItem('query', JSON.stringify(Object.fromEntries(formData)));
            sessionStorage.setItem('colorPalettes', JSON.stringify(data["COLOR_PALETTES"]));
    
            const links = data["links"].join(' || ');
            const redirectUrl = `${window.location.protocol}//${window.location.host}/results?${links}`;
            window.location.href = redirectUrl;
        })
        .catch(error => console.error('Error:', error));
    });
    goButton.addEventListener( 'click', (e) => {
        var loader = document.getElementById('center')
        loader.style.display = '';
    });
});