from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, AbstractUser, Permission, Group
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class Category(models.Model):
    """''Категория товара"""

    name = models.CharField("Имя", max_length=100)
    descriptions = models.TextField("Описание")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"


class ProductType(models.Model):
    """''Вид товара"""

    name = models.CharField("Имя", max_length=150)
    descriptions = models.TextField("Описание")
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид товара"
        verbose_name_plural = "Вид товара"


class Brand(models.Model):
    """''Бренд продукта"""
    name = models.CharField("имя", max_length=150)
    descriptions = models.TextField("описание")
    url = models.SlugField(max_length=150, unique=True)
    category = models.ManyToManyField(Category, verbose_name="Категория", related_name='brands')
    product = models.ManyToManyField(ProductType, verbose_name="Вид товара")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренды"
        verbose_name_plural = "Бренды"


class Cloth(models.Model):
    """Товар"""
    title = models.CharField("Заголовок", max_length=150)
    descriptions = models.TextField("Описание")
    mainPoster = models.ImageField("Изображение", upload_to='products')

    brand = models.ManyToManyField(Brand, verbose_name='Бренды', related_name='product_brand')
    product_type = models.ManyToManyField(ProductType, verbose_name='тип продукта')
    price = models.PositiveIntegerField("Цена", default=0, help_text="Укажите сумму в тенге")
    category = models.ManyToManyField(Category, verbose_name='Категория', blank=True)

    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    is_favorite = models.BooleanField("избранное", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)


class ClothShot(models.Model):
    """''Фото товара"""

    title = models.CharField("Заголовок", max_length=150)
    image = models.ImageField("Изображение", upload_to='cloth_shots')
    image1 = models.ImageField("Изображение", upload_to='cloth_shots', blank=True, null=True)
    image2 = models.ImageField("Изображение", upload_to='cloth_shots', blank=True, null=True)
    cloth = models.ForeignKey(Cloth, verbose_name="Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товара"


class Reviews(models.Model):
    """''Отзыв"""
    text = models.TextField("Отзыв", max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    cloth = models.ForeignKey(Cloth, verbose_name="Товар", on_delete=models.CASCADE)
    time = models.DateField('Дата отправки', default=timezone.now)

    def __str__(self):
        return f'{self.text} - {self.cloth}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class CartItem(models.Model):
    """'корзина'"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.CharField("Размер", max_length=50)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} - {self.quantity} items'

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждение'),
        ('processing', 'Сборка'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )

    order_number = models.CharField("Номер заказа", max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    quantity = models.PositiveIntegerField("Количество позиций", default=1)
    total_items = models.PositiveIntegerField("Общее количество товаров", default=1)
    order_date = models.DateField("Дата заказа", default=timezone.now)
    total_amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    status = models.CharField("Статус заказа", max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    city = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    home = models.CharField(max_length=100)
    index = models.CharField(max_length=20)

    def __str__(self):
        return f"Заказ №{self.order_number} от {self.order_date} ({self.user.username})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class PaymentCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # Формат MM/YY
    cvv = models.CharField(max_length=4)
    card_holder = models.CharField(max_length=100)
    card_type = models.CharField(max_length=20, blank=True)


class PaidItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='paid_items')
    cloth = models.ForeignKey('Cloth', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'cloth')

    def __str__(self):
        return f"{self.user.username} - {self.cloth.title}"

    class Meta:
        verbose_name = "FAV"
        verbose_name_plural = "FAV"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    first_name = models.CharField(max_length=30, blank=True)  # Добавляем столбец для хранения first name
    last_name = models.CharField(max_length=30, blank=True)  # Добавляем столбец для хранения last name
    email = models.EmailField(max_length=255, blank=True)  # Добавляем столбец для хранения email

    def save(self, *args, **kwargs):
        # Синхронизируем first name, last name и email с соответствующими полями пользователя Django
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
            self.email = self.user.email
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class AdminOrdersReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at.strftime("%d.%m.%Y")}'
