document.addEventListener("DOMContentLoaded", function() {
    const prevButton = document.getElementById("prev-button");
    const nextButton = document.getElementById("next-button");
    const logoGrid = document.getElementById("logo-grid");
    let currentIndex = 0;
    const itemsPerPage = 9;

    function renderLogos() {
        logoGrid.innerHTML = '';
        for (let i = currentIndex; i < currentIndex + itemsPerPage && i < websiteName.length; i++) {
            const website = websiteName[i];
            const colDiv = document.createElement("div");
            colDiv.className = "col-md-4 col-sm-6 mb-4";
            colDiv.innerHTML = `
                <div class="card">
                    <div class="logo-container">
                        <a href="https://` + website + `" target="_blank">
                            <img src="static/images/${website}.png" alt="${website}">
                            <div class="overlay">${website}</div>
                        </a>
                    </div>
                </div>
            `;
            logoGrid.appendChild(colDiv);
        }
        prevButton.style.display = currentIndex === 0 ? 'none' : 'inline-block';
        nextButton.style.display = currentIndex + itemsPerPage >= websiteName.length ? 'none' : 'inline-block';
    }

    prevButton.addEventListener("click", function() {
        if (currentIndex > 0) {
            currentIndex -= itemsPerPage;
            console.log(currentIndex);
            renderLogos();
        }
    });

    nextButton.addEventListener("click", function() {
        if (currentIndex + itemsPerPage < websiteName.length) {
            currentIndex += itemsPerPage;
            console.log(currentIndex);
            renderLogos();
        }
    });

    renderLogos();
});