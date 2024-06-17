# urls.py
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('process_payment/', views.ProcessPaymentView.as_view(), name='process_payment'),
    path('repeat-order/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('update-order-status/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
    path('order-detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order-cabinet/', views.OrderViewCB.as_view(), name='order_cab'),
    path('', views.MainView.as_view(), name="home"),
    path('catalog/', views.CatalogView.as_view(), name="catalog"),
    path('review/<int:pk>/', views.AddReview.as_view(), name="add_review"),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('account/login/', views.CustomLoginView.as_view(), name='login'),
    path('account/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/payment-cabinet/', views.PaymentCabinetView.as_view(), name='payment_cabinet'),
    path('accounts/profile/payment-cabinet/delete-card/', views.DeleteCardView.as_view(), name='delete_card'),
    path('fetch_cards/', views.fetch_cards, name='fetch_cards'),
    path('basket/', views.BasketView.as_view(), name='basket'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('order/details/<int:order_id>/', views.order_details, name='order_details'),
    path('order/<int:order_id>/add_review/', views.add_review, name='add_review'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('toggle_favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('favorites/', views.FavoritesCabinetView.as_view(), name='favorites_cabinet'),
    path('<slug:slug>/', views.ProductView.as_view(), name='product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
