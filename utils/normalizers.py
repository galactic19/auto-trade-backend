from decimal import Decimal, InvalidOperation

# 0-패딩 숫자 문자열 필드 목록
ZERO_PAD_NUM_FIELDS = {
    # 최상위 응답의 정규화 대상
    "entr",
    "profa_ch",
    "bncr_profa_ch",
    "nxdy_bncr_sell_exct",
    "fc_stk_krw_repl_set_amt",
    "crd_grnta_ch",
    "crd_grnt_ch",
    "add_grnt_ch",
    "etc_profa",
    "uncl_stk_amt",
    "shrts_prica",
    "crd_set_grnta",
    "chck_ina_amt",
    "etc_chck_ina_amt",
    "crd_grnt_ruse",
    "knx_asset_evltv",
    "elwdpst_evlta",
    "crd_ls_rght_frcs_amt",
    "lvlh_join_amt",
    "lvlh_trns_alowa",
    "repl_amt",
    "remn_repl_evlta",
    "trst_remn_repl_evlta",
    "bncr_remn_repl_evlta",
    "profa_repl",
    "crd_grnta_repl",
    "crd_grnt_repl",
    "add_grnt_repl",
    "rght_repl_amt",
    "pymn_alow_amt",
    "wrap_pymn_alow_amt",
    "ord_alow_amt",
    "bncr_buy_alowa",
    "20stk_ord_alow_amt",
    "30stk_ord_alow_amt",
    "40stk_ord_alow_amt",
    "50stk_ord_alow_amt",
    "60stk_ord_alow_amt",
    "100stk_ord_alow_amt",
    "ch_uncla",
    "ch_uncla_dlfe",
    "ch_uncla_tot",
    "crd_int_npay",
    "int_npay_amt_dlfe",
    "int_npay_amt_tot",
    "etc_loana",
    "etc_loana_dlfe",
    "etc_loan_tot",
    "nrpy_loan",
    "loan_sum",
    "ls_sum",
    "crd_grnt_rt",  # 소수점 포함 0-패딩 문자열
    "mdstrm_usfe",
    "min_ord_alow_yn",
    "loan_remn_evlt_amt",
    "dpst_grntl_remn",
    "sell_grntl_remn",
    "d1_entra",
    "d1_slby_exct_amt",
    "d1_buy_exct_amt",
    "d1_out_rep_mor",
    "d1_sel_exct_amt",
    "d1_pymn_alow_amt",
    "d2_entra",
    "d2_slby_exct_amt",
    "d2_buy_exct_amt",
    "d2_out_rep_mor",
    "d2_sel_exct_amt",
    "d2_pymn_alow_amt",
    # 리스트(stk_entr_prst) 내부 항목 정규화 대상
    "fx_entr",
    "fc_krw_repl_evlta",
    "fc_trst_profa",
    "pymn_alow_amt",  # 중복 허용: 상위/하위 동일 키 모두 처리
    "pymn_alow_amt_entr",
    "ord_alow_amt_entr",
    "fc_uncla",
    "fc_ch_uncla",
    "dly_amt",
    "d1_fx_entr",
    "d2_fx_entr",
    "d3_fx_entr",
    "d4_fx_entr",
    # 호가잔량상위(bid_req_upper) 리스트 내부 항목 정규화 대상
    "cur_prc",
    "pred_pre",
    "trde_qty",
    "tot_sel_req",
    "tot_buy_req",
    "netprps_req",
    "buy_rt",
    # 당일거래량상위(tdy_trde_qty_upper) 리스트 내부 항목 정규화 대상
    "flu_rt",
    "pred_rt",
    "trde_tern_rt",
    "trde_amt",
    "opmr_trde_qty",
    "opmr_pred_rt",
    "opmr_trde_rt",
    "opmr_trde_amt",
    "af_mkrt_trde_qty",
    "af_mkrt_pred_rt",
    "af_mkrt_trde_rt",
    "af_mkrt_trde_amt",
    "bf_mkrt_trde_qty",
    "bf_mkrt_pred_rt",
    "bf_mkrt_trde_rt",
    "bf_mkrt_trde_amt",
    # 거래대금상위(trde_prica_upper) 리스트 내부 항목 정규화 대상
    "sel_bid",
    "buy_bid",
    "now_trde_qty",
    "pred_trde_qty",
    "trde_prica",
    # 외국인기관매매상위(frgnr_orgn_trde_upper) 리스트 내부 항목 정규화 대상
    # 금액/수량 필드는 0-패딩 숫자 문자열일 가능성이 높아 정규화 대상에 포함
    "for_netslmt_amt",
    "for_netslmt_qty",
    "for_netprps_amt",
    "for_netprps_qty",
    "orgn_netslmt_amt",
    "orgn_netslmt_qty",
    "orgn_netprps_amt",
    "orgn_netprps_qty",
}

