from django.urls import path

from order.views import sell_views, buy_views

app_name = 'order'

urlpatterns = [
    path('buy/', buy_views.buy_stock, name='buy_stock'),
]