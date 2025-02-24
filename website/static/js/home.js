const windowReady = (callBack) => {
    if (document.readyState === 'complete') {
      callBack();
    }
    else {
      window.addEventListener('load', callBack);
    }
};

windowReady(function () {
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

function updateBudgetValues(slider, type) {
    const lowerSlider =
      document.getElementById("lowerRangeSlider");
    const upperSlider =
      document.getElementById("upperRangeSlider");
    const lowerInput = document.getElementById("lowerBudget");
    const upperInput = document.getElementById("upperBudget");

    if (type === "lower") {
      // Ensure lower value doesn't exceed upper value
      const value = Math.min(
        parseInt(slider.value),
        parseInt(upperSlider.value)
      );
      lowerSlider.value = value;
      lowerInput.value = value;
    } else {
      // Ensure upper value doesn't go below lower value
      const value = Math.max(
        parseInt(slider.value),
        parseInt(lowerSlider.value)
      );
      upperSlider.value = value;
      upperInput.value = value;
    }
  }

  function updateSliderFromInput(input, type) {
    const lowerSlider =
      document.getElementById("lowerRangeSlider");
    const upperSlider =
      document.getElementById("upperRangeSlider");
    const lowerInput = document.getElementById("lowerBudget");
    const upperInput = document.getElementById("upperBudget");

    let value = parseInt(input.value) || 0;

    // Clamp value between min and max
    value = Math.max(0, Math.min(200, value));

    if (type === "lower") {
      // Ensure lower value doesn't exceed upper value
      value = Math.min(value, parseInt(upperInput.value));
      lowerSlider.value = value;
      lowerInput.value = value;
    } else {
      // Ensure upper value doesn't go below lower value
      value = Math.max(value, parseInt(lowerInput.value));
      upperSlider.value = value;
      upperInput.value = value;
    }
  }