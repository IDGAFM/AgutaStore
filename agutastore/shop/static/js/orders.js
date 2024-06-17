document.addEventListener("DOMContentLoaded", function() {
    const detailButtons = document.querySelectorAll('.detail');
    const modalOverlay = document.querySelector('.modal-overlay');
    const modal = document.querySelector('.modal');
    const closeButton = document.querySelector('.close');

    detailButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            modalOverlay.style.display = 'block';
            modal.style.display = 'block';
        });
    });

    closeButton.addEventListener('click', function() {
        modalOverlay.style.display = 'none';
        modal.style.display = 'none';
    });
});


const burger = document.querySelector('#burger');
const menu = document.querySelector('#b-menu');

burger.addEventListener('click', () => {
    menu.style.display = 'block';
    setTimeout(() => {
        menu.classList.toggle('show');
    }, 50);
});

function closeMenu() {
    document.querySelector('.burger-slide').classList.remove('show');
}
