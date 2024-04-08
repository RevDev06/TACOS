document.querySelectorAll('.dropdown-item').forEach(function(item) {
    item.addEventListener('click', function() {
        var category = item.getAttribute('data-category');
        filterProductsByCategory(category);
    });
});

function filterProductsByCategory(category) {
    var cards = document.querySelectorAll('.category-card');
    cards.forEach(function(card) {
        var cardCategory = card.classList[1];
        if (category === 'all' || cardCategory === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
