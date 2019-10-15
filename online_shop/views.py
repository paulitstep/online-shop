from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from carts.models import Cart
from .forms import ContactForm
from products.models import Product


class HomePage(ListView):
    queryset = Product.objects.all().order_by('?')
    template_name = 'home_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePage, self).get_context_data(*args, **kwargs)
        cart, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart
        return context


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'Contact Page',
        'content': 'Welcome to the contact page.',
        'form': contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({'message': 'Спасибо!'})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, 'contact/view.html', context)
