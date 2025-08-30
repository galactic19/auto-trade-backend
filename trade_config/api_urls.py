# api 경로들만 여기로 모음 모든 url 은 api/v2/...
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('rank/', include('rank.urls')),
    path('order/', include('order.urls')),
]