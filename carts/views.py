from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart


def cart_detail_api_view(request):
    cart, new_obj = Cart.objects.new_or_get(request)
    products = [{
        'id': x.id,
        'url': x.get_absolute_url(),
        'title': x.title,
        'price': x.price
    }
        for x in cart.products.all()]
    cart_data = {'products': products, 'subtotal': cart.subtotal, 'total': cart.total}
    return JsonResponse(cart_data)


def cart_home(request):
    cart, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {'cart': cart})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        product_obj = Product.objects.get(id=product_id)
        cart, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart.products.all():
            cart.products.remove(product_obj)
            added = False
        else:
            cart.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart.products.count()
        if request.is_ajax():
            print('Ajax request')
            json_data = {
                'added': added,
                'removed': not added,
                'cartItems': cart.products.count()
            }
            return JsonResponse(json_data, status=200)
    return redirect('carts:home')


def checkout_home(request):
    cart, new_cart = Cart.objects.new_or_get(request)
    order = None
    if new_cart or cart.products.count() == 0:
        return redirect('carts:home')
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order, order_created = Order.objects.new_or_get(billing_profile=billing_profile, cart=cart)
        if shipping_address_id:
            order.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if shipping_address_id:
            order.save()
    if request.method == 'POST':
        is_done = order.check_done()
        if is_done:
            order.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect('carts:success')
    context = {
        'order': order,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs
    }
    return render(request, 'carts/checkout.html', context)


def checkout_done_view(request):
    return render(request, 'carts/checkout_done.html', {})
