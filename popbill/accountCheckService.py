# -*- coding: utf-8 -*-
# Module for Popbill Closedown API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Jeong Yohan (code@linkhubcorp.com)
# Written : 2020-06-24
# Updated : 2021-12-22
# Thanks for your interest.

from .base import PopbillBase,PopbillException
try:
    from urllib import parse as parse
except ImportError:
    import urllib as parse
import re

class AccountCheckService(PopbillBase):
    """ 팝빌 예금주조회 API Service Implementation. """

    def __init__(self,LinkID,SecretKey):
        """생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """

        super(self.__class__,self).__init__(LinkID,SecretKey)
        self._addScope("182")
        self._addScope("183")

    def getChargeInfo(self, CorpNum, UserID = None, ServiceType = None):
        """ 과금정보 확인
            args
                CorpNum : 회원 사업자번호
                UserID : 팝빌 회원아이디
            return
                과금정보 객체
            raise
                PopbillException
        """
        url = '/EasyFin/AccountCheck/ChargeInfo'
        if ServiceType != None and ServiceType != "":
            url = '/EasyFin/AccountCheck/ChargeInfo?serviceType=' + parse.quote(ServiceType)

        return self._httpget(url, CorpNum, UserID)

    def getUnitCost(self, CorpNum, UserID = None, ServiceType = None):
        """ 예금주조회 단가 확인.
            args
                CorpNum : 팝빌회원 사업자번호
            return
                발행단가 by float
            raise
                PopbillException
        """
        url = '/EasyFin/AccountCheck/UnitCost'
        if ServiceType != None and ServiceType != "":
            url = '/EasyFin/AccountCheck/UnitCost?serviceType=' + parse.quote(ServiceType)

        result = self._httpget(url, CorpNum, UserID)

        return float(result.unitCost)

    def checkAccountInfo(self, CorpNum, BankCode, AccountNumber, UserID = None):

        if BankCode == None or BankCode == "" :
            raise PopbillException(-99999999,"기관코드가 입력되지 않았습니다.")

        if len(BankCode) != 4 :
            raise PopbillException(-99999999,"기관코드가 유효하지 않습니다.")

        if AccountNumber == None or AccountNumber == "" :
            raise PopbillException(-99999999,"계좌번호가 입력되지 않았습니다.")

        uri = "/EasyFin/AccountCheck"
        uri += "?c="+BankCode
        uri += "&n="+AccountNumber

        return self._httppost(uri, "", CorpNum, UserID)

    def checkDepositorInfo(self, CorpNum, BankCode, AccountNumber, IdentityNumType, IdentityNum, UserID = None):

        if BankCode == None or BankCode == "" :
            raise PopbillException(-99999999,"기관코드가 입력되지 않았습니다.")

        if len(BankCode) != 4 :
            raise PopbillException(-99999999,"기관코드가 유효하지 않습니다.")

        if AccountNumber == None or AccountNumber == "" :
            raise PopbillException(-99999999,"계좌번호가 입력되지 않았습니다.")

        if IdentityNumType == None or IdentityNumType == "" :
            raise PopbillException(-99999999,"등록번호 유형이 입력되지 않았습니다.")

        if not re.compile('^[PB]$').match(IdentityNumType) :
            raise PopbillException(-99999999,"등록번호 유형이 유효하지 않습니다.")

        if IdentityNum == None or IdentityNum == "" :
            raise PopbillException(-99999999,"등록번호가 입력되지 않았습니다.")

        if not re.compile('^\d+$').match(IdentityNum) :
            raise PopbillException(-99999999,"등록번호는 숫자만 입력 가능합니다.")

        uri = "/EasyFin/DepositorCheck"
        uri += "?c="+BankCode
        uri += "&n="+AccountNumber
        uri += "&t="+IdentityNumType
        uri += "&p="+IdentityNum

        return self._httppost(uri, "", CorpNum, UserID)
