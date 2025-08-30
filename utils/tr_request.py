import os
import logging
from urllib.parse import urljoin
import requests
from django.contrib.auth import get_user_model

UserModel = get_user_model()

ENV_KIWOOM_DOMAIN = 'KIWOOM_DOMAIN'
ENV_MOTOO_DOMAIN = 'MOTOO_DOMAIN'
logger = logging.getLogger(__name__)


class TrRequest:
    """
    TR 요청 관련 기능을 제공하는 클래스.

    이 클래스는 TR 요청과 관련된 메타정보 헤더 생성, 사용자 토큰 주입, 세션 재사용 등을
    제공하여 HTTP 요청 효율성을 개선합니다. TR 요청에 요구되는 다양한 형식을 지원하며,
    단일 클래스에서 요청과 관련된 로직을 캡슐화합니다.

    :ivar user: 요청에 사용할 사용자 정보.
    :type user: UserModel | None
    :ivar header: TR 요청에 사용할 헤더 정보.
    :type header: dict
    :ivar body: TR 요청의 본문 데이터.
    :type body: dict
    """
    # 클래스 레벨 세션: 커넥션 풀 재사용
    _session = requests.Session()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user', None)
        self.header = kwargs.setdefault('header', {})
        self.body = kwargs.setdefault('body', {})

    @staticmethod
    def _build_headers(header: dict) -> dict:
        """
        기본 헤더를 생성한다.
        """
        cont_yn = header.get('cont-yn', 'N')
        next_key = header.get('next-key', '')
        return {
            'Content-Type': 'application/json;charset=UTF-8',
            'cont-yn': cont_yn,
            'next-key': next_key,
        }

    def _merge_tr_headers(self) -> None:
        """
        TR 메타정보를 헤더에 병합한다.
        """
        if self.header is None or not isinstance(self.header, dict):
            raise ValueError('TR 구분 정보는 dict 타입이어야 합니다.')
        base = self._build_headers(self.header)
        base.update(self.header)
        self.header = base

    @staticmethod
    def _inject_user_token(header: dict, user: UserModel | None) -> dict:
        """
        사용자 액세스 토큰을 헤더에 주입. 없으면 authorization 키 제거.
        """
        try:
            if isinstance(user, UserModel):
                username = getattr(user, 'username', None)
                if username:
                    user_obj = UserModel.objects.select_related('user_token').get(username=username)
                    token_obj = getattr(user_obj, 'user_token', None)
                    access_token = getattr(token_obj, 'access_token', None)
                    if access_token:
                        header['authorization'] = f'Bearer {access_token}'
                        return header
        except UserModel.DoesNotExist:
            logger.warning('지정된 사용자(username=%s)를 찾을 수 없습니다.', getattr(user, 'username', None))
        header.pop('authorization', None)
        return header

    def get_user_info(self):
        """
        인스턴스 헤더에 사용자 토큰 반영 후 헤더 반환 (하위 호환 메서드).
        """
        self._inject_user_token(self.header, self.user)
        self._merge_tr_headers()
        return self.header

    def get_tr(self):
        # Tr 요청에 대한 header 생성
        # get_tr는 기존 호환성을 위해 유지. 내부적으로 검증/병합만 수행.
        self._merge_tr_headers()
        return self.header

    @staticmethod
    def _resolve_base_url(real: str | None) -> str:
        base = os.getenv(ENV_KIWOOM_DOMAIN) if real == 'R' else os.getenv(ENV_MOTOO_DOMAIN)
        if not base:
            raise RuntimeError(f'도메인 환경변수 누락: {ENV_KIWOOM_DOMAIN} 또는 {ENV_MOTOO_DOMAIN}')
        return base.rstrip('/')

    @classmethod
    def request_post(cls, endpoint: str, *, user: UserModel | None = None,
                     body: dict | None = None, header: dict | None = None,
                     real: str | None = None):
        """
        인스턴스 생성 없이 POST 요청을 실행.
        - 세션을 재사용하여 성능/자원 효율 개선
        - user : User Object,
        - headers: dict : cont-yn, next-key, api-id(TR)
        - body : dict : 필요한 Body 요청 값.
        """
        logger.debug('TR POST 요청: endpoint=%s real=%s', endpoint, real)
        if not endpoint:
            raise ValueError('endpoint가 필요합니다.')

        body = body or {}
        header = header or {}

        base = cls._resolve_base_url(real)
        headers = cls._build_headers(header)
        headers.update(header)
        headers = cls._inject_user_token(headers, user)

        url = urljoin(base + '/', str(endpoint).lstrip('/'))
        return cls._session.post(url, headers=headers, json=body)
