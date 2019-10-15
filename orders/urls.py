from django.urls import path, re_path

from .views import OrderListView, OrderDetailView


urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    re_path('(?P<order_id>[0-9A-Za-z]+)/', OrderDetailView.as_view(), name='detail'),
]
