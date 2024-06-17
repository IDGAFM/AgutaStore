const burger = document.querySelector('#burger');
const menu = document.querySelector('#b-menu');

burger.addEventListener('click', () => {
    menu.style.display = 'block';
    setTimeout(() => {
        menu.classList.toggle('show');
    }, 50);
});

function toggleImage() {
    var img = document.getElementById('image');
    if (img.src.match("/image/favorite.jpg")) {
        img.src = "/image/favorite-shaded.png";
    } else {
        img.src = "/image/favorite.jpg";
    }
}

function toggleButton(button) {
    var isActive = button.classList.contains('active');

    if (isActive) {
        return;
    }

    var buttons = document.querySelectorAll('.toggle-button');
    buttons.forEach(function(btn) {
        btn.classList.remove('active');
    });

    button.classList.add('active');

    // Убираем подсветку у всех кнопок
    buttons.forEach(btn => {
        btn.classList.remove('selected');
    });

    // Выделяем выбранную кнопку
    button.classList.add('selected');

    // Устанавливаем выбранный размер в скрытое поле формы
    document.getElementById('selected-size').value = button.innerText;
}

document.getElementById('add-to-cart-form').addEventListener('submit', function(event) {
    event.preventDefault();

    if (!isLoggedIn) {
        alert('Войдите в аккаунт чтобы добавить в корзину');
        return;
    }

    var formData = new FormData(this);
    var selectedSize = document.querySelector('.toggle-button.active');

    if (!selectedSize) {
        alert('Пожалуйста, выберите размер');
        return;
    }

    document.getElementById('selected-size').value = selectedSize.innerText;

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/basket/";
        } else {
            console.error('Ошибка при добавлении товара в корзину');
        }
    })
    .catch(error => {
        console.error('Ошибка при отправке запроса:', error);
    });
});