from datetime import datetime

import requests
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import UserToken
from trade_config.settings import MOTOO_DOMAIN


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_access_token(request, *args, **kwargs):
    # 키움증권 토큰 발급
    if request.method == 'GET':
        user = request.user

        # 토큰 요청 테스트
        params = {
            'grant_type': 'client_credentials',
            'appkey': user.api_key,
            'secretkey': user.secret_key,
        }
        response_data = fn_au10001(params).json()
        if response_data['token'] is None:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        rs_data = {
            'username': user.username,
            'token': response_data['token'],
            'return_msg': response_data['return_msg'],
            'expires_dt': response_data['expires_dt'],
        }
        # 생성 토큰을 저장.
        create_token, token_bool = _create_or_update_kiwoom_token(rs_data)

        if create_token:
            user_info = {
                'username': user.username,
            }
        else:
            user_info = {
                'username': None,
            }
        return Response(user_info, status=status.HTTP_200_OK)
    return None


def _get_user_token_or_none(user_obj):
    """
    안전하게 유저 토큰을 반환. 없으면 None.
    """
    return getattr(user_obj, 'user_token', None)


def _build_revocation_payload(user_obj, token):
    """
    외부 토큰 폐기 API 호출에 필요한 페이로드 생성.
    """
    return {
        'appkey': user_obj.api_key,
        'secretkey': user_obj.secret_key,
        'token': token.access_token,
    }


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def delete_access_token(request, *args, **kwargs):
    # 토큰 폐기 URL 함수
    user = request.user
    if not user or not user.is_authenticated:
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # username 대신 pk 기반 조회, 토큰을 미리 로딩
    user_obj = get_user_model().objects.select_related('user_token').get(pk=user.pk)

    token = _get_user_token_or_none(user_obj)
    if token is None:
        return Response({'message': 'No token found.'}, status=status.HTTP_404_NOT_FOUND)

    payload = _build_revocation_payload(user_obj, token)
    status_code = fn_au10002(payload)

    if status_code != status.HTTP_200_OK:
        return Response({'message': 'Token revocation failed.'}, status=status.HTTP_400_BAD_REQUEST)

    token.delete()
    return Response({'message': 'Token revoked successfully.'}, status=status.HTTP_200_OK)


def _create_or_update_kiwoom_token(user):
    # 키움의 유저의 토큰을 저장 및 업데이트
    expires_naive = datetime.strptime(user['expires_dt'], "%Y%m%d%H%M%S")
    expires_at = timezone.make_aware(expires_naive, timezone.get_current_timezone())

    # 실제 User 인스턴스 조회
    user_obj = get_user_model().objects.get(username=user['username'])

    return UserToken.objects.update_or_create(
        user=user_obj,
        defaults={
            'access_token':user['token'],
            'expires_in':  expires_at,
    }

    )

def fn_au10001(data):
    # 요청할 API URL
    # 토큰 요청
    # host = 'https://mockapi.kiwoom.com' # 모의투자
    endpoint = '/oauth2/token'
    url = MOTOO_DOMAIN + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    return response

def fn_au10002(data):
    # 접근토큰폐기
    endpoint = '/oauth2/revoke'
    url = MOTOO_DOMAIN + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)
    return response.status_code
