const productos = [
    { name: "Monitor", description: "Descripción del monitor", image: "imagen_monitor.jpg" },
    { name: "Mouse", description: "Descripción del mouse", image: "imagen_mouse.jpg" },
    { name: "Teclado", description: "Descripción del teclado", image: "imagen_teclado.jpg" },
    { name: "Tetas", description: "Descripción de las tetas", image: "imagen_tetas.jpg" },
    { name: "Dildos para Oscar (de 70cm)", description: "Descripción del dildo", image: "imagen_dildo.jpg" },
];

const searchInput = document.getElementById("searchInput");
const resultsContainer = document.getElementById("resultsContainer");
const noResults = document.getElementById("noResults");

const handleSearch = () => {
    const searchItem = searchInput.value.toLowerCase();
    const filteredProducts = productos.filter((producto) =>
        producto.name.toLowerCase().includes(searchItem)
    );

    resultsContainer.innerHTML = "";

    if (filteredProducts.length === 0) {
        noResults.style.display = "block";
    } else {
        filteredProducts.forEach((producto) => {
            const card = `
                <div class="card">
                    <img src="${producto.image}" class="card-img-top" alt="${producto.name}">
                    <div class="card-body">
                        <h5 class="card-title">${producto.name}</h5>
                        <p class="card-text">${producto.description}</p>
                    </div>
                </div>
            `;
            resultsContainer.insertAdjacentHTML("beforeend", card);
        });
        noResults.style.display = "none";
    }

    if (searchInput.value === "") {
        resultsContainer.innerHTML = "";
        noResults.style.display = "none";
    }
};

searchInput.addEventListener("input", handleSearch);
