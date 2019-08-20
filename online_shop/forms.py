from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(label='ФИО', widget=forms.TextInput(
        attrs={'class': 'form-control'}
    )
    )
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(
        attrs={'class': 'form-control'}
    )
    )
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(
        attrs={'class': 'form-control'}
    )
    )
