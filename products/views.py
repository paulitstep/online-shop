from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from .models import Product


class ProductRussianListView(ListView):
    queryset = Product.objects.filter(category__icontains='russian')
    template_name = 'products/russian_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductRussianListView, self).get_context_data(*args, **kwargs)
        cart, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart
        return context


class ProductForeignListView(ListView):
    queryset = Product.objects.filter(category__icontains='foreign')
    template_name = 'products/foreign_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductForeignListView, self).get_context_data(*args, **kwargs)
        cart, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart
        return context


class ProductDetectiveListView(ListView):
    queryset = Product.objects.filter(category__icontains='detective')
    template_name = 'products/detective_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetectiveListView, self).get_context_data(*args, **kwargs)
        cart, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart
        return context


class ProductFantasyListView(ListView):
    queryset = Product.objects.filter(category__icontains='fantasy')
    template_name = 'products/fantasy_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductFantasyListView, self).get_context_data(*args, **kwargs)
        cart, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart
        return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'


class ProductFeaturedDetailView(DetailView):
    template_name = 'products/featured_detail.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Такого товара не существует')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Uhhm')

        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance
