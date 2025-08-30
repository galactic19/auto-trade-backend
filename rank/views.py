from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.normalizers import normalize_zero_padded_numbers
from utils.tr_request import TrRequest


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def get_rank_list(request, *args, **kwargs):
    # 당일 거래량 상위 요청
    # 순매수 잔략 순위로 확인
    user = request.user
    endpoint = '/api/dostk/rkinfo'
    header = {'api-id': 'ka10030'}

    body = {
        'mrkt_tp': '000',  # 시장구분 000:전체, 001:코스피, 101:코스닥
        'sort_tp': '1',  # 정렬구분 1:거래량, 2:거래회전율, 3:거래대금
        'mang_stk_incls': '0',
        # 관리종목포함 0:관리종목 포함, 1:관리종목 미포함, 3:우선주제외, 11:정리매매종목제외, 4:관리종목, 우선주제외, 5:증100제외, 6:증100마나보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 14:ETF제외, 15:스팩제외, 16:ETF+ETN제외
        'crd_tp': '0',  # 신용구분 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 8:신용대주
        'trde_qty_tp': '0',
        # 거래량구분 0:전체조회, 5:5천주이상, 10:1만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:500만주이상, 1000:백만주이상
        'pric_tp': '0',
        # 가격구분 0:전체조회, 1:1천원미만, 2:1천원이상, 3:1천원~2천원, 4:2천원~5천원, 5:5천원이상, 6:5천원~1만원, 10:1만원미만, 7:1만원이상, 8:5만원이상, 9:10만원이상
        'trde_prica_tp': '0',
        # 거래대금구분 0:전체조회, 1:1천만원이상, 3:3천만원이상, 4:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상
        'mrkt_open_tp': '0',  # 장운영구분 0:전체조회, 1:장중, 2:장전시간외, 3:장후시간외
        'stex_tp': '3',  # 거래소구분 1:KRX, 2:NXT 3.통합
    }

    try:
        data = TrRequest.request_post(user=user, endpoint=endpoint, body=body, header=header)
        en_data = data.json()
    except ValueError:
        return Response({'message': 'Invalid JSON response', 'raw': data.text}, status=data.status_code)

    ko_data = normalize_zero_padded_numbers(en_data)
    return Response(ko_data, status=data.status_code)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def get_top_trading_value(request, *args, **kwargs):
    # 거래대금 상위 요청
    # body 000:전체 001: 코스피, 101: 코스닥
    # ka10032
    user = request.user
    endpoint = '/api/dostk/rkinfo'
    header = {'api-id': 'ka10032'}

    body = {
        'mrkt_tp': '000',  # 시장구분 000:전체, 001:코스피, 101:코스닥
        'mang_stk_incls': '1',  # 관리종목포함 0:관리종목 미포함, 1:관리종목 포함
        'stex_tp': '3',  # 거래소구분 1:KRX, 2:NXT 3.통합
    }

    try:
        data = TrRequest.request_post(user=user, endpoint=endpoint, body=body, header=header)
        en_data = data.json()
    except ValueError:
        return Response({'message': 'Invalid JSON response', 'raw': data.text}, status=data.status_code)
    ko_data = normalize_zero_padded_numbers(en_data)
    return Response(ko_data, status=data.status_code)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def get_top_fi_trading_rank(request, *args, **kwargs):
    # 외국인기관 매매 상위 요청
    # ka90009
    user = request.user
    endpoint = '/api/dostk/rkinfo'
    header = {'api-id': 'ka90009'}

    body = {
        'mrkt_tp': '000',  # 시장구분 000:전체, 001:코스피, 101:코스닥
        'amt_qty_tp': '1',  # 금액수량구분 1:금액(천만), 2:수량(천)
        'qry_dt_tp': '1',  # 조회일자구분 0:조회일자 미포함, 1:조회일자 포함
        'date': '20241101',  # 날짜 YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
        'stex_tp': '1',  # 거래소구분 1:KRX, 2:NXT, 3:통합
    }

    try:
        data = TrRequest.request_post(user=user, endpoint=endpoint, body=body, header=header)
        en_data = data.json()
    except ValueError:
        return Response({'message': 'Invalid JSON response', 'raw': data.text}, status=data.status_code)

    ko_data = normalize_zero_padded_numbers(en_data)
    return Response(ko_data, status=data.status_code)
