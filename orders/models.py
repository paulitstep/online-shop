from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from online_shop.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Создан'),
    ('paid', 'Оплачен'),
    ('shipped', 'Доставлен'),
    ('refunded', 'Возврат'),
)


class OrderManagerQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart, active=True, status='created')
        if qs.count() == 1:
            order = qs.first()
        else:
            order = self.model.objects.create(billing_profile=billing_profile, cart=cart)
            created = True
        return order, created


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', null=True, blank=True, on_delete=models.CASCADE)
    shipping_address_final = models.TextField(blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(decimal_places=2, max_digits=10, default=5.00)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp', '-update']

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'order_id': self.order_id})

    def get_status(self):
        if self.status == 'refunded':
            return 'Возврат заказа'
        elif self.status == 'shipped':
            return 'Доставлен'
        return 'Доставляется'

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        total = cart_total + Decimal(shipping_total)
        self.total = total
        self.save()
        return total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        total = self.total
        if billing_profile and shipping_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

    if instance.shipping_address and not instance.shipping_address_final:
        instance.shipping_address_final = instance.shipping_address.get_address()


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart = instance
        cart_id = cart.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order = qs.first()
            order.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
