from django.urls import path

from rank import views

app_name = 'rank'

urlpatterns = [
    path('', views.get_rank_list, name='get_rank_list'),
    path('trade/value/', views.get_top_trading_value, name='get_top_trading_value'),
    path('trade/fi/', views.get_top_fi_trading_rank, name='get_top_fi_trading_rank'),
]
