# 매수 관련 동작을 수행
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from utils.tr_request import TrRequest


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def buy_stock(request, *args, **kwargs):
    # 주식 매수 주문
    stock_code = '005930'
    ord_qty = str(1)
    ord_price = ''
    user = request.user
    endpoint = '/api/dostk/ordr'
    header = {'api-id': 'kt10000'}
    body = {
        'dmst_stex_tp': 'KRX',  # 국내거래소구분 KRX,NXT,SOR
        'stk_cd': stock_code,  # 종목코드
        'ord_qty': ord_qty,  # 주문수량
        'ord_uv': ord_price,  # 주문단가
        'trde_tp': '3',
        # 매매구분 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)
        'cond_uv': '',  # 조건단가
    }

    try:
        data = TrRequest.request_post(user=user, endpoint=endpoint, body=body, header=header)
    except ValueError:
        return Response({'message': 'Invalid JSON response'}, status=status.HTTP_400_BAD_REQUEST)

    print('주문에 대한 요청이 생성 되었습니다.')
    print(data.json())
    return Response(data.json(), status=data.status_code)