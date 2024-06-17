


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

document.getElementById("openPopup").addEventListener("click", function() {
  document.getElementById("popup").style.display = "block";
});

document.getElementById("closePopup").addEventListener("click", function() {
  document.getElementById("popup").style.display = "none";
});

window.addEventListener("click", function(event) {
  var popup = document.getElementById("popup");
  if (event.target == popup) {
    popup.style.display = "none";
  }
});