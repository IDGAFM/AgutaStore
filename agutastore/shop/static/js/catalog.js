const burger = document.querySelector('#burger');
const menu = document.querySelector('#b-menu');

burger.addEventListener('click', () => {
    menu.style.display = 'block'; 
    setTimeout(() => {
        menu.classList.toggle('show'); 
    }, 50); 
});


document.getElementById('price-btn').addEventListener('click', function() {
    var filterWindow = document.getElementById('price-filter');
    filterWindow.style.display = (filterWindow.style.display === 'block') ? 'none' : 'block';
});

document.getElementById('apply-price').addEventListener('click', function() {
    var filterWindow = document.getElementById('price-filter');
    filterWindow.style.display = 'none';
});

document.getElementById('brand-btn').addEventListener('click', function() {
    var filterWindow = document.getElementById('brand-filter');
    filterWindow.style.display = 'block';
});

document.getElementById('apply-brand').addEventListener('click', function() {
    var filterWindow = document.getElementById('brand-filter');
    filterWindow.style.display = 'none';
});

document.addEventListener("DOMContentLoaded", function() {
    var tovarBtn = document.getElementById("tovar-btn");
    var tovarFilter = document.getElementById("tovar-filter");
    var applyBtn = document.getElementById("apply-product-type");

    tovarBtn.addEventListener("click", function() {
        tovarFilter.style.display = "block";
    });

    applyBtn.addEventListener("click", function() {
        tovarFilter.style.display = "none";
    });
});

function closeMenu() {
    document.querySelector('.burger-slide').classList.remove('show');
}



