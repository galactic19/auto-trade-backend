# 계좌 관리 파일
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.normalizers import normalize_zero_padded_numbers
from utils.tr_request import TrRequest


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def get_account_info(request, *args, **kwargs):
    # 계좌 평가 현황 조회.
    user = request.user
    if not user or not user.is_authenticated:
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    api_resp = TrRequest.request_post(user=user, endpoint='/api/dostk/acnt',
                                      body={'qry_tp': '0',  # 상장폐지조회구분 0:전체, 1:상장폐지종목제외
                                            'dmst_stex_tp': 'KRX'},
                                      header={'api-id': 'kt00004'})

    try:
        payload = api_resp.json()
    except ValueError:
        # JSON 파싱 실패 시 원문 텍스트를 그대로 반환
        return Response({'message': 'Invalid JSON response', 'raw': api_resp.text}, status=api_resp.status_code)
    normalized = normalize_zero_padded_numbers(payload)
    return Response(normalized, status=api_resp.status_code)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def get_cash_deposit_detail(request, *args, **kwargs):
    # 예수금 상세 현황 요청
    user = request.user
    if not user or not user.is_authenticated:
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    api_resp = TrRequest.request_post(user=user, endpoint='/api/dostk/acnt', body={'qry_tp': '2'},
                                      header={'api-id': 'kt00001'})

    try:
        payload = api_resp.json()
    except ValueError:
        # JSON 파싱 실패 시 원문 텍스트를 그대로 반환
        return Response({'message': 'Invalid JSON response', 'raw': api_resp.text}, status=api_resp.status_code)

    normalized = normalize_zero_padded_numbers(payload)
    return Response(normalized, status=api_resp.status_code)
