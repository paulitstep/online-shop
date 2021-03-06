"""online_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic.base import RedirectView

from accounts.views import LoginView, RegisterView, GuestRegisterView
from addresses.views import AddressListView, AddressCreateView, AddressUpdateView, checkout_address_create_view, checkout_address_reuse_view
from billing.views import payment_method_view, payment_method_create_view
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, Mailchimp_Webhook_View
from .views import HomePage, contact_page

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('account/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('accounts.passwords.urls')),
    path('address/', RedirectView.as_view(url='/addresses')),
    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<pk>/', AddressUpdateView.as_view(), name='address-update'),
    path('contact/', contact_page, name='contact'),
    path('api/cart/', cart_detail_api_view, name='api_cart'),
    path('cart/', include(('carts.urls', 'carts'), namespace='carts')),
    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('billing/payment-method/create/', payment_method_create_view, name='billing-payment-create-method'),
    path('login/', LoginView.as_view(), name='login'),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/guest/', GuestRegisterView.as_view(), name='guest_register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    path('webhooks/mailchimp/', Mailchimp_Webhook_View.as_view(), name='webhooks-mailchimp'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
