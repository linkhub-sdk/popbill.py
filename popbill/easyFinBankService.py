# -*- coding: utf-8 -*-
# Module for Popbill EasyFinBank API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Jeong Yohan (code@linkhub.co.kr)
# Written : 2020-06-01
# Thanks for your interest.

from .base import PopbillBase, PopbillException

class EasyFinBankService(PopbillBase):
    """ 팝빌 계좌조회 API Service Implementation. """

    def __init__(self, LinkID, SecretKey):
        """ 생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("180")

    def registBankAccount(self, CorpNum, AccountInfo, UserID=None):

        uri = "/EasyFin/Bank/BankAccount/Regist"
        uri += "?UsePeriod="+AccountInfo.UsePeriod

        postData = self._stringtify(AccountInfo)

        return self._httppost(uri, postData, CorpNum, UserID)

    def updateBankAccount(self, CorpNum, AccountInfo, UserID=None):

        uri = "/EasyFin/Bank/BankAccount/"+AccountInfo.BankCode+"/"+AccountInfo.AccountNumber+"/Update"

        postData = self._stringtify(AccountInfo)

        return self._httppost(uri, postData, CorpNum, UserID)


    def closeBankAccount(self, CorpNum, BankCode, AccountNumber, CloseType, UserID=None):

        uri = "/EasyFin/Bank/BankAccount/Close"
        uri += '?BankCode=' + BankCode
        uri += '&AccountNumber=' + AccountNumber
        uri += '&CloseType=' + CloseType

        return self._httppost(uri, '', CorpNum, UserID)
        
    def revokeCloseBankAccount(self, CorpNum, BankCode, AccountNumber, CloseType, UserID=None):

        uri = "/EasyFin/Bank/BankAccount/RevokeClose"
        uri += '?BankCode=' + BankCode
        uri += '&AccountNumber=' + AccountNumber

        return self._httppost(uri, '', CorpNum, UserID)


    def getBankAccountMgtURL(self, CorpNum, UserID=None):
        """ 계좌 관리 팝업 URL
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                계좌 관리 팝업 URL
            raise
                PopbillException
        """
        return self._httpget('/EasyFin/Bank?TG=BankAccount', CorpNum, UserID).url

    def getBankAccountInfo(self, CorpNum, BankCode, AccountNumber, UserID=None):

        uri = "/EasyFin/Bank/BankAccount/" + BankCode + "/"+ AccountNumber

        return self._httpget(uri, CorpNum, UserID)

    def listBankAccount(self, CorpNum, UserID=None):
        """ 계좌 목록 확인
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                계좌 목록
            raise
                PopbillException
        """

        return self._httpget('/EasyFin/Bank/ListBankAccount', CorpNum, UserID)

    def requestJob(self, CorpNum, BankCode, AccountNumber, SDate, EDate, UserID=None):
        """ 수집 요청
            args
                CorpNum : 팝빌회원 사업자번호
                BankCode : 은행코드
                AccountNumber : 계좌번호
                SDate : 시작일자, 표시형식(yyyyMMdd)
                EDate : 종료일자, 표시형식(yyyyMMdd)
                UserID : 팝빌회원 아이디
            return
                작업아이디 (jobID)
            raise
                PopbillException
        """
        if BankCode == None or BankCode == '':
            raise PopbillException(-99999999, "은행코드가 입력되지 않았습니다.")

        if AccountNumber == None or AccountNumber == '':
            raise PopbillException(-99999999, "계좌번호가 입력되지 않았습니다.")

        if SDate == None or SDate == '':
            raise PopbillException(-99999999, "시작일자가 입력되지 않았습니다.")

        if EDate == None or EDate == '':
            raise PopbillException(-99999999, "종료일자가 입력되지 않았습니다.")

        uri = '/EasyFin/Bank/BankAccount'
        uri += '?AccountNumber=' + AccountNumber
        uri += '&BankCode=' + BankCode
        uri += '&SDate=' + SDate
        uri += '&EDate=' + EDate

        return self._httppost(uri, "", CorpNum, UserID).jobID

    def getJobState(self, CorpNum, JobID, UserID=None):
        """ 수집 상태 확인
            args
                CorpNum : 팝빌회원 사업자번호
                JobID : 작업아이디
                UserID : 팝빌회원 아이디
            return
                수집 상태 정보
            raise
                PopbillException
        """
        if JobID == None or len(JobID) != 18:
            raise PopbillException(-99999999, "작업아이디(jobID)가 올바르지 않습니다.")

        return self._httpget('/EasyFin/Bank/' + JobID + '/State', CorpNum, UserID)

    def listActiveJob(self, CorpNum, UserID=None):
        """ 수집 상태 목록 확인
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                수집 상태 정보 목록
            raise
                PopbillException
        """

        return self._httpget('/EasyFin/Bank/JobList', CorpNum, UserID)

    def search(self, CorpNum, JobID, TradeType, SearchString, Page, PerPage, Order, UserID=None):
        """ 수집 결과 조회
            args
                CorpNum : 팝빌회원 사업자번호
                JobID : 작업아이디
                TradeType : 거래유형 배열, I-입금, O-출금
                SearchString : 조회 검색어, 입금/출금액, 메모, 적요 like 검색
                Page : 페이지 번호
                PerPage : 페이지당 목록 개수, 최대 1000개
                Order : 정렬 방향, D-내림차순, A-오름차순
                UserID : 팝빌회원 아이디
            return
                수집 결과 정보
            raise
                PopbillException
        """
        if JobID == None or len(JobID) != 18:
            raise PopbillException(-99999999, "작업아이디(jobID)가 올바르지 않습니다.")

        uri = '/EasyFin/Bank/' + JobID
        uri += '?TradeType=' + ','.join(TradeType)

        if SearchString is not None:
            uri += '&SearchString=' + SearchString

        uri += '&Page=' + str(Page)
        uri += '&PerPage=' + str(PerPage)
        uri += '&Order=' + Order

        return self._httpget(uri, CorpNum, UserID)

    def summary(self, CorpNum, JobID, TradeType, SearchString, UserID=None):
        """ 수집 결과 요약정보
            args
                CorpNum : 팝빌회원 사업자번호
                JobID : 작업아이디
                TradeType : 거래유형 배열, I-입금, O-출금
                SearchString : 조회 검색어, 입금/출금액, 메모, 적요 like 검색
                UserID : 팝빌회원 아이디
            return
                수집 결과 정보
            raise
                PopbillException
        """
        if JobID == None or len(JobID) != 18:
            raise PopbillException(-99999999, "작업아이디(jobID)가 올바르지 않습니다.")

        uri = '/EasyFin/Bank/' + JobID +'/Summary'
        uri += '?TradeType=' + ','.join(TradeType)

        if SearchString is not None:
            uri += '&SearchString=' + SearchString

        return self._httpget(uri, CorpNum, UserID)

    def saveMemo(self, CorpNum, TID, Memo, UserID=None):
        """ 수집 요청
            args
                CorpNum : 팝빌회원 사업자번호
                TID : 거래내역 아이디, Search API 거래내역 반환항목 중 tid
                Memo : 메모
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if TID == None or TID == '':
            raise PopbillException(-99999999, "거래내역 아이디가 입력되지 않았습니다.")

        uri = '/EasyFin/Bank/SaveMemo'
        uri += '?TID=' + TID
        uri += '&Memo=' + Memo

        return self._httppost(uri, "", CorpNum, UserID)

    def getFlatRatePopUpURL(self, CorpNum, UserID=None):
        """ 정액제 서비스 신청 URL
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                계좌 관리 팝업 URL
            raise
                PopbillException
        """
        return self._httpget('/EasyFin/Bank?TG=CHRG', CorpNum, UserID).url

    def getFlatRateState(self, CorpNum, BankCode, AccountNumber, UserID=None):
        """ 정액제 서비스 상태 확인
            args
                CorpNum : 팝빌회원 사업자번호
                BankCode : 은행코드
                AccountNumber : 계좌번호
                UserID : 팝빌회원 아이디
            return
                정액제 서비스 상태 정보
            raise
                PopbillException
        """

        if BankCode == None or BankCode == '':
            raise PopbillException(-99999999, "은행코드가 입력되지 않았습니다.")

        if AccountNumber == None or AccountNumber == '':
            raise PopbillException(-99999999, "계좌번호가 입력되지 않았습니다.")

        uri = '/EasyFin/Bank/Contract/' + BankCode +'/' + AccountNumber

        return self._httpget(uri, CorpNum, UserID)

    def getChargeInfo(self, CorpNum, UserID=None):
        """ 과금정보 확인
            args
                CorpNum : 회원 사업자번호
                UserID : 팝빌 회원아이디
            return
                과금정보 객체
            raise
                PopbillException
        """

        return self._httpget('/EasyFin/Bank/ChargeInfo', CorpNum, UserID)

class BankAccountInfo(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
