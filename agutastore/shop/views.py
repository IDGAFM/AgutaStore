import uuid
from django.db.models import Q
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView

from .forms import UserRegisterForm, UserLoginForm, ProfileForm, ReviewForm, PaymentCardForm, AdminOrdersReviewForm
from .models import Cloth, Order, PaymentCard, Profile, CartItem, Brand, ProductType, Category, Favorite, PaidItem, \
    ClothShot


# Create your views here.
class MainView(ListView):
    model = Cloth
    template_name = 'aitustore/index.html'
    context_object_name = 'newThing'

    def get_queryset(self):
        return Cloth.objects.order_by('-id')[:6]


class CatalogView(ListView):
    model = Cloth
    template_name = 'aitustore/catalog.html'
    context_object_name = 'catalog'
    paginate_by = 9

    def get_queryset(self):
        queryset = Cloth.objects.all()
        category = self.request.GET.get('category')
        product_type = self.request.GET.get('product_type')

        if category:
            queryset = queryset.filter(category__url=category)

        if product_type:
            queryset = queryset.filter(product_type__url=product_type)

        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        brands = self.request.GET.getlist('brand')
        search_query = self.request.GET.get('search', '')

        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)
        if brands:
            queryset = queryset.filter(brand__in=brands).distinct()
        if search_query:
            queryset = queryset.filter(title__icontains=search_query).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['product_types'] = ProductType.objects.all().order_by('-id')
        context['search_query'] = self.request.GET.get('search', '')
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')

        product_type_url = self.request.GET.get('product_type')

        if product_type_url:
            context['selected_product_type'] = ProductType.objects.filter(url=product_type_url).first()
        else:
            context['selected_product_type'] = None

        return context


class ProductView(DetailView):
    model = Cloth
    template_name = 'aitustore/product.html'
    context_object_name = 'view'
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cloth = self.get_object()
        user = self.request.user
        context['reviews'] = cloth.get_review()
        context['cloth_shots'] = ClothShot.objects.filter(cloth=cloth)
        context['is_user_logged_in'] = user.is_authenticated
        context['is_favorite'] = Favorite.objects.filter(user=user,
                                                         cloth=cloth).exists() if user.is_authenticated else False
        return context


class FavoritesCabinetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'aitustore/favorites-cabinet.html', {'favorites': favorites, 'is_favorite': True})


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cloth_id = request.POST.get('cloth_id')
        size = request.POST.get('size')

        cloth = get_object_or_404(Cloth, id=cloth_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, cloth=cloth)

        if not created:
            favorite.delete()
            return JsonResponse({'added': False})

        return JsonResponse({'added': True})


class CustomLoginView(LoginView):
    template_name = 'aitustore/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('profile')

    def get_initial(self):
        initial = super().get_initial()
        email_from_registration = self.request.session.get('registered_email')
        if email_from_registration:
            initial['username'] = email_from_registration
        return initial


class RegisterView(CreateView):
    template_name = 'aitustore/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        profile = Profile.objects.create(user=user)
        user = authenticate(username=user.email, password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class ProfileView(ListView):
    model = Profile
    template_name = 'aitustore/personal-cabinet.html'
    context_object_name = 'prof'

    def get_queryset(self):
        user_profile, created = Profile.objects.get_or_create(user=self.request.user)
        return [user_profile]


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)


class AddReview(View):
    def post(self, request, pk):
        error = ''
        form = ReviewForm(request.POST)
        cloth = Cloth.objects.get(pk=pk)
        if form.is_valid():
            review = form.save(commit=False)
            review.cloth = cloth
            review.user = request.user
            if request.POST.get("parent", None):
                review.parent_id = int(request.POST.get("parent"))
            review.save()
        return redirect(cloth.get_absolute_url())


