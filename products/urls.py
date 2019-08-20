from django.urls import path

from .views import (
    ProductRussianListView,
    ProductForeignListView,
    ProductDetectiveListView,
    ProductFantasyListView,
    ProductDetailSlugView,
)


urlpatterns = [
    path('russian/', ProductRussianListView.as_view(), name='russian_list'),
    path('foreign/', ProductForeignListView.as_view(), name='foreign_list'),
    path('detective/', ProductDetectiveListView.as_view(), name='detective_list'),
    path('fantasy/', ProductFantasyListView.as_view(), name='fantasy_list'),
    path('<slug>/', ProductDetailSlugView.as_view(), name='detail'),
]
