from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        labels = {
            'name': 'Имя и фамилия',
            'mobile': 'Контактный телефон',
            'payment': 'Оплата',
            'address': 'Адрес (улица, дом, корпус, квартира)',
            'city': 'Город',
            'region': 'Область',
            'postal_code': 'Почтовый индекс'
        }
        fields = [
            'name',
            'mobile',
            'payment',
            'address',
            'city',
            'region',
            'postal_code'
        ]
