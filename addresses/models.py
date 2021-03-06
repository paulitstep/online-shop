from django.db import models
from django.urls import reverse

from billing.models import BillingProfile


LIST_OF_REGIONS = (
    ('Brest', 'Брестская область'),
    ('Vitebsk', 'Витебская область'),
    ('Gomel', 'Гомельская область'),
    ('Grodno', 'Гродненская область'),
    ('Minsk', 'Минская область'),
    ('Mogilev', 'Могилевская область'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, default='shipping')
    name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=120)
    address = models.TextField(max_length=120)
    city = models.CharField(max_length=120, default='Минск')
    region = models.CharField(max_length=120, choices=LIST_OF_REGIONS, default='Minsk')
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_absolute_url(self):
        return reverse('address-update', kwargs={'pk': self.pk})

    def get_short_address(self):
        return '{name}, {city}, {address}'.format(
            name=self.name,
            city=self.city,
            address=self.address
        )

    def get_address(self):
        return '{name},\n{city},\n{mobile},\n{address},\n{postal_code}'.format(
            name=self.name,
            city=self.city,
            mobile=self.mobile,
            address=self.address,
            postal_code=self.postal_code
        )