# 영문 키 → 한글 키 매핑
EN_TO_KO = {
    "entr": "예수금",
    "profa_ch": "주식증거금현금",
    "bncr_profa_ch": "수익증권증거금현금",
    "nxdy_bncr_sell_exct": "익일수익증권매도정산대금",
    "fc_stk_krw_repl_set_amt": "해외주식원화대용설정금",
    "crd_grnta_ch": "신용보증금현금",
    "crd_grnt_ch": "신용담보금현금",
    "add_grnt_ch": "추가담보금현금",
    "etc_profa": "기타증거금",
    "uncl_stk_amt": "미수확보금",
    "shrts_prica": "공매도대금",
    "crd_set_grnta": "신용설정평가금",
    "chck_ina_amt": "수표입금액",
    "etc_chck_ina_amt": "기타수표입금액",
    "crd_grnt_ruse": "신용담보재사용",
    "knx_asset_evltv": "코넥스기본예탁금",
    "elwdpst_evlta": "ELW예탁평가금",
    "crd_ls_rght_frcs_amt": "신용대주권리예정금액",
    "lvlh_join_amt": "생계형가입금액",
    "lvlh_trns_alowa": "생계형입금가능금액",
    "repl_amt": "대용금평가금액(합계)",
    "remn_repl_evlta": "잔고대용평가금액",
    "trst_remn_repl_evlta": "위탁대용잔고평가금액",
    "bncr_remn_repl_evlta": "수익증권대용평가금액",
    "profa_repl": "위탁증거금대용",
    "crd_grnta_repl": "신용보증금대용",
    "crd_grnt_repl": "신용담보금대용",
    "add_grnt_repl": "추가담보금대용",
    "rght_repl_amt": "권리대용금",
    "pymn_alow_amt": "출금가능금액",
    "wrap_pymn_alow_amt": "랩출금가능금액",
    "ord_alow_amt": "주문가능금액",
    "bncr_buy_alowa": "수익증권매수가능금액",
    "20stk_ord_alow_amt": "20%종목주문가능금액",
    "30stk_ord_alow_amt": "30%종목주문가능금액",
    "40stk_ord_alow_amt": "40%종목주문가능금액",
    "50stk_ord_alow_amt": "50%종목주문가능금액",
    "60stk_ord_alow_amt": "60%종목주문가능금액",
    "100stk_ord_alow_amt": "100%종목주문가능금액",
    "ch_uncla": "현금미수금",
    "ch_uncla_dlfe": "현금미수연체료",
    "ch_uncla_tot": "현금미수금합계",
    "crd_int_npay": "신용이자미납",
    "int_npay_amt_dlfe": "신용이자미납연체료",
    "int_npay_amt_tot": "신용이자미납합계",
    "etc_loana": "기타대여금",
    "etc_loana_dlfe": "기타대여금연체료",
    "etc_loan_tot": "기타대여금합계",
    "nrpy_loan": "미상환융자금",
    "loan_sum": "융자금합계",
    "ls_sum": "대주금합계",
    "crd_grnt_rt": "신용담보비율",
    "mdstrm_usfe": "중도이용료",
    "min_ord_alow_yn": "최소주문가능금액",
    "loan_remn_evlt_amt": "대출총평가금액",
    "dpst_grntl_remn": "예탁담보대출잔고",
    "sell_grntl_remn": "매도담보대출잔고",
    "d1_entra": "d+1추정예수금",
    "d1_slby_exct_amt": "d+1매도매수정산금",
    "d1_buy_exct_amt": "d+1매수정산금",
    "d1_out_rep_mor": "d+1미수변제소요금",
    "d1_sel_exct_amt": "d+1매도정산금",
    "d1_pymn_alow_amt": "d+1출금가능금액",
    "d2_entra": "d+2추정예수금",
    "d2_slby_exct_amt": "d+2매도매수정산금",
    "d2_buy_exct_amt": "d+2매수정산금",
    "d2_out_rep_mor": "d+2미수변제소요금",
    "d2_sel_exct_amt": "d+2매도정산금",
    "d2_pymn_alow_amt": "d+2출금가능금액",
    "stk_entr_prst": "종목별예수금",
    # 종목별예수금 리스트 내부 항목
    "crnc_cd": "통화코드",
    "fx_entr": "외화예수금",
    "fc_krw_repl_evlta": "원화대용평가금",
    "fc_trst_profa": "해외주식증거금",
    "pymn_alow_amt_entr": "출금가능금액(예수금)",
    "ord_alow_amt_entr": "주문가능금액(예수금)",
    "fc_uncla": "외화미수(합계)",
    "fc_ch_uncla": "외화현금미수금",
    "dly_amt": "연체료",
    "d1_fx_entr": "d+1외화예수금",
    "d2_fx_entr": "d+2외화예수금",
    "d3_fx_entr": "d+3외화예수금",
    "d4_fx_entr": "d+4외화예수금",
    "acnt_nm": "계좌명",
    "brch_nm": "지점명",
    "tot_est_amt": "유가잔고평가액",
    "aset_evlt_amt": "예탁자산평가액",
    "tot_pur_amt": "총매입금액",
    "prsm_dpst_aset_amt": "추정예탁자산",
    "tot_grnt_sella": "매도담보대출금",
    "tdy_lspft_amt": "당일투자원금",
    "invt_bsamt": "당월투자원금",
    "lspft_amt": "누적투자원금",
    "tdy_lspft": "당일투자손익",
    "lspft2": "당월투자손익",
    "lspft": "누적손익",
    "tdy_lspft_rt": "당일손익율",
    "lspft_ratio": "당월손익율",
    "lspft_rt": "누적손익율",
    "stk_acnt_evlt_prst": "종목별계좌평가현황",
    # 종목별계좌평가현황 리스트 내부 항목
    "stk_cd": "종목코드",
    "stk_nm": "종목명",
    "rmnd_qty": "보유수량",
    "avg_prc": "평균단가",
    "cur_prc": "현재가",
    "evlt_amt": "평가금액",
    "pl_amt": "손익금액",
    "pl_rt": "손익율",
    "loan_dt": "대출일",
    "pur_amt": "매입금액",
    "setl_remn": "결제잔고",
    "pred_buyq": "전일매수수량",
    "pred_sellq": "전일매도수량",
    "tdy_buyq": "금일매수수량",
    "tdy_sellq": "금일매도수량",
    # 호가잔량상위 응답 매핑
    "bid_req_upper": "호가잔량상위",
    "pred_pre_sig": "전일대비기호",
    "pred_pre": "전일대비",
    "trde_qty": "거래량",
    "tot_sel_req": "총매도잔량",
    "tot_buy_req": "총매수잔량",
    "netprps_req": "순매수잔량",
    "buy_rt": "매수비율",
    # 당일거래량상위 응답 매핑
    "tdy_trde_qty_upper": "당일거래량상위",
    "flu_rt": "등락률",
    "pred_rt": "전일비",
    "trde_tern_rt": "거래회전율",
    "trde_amt": "거래금액",
    "opmr_trde_qty": "장중거래량",
    "opmr_pred_rt": "장중전일비",
    "opmr_trde_rt": "장중거래회전율",
    "opmr_trde_amt": "장중거래금액",
    "af_mkrt_trde_qty": "장후거래량",
    "af_mkrt_pred_rt": "장후전일비",
    "af_mkrt_trde_rt": "장후거래회전율",
    "af_mkrt_trde_amt": "장후거래금액",
    "bf_mkrt_trde_qty": "장전거래량",
    "bf_mkrt_pred_rt": "장전전일비",
    "bf_mkrt_trde_rt": "장전거래회전율",
    "bf_mkrt_trde_amt": "장전거래금액",
    # 거래대금상위 응답 매핑
    "trde_prica_upper": "거래대금상위",
    "now_rank": "현재순위",
    "pred_rank": "전일순위",
    "sel_bid": "매도호가",
    "buy_bid": "매수호가",
    "now_trde_qty": "현재거래량",
    "pred_trde_qty": "전일거래량",
    "trde_prica": "거래대금",
    # 외국인기관매매상위 응답 매핑
    "frgnr_orgn_trde_upper": "외국인기관매매상위",
    "for_netslmt_stk_cd": "외인순매도종목코드",
    "for_netslmt_stk_nm": "외인순매도종목명",
    "for_netslmt_amt": "외인순매도금액",
    "for_netslmt_qty": "외인순매도수량",
    "for_netprps_stk_cd": "외인순매수종목코드",
    "for_netprps_stk_nm": "외인순매수종목명",
    "for_netprps_amt": "외인순매수금액",
    "for_netprps_qty": "외인순매수수량",
    "orgn_netslmt_stk_cd": "기관순매도종목코드",
    "orgn_netslmt_stk_nm": "기관순매도종목명",
    "orgn_netslmt_amt": "기관순매도금액",
    "orgn_netslmt_qty": "기관순매도수량",
    "orgn_netprps_stk_cd": "기관순매수종목코드",
    "orgn_netprps_stk_nm": "기관순매수종목명",
    "orgn_netprps_amt": "기관순매수금액",
    "orgn_netprps_qty": "기관순매수수량",

}


