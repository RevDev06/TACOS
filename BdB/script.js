const productos = [
    { name: "Monitor" },
    { name: "Mouse" },
    { name: "Teclado" },
    { name: "Tetas" },
    { name: "Dildos para Tenorio (de 70cm)" },
];

const searchInput = document.getElementById("searchInput");
const resultList = document.getElementById("resultslist");
const noResults = document.getElementById("noResults");


const handleSearch = () => {
    const searchItem = searchInput.value.toLowerCase();
    const filtreredproductos = productos.filter((producto) => producto.name.toLowerCase().startsWith
        (searchItem));

    resultList.innerHTML = "";

    if (filtreredproductos.length === 0) {
        noResults.style.display = "block"
    } else {

        filtreredproductos.forEach((producto) => {
            const li = document.createElement("li");
            li.textContent = producto.name;
            resultList.appendChild(li);
        });
        noResults.style.display = "none";

    }

    if (searchInput.value === "") {
        resultList.innerHTML = "";
    }
};

searchInput.addEventListener("input", handleSearch);