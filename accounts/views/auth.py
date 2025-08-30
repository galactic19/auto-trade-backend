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


# @api_view(['GET', 'POST'])
@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def get_access_token(request, *args, **kwargs):
    # 키움증권 토큰 발급
    """
    요청 시 키움증권 API를 통해 토큰을 발급받고 생성된 토큰을 저장하며, 사용자 정보를 반환하는 함수.

    Parameters:
        request (HttpRequest): API 요청 객체.
        *args: 추가적인 위치 인자.
        **kwargs: 추가적인 키워드 인자.

    Returns:
        Response: 처리된 사용자 정보와 HTTP 상태 코드 반환.

    Raises:
        None
    """
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
        print("create_token : ", create_token)
        print("token_bool : ", token_bool)

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
    사용자 객체에서 'user_token' 속성을 가져오거나, 속성이 없을 경우 None을 반환하는 함수.

    이 함수는 특정 사용자가 'user_token' 속성을 가지고 있는지 확인하고, 이를 반환하거나
    없는 경우 None을 반환하는 데 사용됨.

    Args:
        user_obj (Any): 'user_token' 속성 존재 여부를 확인할 사용자 객체.

    Returns:
        Any: 'user_token' 속성이 존재하면 해당 값을 반환하고, 없을 경우 None을 반환.
    """
    return getattr(user_obj, 'user_token', None)


def _build_revocation_payload(user_obj, token):
    """
    주어진 사용자 객체와 토큰을 사용하여 토큰 폐기 요청에 필요한 페이로드를 생성하는 함수.

    Parameters:
    user_obj (object): 사용자 객체로 API 키와 보안 키를 포함해야 함
    token (object): 액세스 토큰 정보를 담고 있는 객체

    Returns:
    dict: 토큰 폐기 요청에 필요한 페이로드를 딕셔너리 형태로 반환
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

    token = _get_user_token_or_none(user_obj) # 토큰 없을 시 None
    if token is None:
        return Response({'message': 'No token found.'}, status=status.HTTP_404_NOT_FOUND)

    payload = _build_revocation_payload(user_obj, token)
    status_code = fn_au10002(payload)

    if status_code != status.HTTP_200_OK:
        return Response({'message': 'Token revocation failed.'}, status=status.HTTP_400_BAD_REQUEST)

    token.delete()
    return Response({'message': 'Token revoked successfully.'}, status=status.HTTP_200_OK)


def _create_or_update_kiwoom_token(user):
    """
    주어진 사용자 데이터를 기반으로 Kiwoom 토큰을 생성하거나 갱신하는 함수

    사용자 데이터에서 만료 날짜와 시간을 파싱하고 이를 기준으로 토큰의 만료 시점과
    갱신 여부를 결정하며 UserToken 객체 생성 또는 갱신 작업을 수행함.

    Parameters:
        user (dict): 사용자 정보를 포함한 딕셔너리.
                     'username', 'expires_dt', 'token' 키를 포함해야 함.

    Returns:
        tuple: (UserToken 객체, 생성 여부). UserToken 객체와 새로 생성 여부를 반환함.
    """

    expires_naive = datetime.strptime(user['expires_dt'], "%Y%m%d%H%M%S")
    expires_at = timezone.make_aware(expires_naive, timezone.get_current_timezone())

    # 실제 User 인스턴스 조회
    user_obj = get_user_model().objects.get(username=user['username'])

    return UserToken.objects.update_or_create(
        user=user_obj,
        defaults={
            'access_token': user['token'],
            'expires_in': expires_at,
        }
    )


def fn_au10001(data):
    # 요청할 API URL
    # 토큰 요청
    endpoint = '/oauth2/token'
    url = MOTOO_DOMAIN + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',  # 컨텐츠타입
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)
    print('키움에서 온 요청을 표기 합니다.')
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
