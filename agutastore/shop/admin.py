from django.contrib import admin
from .models import (
    Cloth, Category, Brand, ClothShot, ProductType, CartItem, Reviews, PaymentCard,
    Favorite, Order, Profile, PaidItem, AdminOrdersReview
)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name",)}
    list_display = ('name', 'descriptions')
    search_fields = ('name',)

class ProductTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name",)}
    list_display = ('name', 'descriptions')
    search_fields = ('name',)

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name",)}
    list_display = ('name', 'descriptions')
    search_fields = ('name',)
    filter_horizontal = ('category', 'product')

class ClothAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("title",)}
    list_display = ('title', 'price', 'draft', 'is_favorite')
    search_fields = ('title',)
    list_filter = ('brand', 'category', 'product_type')
    filter_horizontal = ('brand', 'product_type', 'category')

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'cloth', 'time')
    search_fields = ('text', 'user__username', 'cloth__title')
    list_filter = ('time',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'cloth', 'quantity')
    search_fields = ('user__username', 'cloth__title')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'order_date', 'status', 'total_amount')
    search_fields = ('order_number', 'user__username')
    list_filter = ('status', 'order_date')

class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ('owner', 'card_number', 'expiry_date')
    search_fields = ('owner__username', 'card_number')

class PaidItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'cloth', 'quantity', 'price', 'created_at')
    search_fields = ('order__order_number', 'cloth__title')
    list_filter = ('created_at',)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'cloth')
    search_fields = ('user__username', 'cloth__title')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'first_name', 'last_name', 'email')
    search_fields = ('user__username', 'phone', 'first_name', 'last_name', 'email')

admin.site.register(Cloth, ClothAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ClothShot)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(PaymentCard, PaymentCardAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(PaidItem, PaidItemAdmin)
admin.site.register(AdminOrdersReview)

