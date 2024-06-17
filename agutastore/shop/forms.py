from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile, Reviews, PaymentCard, AdminOrdersReview


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Устанавливаем email в качестве username
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone']

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        if commit:
            profile.user.save()
            profile.save()
        return profile


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['text']


class PaymentCardForm(forms.ModelForm):
    class Meta:
        model = PaymentCard
        fields = ['card_number', 'expiry_date', 'cvv', 'card_holder']

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.isdigit() or len(card_number) != 16:
            raise forms.ValidationError("Введите правильный номер карты.")
        return card_number

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            raise forms.ValidationError("Введите правильный CVV код.")
        return cvv

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data['expiry_date']
        # Реализуйте валидацию формата и даты действия карты
        return expiry_date

    def save(self, commit=True):
        card = super().save(commit=False)
        card.card_type = self.detect_card_type(card.card_number)
        if commit:
            card.save()
        return card

    @staticmethod
    def detect_card_type(card_number):
        if card_number.startswith('4'):
            return 'VISA'
        elif card_number.startswith(('51', '52', '53', '54', '55')):
            return 'MasterCard'
        # Можно добавить дополнительные проверки для других типов карт
        return 'Unknown'


class AdminOrdersReviewForm(forms.ModelForm):
    class Meta:
        model = AdminOrdersReview
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={
                'id': 'review',
                'name': 'review',
                'class': 'review-input',
                'placeholder': 'Напишите заметку...'
            }),
        }