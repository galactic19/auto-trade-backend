from django.urls import path

from accounts.views.account import get_account_info, get_cash_deposit_detail
from accounts.views.auth import get_access_token, delete_access_token


app_name = 'accounts'

urlpatterns = [
    path('', get_access_token, name='get_access_token'), # 키움에서 토큰을 발급하는 URL
    path('me/', get_access_token, name='get_access_token'), # 키움에서 토큰을 발급하는 URL
    path('delete/', delete_access_token, name='delete_access_token'), # 키움 토큰을 삭제하는 URL
    # 계좌 관련 url
    path('account/', get_account_info, name='get_account_info'),
    path('account/me/', get_account_info, name='get_account_info'),
    path('account/detail/', get_cash_deposit_detail, name='get_cash_deposit_detail'),
]
