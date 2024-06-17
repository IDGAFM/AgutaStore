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
