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





// $(document).ready(function () {
//     $("#upload-button").click(function (e) {
//         e.preventDefault(); // Prevent form submission
//         var fileInput = document.getElementById("clothing-image");

//         // Ensure a file is selected
//         if (!fileInput.files[0]) {
//             alert("Please select an image before uploading.");
//             return;
//         }

//         var formData = new FormData();
//         formData.append("clothingImage", fileInput.files[0]);

//         // Perform AJAX request to /style_match
//         $.ajax({
//             type: "POST",
//             url: "/style_match",
//             data: formData,
//             processData: false,
//             contentType: false,
//             success: function (response) {
            
//                 try {
//                     var recommendationsStr = response.recommendations.replace(/```json|\n```/g, '');
//                     var recommendations = JSON.parse(recommendationsStr);
            
//                     if (Array.isArray(recommendations.recommended_outfits)) {
//                         var outfitsHtml = "<hr><h4>Recommended Outfits</h4><ul>";
//                         recommendations.recommended_outfits.forEach(function (outfit) {
//                             outfitsHtml += `<li><strong>${outfit.name}:</strong> ${outfit.description}</li>`;
//                         });
//                         outfitsHtml += "</ul>";
//                         $("#outfit-suggestions").html(outfitsHtml);
//                     } else {
//                         $("#outfit-suggestions").html("<p>No recommended outfits found.</p>");
//                     }
            
//                     if (Array.isArray(recommendations.style_tips)) {
//                         $("#style-tips").html(`<h3>Style Tips: </h3><ul>${recommendations.style_tips.map(tip => `<li>${tip}</li>`).join('')}</ul>`);
//                     } else {
//                         $("#style-tips").html("<p>No style tips available.</p>");
//                     }

//                     if (Array.isArray(recommendations.accessories)) {

//                         var accessoriesHtml = "<hr><h4>Accesories:</h4><ul>";
//                         recommendations.accessories.forEach(function (accessory) {
//                             accessoriesHtml += `<li><strong>${accessory.type}:</strong> ${accessory.color_scheme}</li>`;
//                         });
//                         accessoriesHtml += "</ul>";
//                         $("#accessories-suggestions").html(accessoriesHtml);
//                     } else {
//                         $("#accessories-suggestions").html("<p>No accessories found.</p>");
//                     }
            
//                     $("#recommendations-section").show();

//                     document.getElementById("recommendations-section").scrollIntoView({
//                         behavior: "smooth",
//                         block: "start"
//                     });
//                 } catch (error) {
//                     console.error("Error parsing recommendations:", error);
//                     alert("There was an error processing the recommendation data.");
//                 }
//             },
//             error: function (error) {
//                 console.error("Error:", error);
//                 alert("An error occurred while uploading the image.");
//             },
//         });
//     });
// });
