from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        labels = {
            'name': 'Имя и фамилия',
            'mobile': 'Контактный телефон',
            'address': 'Адрес (улица, дом, корпус, квартира)',
            'city': 'Город',
            'region': 'Область',
            'postal_code': 'Почтовый индекс'
        }
        fields = [
            'name',
            'mobile',
            'address',
            'city',
            'region',
            'postal_code'
        ]


class AddressCheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        labels = {
            'name': 'Имя и фамилия',
            'mobile': 'Контактный телефон',
            'address': 'Адрес (улица, дом, корпус, квартира)',
            'city': 'Город',
            'region': 'Область',
            'postal_code': 'Почтовый индекс'
        }
        fields = [
            'name',
            'mobile',
            'address',
            'city',
            'region',
            'postal_code'
        ]
