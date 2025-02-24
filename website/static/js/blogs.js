document.addEventListener("DOMContentLoaded", function() {
    const prevButton = document.getElementById("prev-button");
    const nextButton = document.getElementById("next-button");
    const logoGrid = document.getElementById("logo-grid");
    let currentIndex = 0;
    const itemsPerPage = 6;

    function renderLogos() {
        logoGrid.innerHTML = '';
        for (let i = currentIndex; i < currentIndex + itemsPerPage && i < blogsname.length; i++) {
            const blog = blogsname[i];
            const colDiv = document.createElement("div");
            colDiv.className = "col-md-4 col-sm-6 mb-4";
            colDiv.innerHTML = `
            <div class="card">
                <img src="${blog.Image}"class="card-img-top" alt="${blog.Name}">
                <div class="card-body">
                    <h5 class="card-title">${blog.Name}</h5>
                    <p class="card-text">${blog.Text}</p>
                    <a href="${blog.URL}" target="_blank" class="btn btn-primary">Visit Website</a>
                </div>
            </div>           
            `;          
            logoGrid.appendChild(colDiv);
        }
        prevButton.style.display = currentIndex === 0 ? 'none' : 'inline-block';
        nextButton.style.display = currentIndex + itemsPerPage >= blogsname.length ? 'none' : 'inline-block';
    }

    prevButton.addEventListener("click", function() {
        if (currentIndex > 0) {
            currentIndex -= itemsPerPage;
            console.log(currentIndex);
            renderLogos();
        }
    });

    nextButton.addEventListener("click", function() {
        if (currentIndex + itemsPerPage < blogsname.length) {
            currentIndex += itemsPerPage;
            console.log(currentIndex);
            renderLogos();
        }
    });

    renderLogos();
});