def _normalize_numeric_string(val: str) -> str | None:
    """
    '000000000123.45' 같은 0-패딩 숫자 문자열을 사람이 읽기 쉬운 문자열로 변환.
    정상이 아닌 값은 None 반환.
    """
    stripped = val.lstrip("0") or "0"
    try:
        dec = Decimal(stripped)
        return format(dec, "f")
    except InvalidOperation:
        return None


# ... existing code ...


def normalize_zero_padded_numbers(payload):
    """
    응답 페이로드에 대해:
      - ZERO_PAD_NUM_FIELDS에 해당하는 0-패딩 숫자 문자열을 정규화
      - EN_TO_KO 매핑을 이용해 키를 한글로 치환
    dict, list(또는 tuple) 모두 재귀적으로 처리합니다.
    """
    # dict 처리: 값 정규화 → 키 한글 치환
    if isinstance(payload, dict):
        new_dict = {}
        for key, value in payload.items():
            # 하위 구조 재귀 처리
            if isinstance(value, (dict, list, tuple)):
                normalized_value = normalize_zero_padded_numbers(value)
            elif isinstance(value, str) and key in ZERO_PAD_NUM_FIELDS:
                normalized_value = _normalize_numeric_string(value)
            else:
                normalized_value = value

            # 키 한글 치환
            # new_key = EN_TO_KO.get(key, key)
            new_key = EN_TO_KO.get(key, key)
            new_dict[new_key] = normalized_value
        return new_dict

    # 시퀀스 처리: 각 요소를 재귀 처리
    if isinstance(payload, (list, tuple)):
        return [normalize_zero_padded_numbers(item) for item in payload]

    # 기타 타입은 그대로 반환
    return payload


__all__ = ["ZERO_PAD_NUM_FIELDS", "EN_TO_KO", "normalize_zero_padded_numbers"]
