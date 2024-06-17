// Helper function to detect card type
function getCardType(cardNumber) {
    const cardPatterns = {
        visa: /^4[0-9]{12}(?:[0-9]{3})?$/,
        mastercard: /^5[1-5][0-9]{14}$/,
        amex: /^3[47][0-9]{13}$/,
        discover: /^6(?:011|5[0-9]{2})[0-9]{12}$/,
    };

    for (let card in cardPatterns) {
        if (cardPatterns[card].test(cardNumber)) {
            return card;
        }
    }
    return 'unknown';
}

// Display card type
function displayCardType(cardType) {
    const cardTypeElement = document.getElementById('card-type');
    cardTypeElement.textContent = cardType !== 'unknown' ? cardType.toUpperCase() : 'Неизвестная карта';
}

// Fetch and populate saved cards
function fetchAndPopulateCards() {
    fetch('/fetch_cards/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        const savedCardsSelect = document.getElementById('saved-cards');
        savedCardsSelect.innerHTML = ''; // Clear existing options

        const newCardOption = document.createElement('option');
        newCardOption.value = 'new';
        newCardOption.textContent = 'Новая карта';
        savedCardsSelect.appendChild(newCardOption);

        if (data.cards.length > 0) {
            data.cards.forEach(card => {
                const option = document.createElement('option');
                option.value = card.id;
                option.textContent = `**** **** **** ${card.card_number.slice(-4)} - ${card.card_holder}`;
                option.dataset.cardNumber = card.card_number;
                option.dataset.expiryDate = card.expiry_date;
                option.dataset.cvv = card.cvv;
                option.dataset.cardHolder = card.card_holder;
                savedCardsSelect.appendChild(option);
            });
        } else {
            const noCardOption = document.createElement('option');
            noCardOption.disabled = true;
            noCardOption.textContent = 'Нет сохраненных карт';
            savedCardsSelect.appendChild(noCardOption);
        }
    })
    .catch(error => {
        console.error('Ошибка при получении карт:', error);
        alert('Ошибка при получении карт, попробуйте еще раз.');
    });
}

// Toggle card form and auto-fill card details based on selected option
function toggleCardForm(value) {
    const cardNumberInput = document.querySelector('input[name="card_number"]');
    const expiryDateInput = document.querySelector('input[name="expiry_date"]');
    const cvvInput = document.querySelector('input[name="cvv"]');
    const cardHolderInput = document.querySelector('input[name="card_holder"]');

    const selectedOption = document.querySelector(`#saved-cards option[value="${value}"]`);

    if (value === 'new') {
        cardNumberInput.value = '';
        expiryDateInput.value = '';
        cvvInput.value = '';
        cardHolderInput.value = '';
    } else {
        cardNumberInput.value = selectedOption.dataset.cardNumber;
        expiryDateInput.value = selectedOption.dataset.expiryDate;
        cvvInput.value = selectedOption.dataset.cvv;
        cardHolderInput.value = selectedOption.dataset.cardHolder;
        const cardType = getCardType(cardNumberInput.value);
        displayCardType(cardType);
    }
}

// Process payment
function processPayment(event) {
    event.preventDefault();

    const addressForm = document.getElementById('address-form');
    if (!addressForm.checkValidity()) {
        alert('Пожалуйста, заполните все поля адреса.');
        return;
    }

    const selectedCard = document.getElementById('saved-cards').value;
    const useSavedCard = selectedCard !== 'new';
    let cardDetails;

    if (!useSavedCard) {
        const cardNumber = document.querySelector('input[name="card_number"]').value;
        const expiryDate = document.querySelector('input[name="expiry_date"]').value;
        const cvv = document.querySelector('input[name="cvv"]').value;
        const cardHolder = document.querySelector('input[name="card_holder"]').value;

        if (!cardNumber || !expiryDate || !cvv || !cardHolder) {
            alert('Пожалуйста, заполните все поля данных карты.');
            return;
        }

        const cardType = getCardType(cardNumber);

        cardDetails = {
            card_number: cardNumber,
            expiry_date: expiryDate,
            cvv: cvv,
            card_holder: cardHolder,
            save_card: document.querySelector('input[name="save_card"]').checked,
            card_type: cardType
        };
    } else {
        cardDetails = { saved_card: selectedCard };
    }

    const formData = new FormData(addressForm);
    const addressData = {
        city: formData.get('city'),
        street: formData.get('street'),
        home: formData.get('home'),
        index: formData.get('index')
    };

    fetch('/process_payment/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            address: addressData,
            use_saved_card: useSavedCard,
            card_details: cardDetails
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Оплата прошла успешно!');
            window.location.href = data.redirect_url;
        } else {
            alert('Ошибка оплаты: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка при оплате:', error);
        alert('Ошибка при оплате, попробуйте еще раз.');
    });
}

// Open and close popup
function openPopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'block';
}

function closePopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'none';
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    fetchAndPopulateCards();
    document.getElementById('saved-cards').addEventListener('change', (event) => toggleCardForm(event.target.value));
    document.getElementById('addCardForm').addEventListener('submit', processPayment);
    document.querySelector('input[name="card_number"]').addEventListener('input', function() {
        const cardType = getCardType(this.value);
        displayCardType(cardType);
    });

    // Burger menu toggle
    const burger = document.querySelector('#burger');
    const menu = document.querySelector('#b-menu');

    burger.addEventListener('click', () => {
        menu.style.display = 'block';
        setTimeout(() => {
            menu.classList.toggle('show');
        }, 50);
    });

    // Close menu on click outside
    document.addEventListener('click', function(event) {
        const isClickInside = menu.contains(event.target) || burger.contains(event.target);
        if (!isClickInside) {
            menu.classList.remove('show');
            setTimeout(() => {
                menu.style.display = 'none';
            }, 300);
        }
    });
});
