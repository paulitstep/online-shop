from django.db import models

from billing.models import BillingProfile


LIST_OF_REGIONS = (
    ('Brest', 'Брестская область'),
    ('Vitebsk', 'Витебская область'),
    ('Gomel', 'Гомельская область'),
    ('Grodno', 'Гродненская область'),
    ('Minsk', 'Минская область'),
    ('Mogilev', 'Могилевская область'),
)

PAYMENT_CHOICES = (
    ('-', '-'),
    ('cash', 'Наличными'),
    ('credit_card', 'Карточкой'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, default='shipping')
    name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=120)
    payment = models.CharField(max_length=120, choices=PAYMENT_CHOICES, default='-')
    address = models.TextField(max_length=120)
    city = models.CharField(max_length=120, default='Минск')
    region = models.CharField(max_length=120, choices=LIST_OF_REGIONS, default='Minsk')
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return '{city},\n{address},\n{postal_code}'.format(
            city=self.city,
            address=self.address,
            postal_code=self.postal_code
        )