class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'aitustore/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-order_date') if self.request.user.is_staff else Order.objects.filter(
            user=self.request.user).order_by('-order_date')

        search_query = self.request.GET.get('search', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')

        queryset = queryset.exclude(status='delivered')

        if search_query:
            queryset = queryset.filter(
                Q(order_number__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query)
            )

        if date_from:
            queryset = queryset.filter(order_date__gte=datetime.strptime(date_from, '%Y-%m-%d'))

        if date_to:
            queryset = queryset.filter(order_date__lte=datetime.strptime(date_to, '%Y-%m-%d'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_status_choices'] = dict(Order.ORDER_STATUS_CHOICES)
        context['search_query'] = self.request.GET.get('search', '')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        return context


@login_required
def add_review(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not request.user.is_staff and order.user != request.user:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    if request.method == 'POST':
        form = AdminOrdersReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.user = request.user
            review.save()
            return redirect('order_details', order_id=order.id)

    return redirect('order_details', order_id=order.id)


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not request.user.is_staff and order.user != request.user:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    reviews = order.reviews.all()
    form = AdminOrdersReviewForm()

    context = {
        'order': order,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'aitustore/admin-orders-info.html', context)


@require_POST
@login_required
def update_order_status(request, order_id, status):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    order = get_object_or_404(Order, id=order_id)
    if status not in dict(Order.ORDER_STATUS_CHOICES):
        return JsonResponse({'error': 'Invalid status'}, status=400)

    order.status = status
    order.save()
    return JsonResponse({'success': True, 'new_status': order.get_status_display()})


@require_POST
@login_required
def repeat_order(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        if order.user != request.user:
            return JsonResponse({'error': 'Not authorized'}, status=403)

        new_order_number = f"{order.order_number}-{uuid.uuid4().hex[:2]}"

        new_order = Order.objects.create(
            order_number=new_order_number,
            user=order.user,
            quantity=order.quantity,
            total_items=order.total_items,
            total_amount=order.total_amount,
            city=order.city,
            street=order.street,
            home=order.home,
            size=order.size,
            index=order.index,
            status='pending'
        )

        for item in order.paid_items.all():
            PaidItem.objects.create(
                order=new_order,
                cloth=item.cloth,
                size=item.size,
                quantity=item.quantity,
                price=item.price
            )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        cloth = get_object_or_404(Cloth, pk=product_id)
        existing_item = CartItem.objects.filter(user=request.user, cloth=cloth, size=size).first()
        if existing_item:
            existing_item.quantity += 1
            existing_item.save()
        else:
            CartItem.objects.create(user=request.user, cloth=cloth, size=size)
        return redirect(reverse('basket'))


class OrderDetailView(DetailView):
    model = Order
    template_name = 'aitustore/admin-orders-info.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_status_choices'] = dict(Order.ORDER_STATUS_CHOICES)
        return context

    def get_object(self, queryset=None):
        order = super().get_object(queryset=queryset)
        if not self.request.user.is_staff:
            raise PermissionDenied("You are not authorized to view this page.")
        return order


class BasketView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'aitustore/cartitem_list.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_price = sum(item.cloth.price for item in cart_items)
        context['total_price'] = total_price
        context['cart_empty'] = not cart_items.exists()
        return context


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
        cart_item.delete()
        return redirect(reverse('basket'))


class PaymentCabinetView(View):
    def get(self, request):
        user = request.user
        cards = PaymentCard.objects.filter(owner=user)
        form = PaymentCardForm()
        return render(request, 'aitustore/payment-cabinet.html', {'cards': cards, 'form': form, 'user': user})

    def post(self, request):
        user = request.user
        form = PaymentCardForm(request.POST)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.owner = user
            new_card.save()
            return redirect('payment_cabinet')
        else:
            cards = PaymentCard.objects.filter(owner=user)
            return render(request, 'aitustore/payment-cabinet.html', {'cards': cards, 'form': form, 'user': user})


class DeleteCardView(View):
    def post(self, request):
        user = request.user
        card_id = json.loads(request.body).get("card_id")
        try:
            card = PaymentCard.objects.get(id=card_id, owner=user)
            card.delete()
            return JsonResponse({"success": True})
        except PaymentCard.DoesNotExist:
            return JsonResponse({"success": False}, status=404)


@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        cards = PaymentCard.objects.filter(owner=request.user)
        total_price = sum(item.cloth.price * item.quantity for item in cart_items)
        context = {
            'cart_items': cart_items,
            'cards': cards,
            'total_price': total_price,
            'cart_empty': not cart_items.exists(),
        }
        return render(request, 'aitustore/cartitem_list.html', context)


@method_decorator(login_required, name='dispatch')
class ProcessPaymentView(View):
    def post(self, request):
        data = json.loads(request.body)
        address = data.get('address')
        use_saved_card = data.get('use_saved_card')
        card_details = data.get('card_details', {})

        if use_saved_card:
            card_id = card_details.get('saved_card')
            card = get_object_or_404(PaymentCard, id=card_id, owner=request.user)
        else:
            card = PaymentCard(
                owner=request.user,
                card_number=card_details['card_number'],
                expiry_date=card_details['expiry_date'],
                cvv=card_details['cvv'],
                card_holder=card_details['card_holder'],
                card_type=card_details['card_type']
            )
            if card_details.get('save_card'):
                card.save()

        payment_successful = True  # Симуляция успешной оплаты

        if payment_successful:
            order_number = str(uuid.uuid4()).replace('-', '').upper()[:6]
            cart_items = CartItem.objects.filter(user=request.user)
            total_amount = sum(item.cloth.price * item.quantity for item in cart_items)

            order = Order.objects.create(
                order_number=order_number,
                user=request.user,
                total_amount=total_amount,
                status='pending',
                city=address['city'],
                street=address['street'],
                home=address['home'],
                index=address['index']
            )

            for item in cart_items:
                PaidItem.objects.create(
                    order=order,
                    cloth=item.cloth,
                    quantity=item.quantity,
                    size=item.size,
                    price=item.cloth.price * item.quantity
                )
            cart_items.delete()
            return JsonResponse({'success': True, 'redirect_url': '/'})

        return JsonResponse({'success': False, 'error': 'Ошибка при обработке платежа'}, status=400)


def fetch_cards(request):
    if request.user.is_authenticated:
        user_cards = PaymentCard.objects.filter(owner=request.user)
        cards_list = [{'id': card.id, 'card_number': card.card_number, 'card_holder': card.card_holder} for card in
                      user_cards]
        return JsonResponse({'cards': cards_list})
    else:
        return JsonResponse({'cards': []})


class OrderViewCB(ListView):
    model = Order
    template_name = 'aitustore/order-cabinet.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.none()  # Admins shouldn't see orders here
        # Otherwise, return only the delivered orders of the logged-in user
        return Order.objects.filter(user=self.request.user, status='delivered')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_staff
        return context
