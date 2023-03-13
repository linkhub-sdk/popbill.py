# -*- coding: utf-8 -*-
# Module for Popbill BizInfoCheck API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : shchoi (code@linkhubcorp.com)
# Written : 2022-09-28
# Thanks for your interest.

from .base import PopbillBase, PopbillException


class BizInfoCheckService(PopbillBase):
    """팝빌 기업정보조회 API Service Implementation."""

    def __init__(self, LinkID, SecretKey):
        """생성자
        args
            LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
            SecretKey : 링크허브에서 발급받은 비밀키(SecretKey)
        """

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("171")

    def getChargeInfo(self, CorpNum, UserID=None):
        """과금정보 확인
        args
            CorpNum : 회원 사업자번호
            UserID : 팝빌 회원아이디
        return
            과금정보 객체
        raise
            PopbillException
        """
        return self._httpget("/BizInfo/ChargeInfo", CorpNum, UserID)

    def getUnitCost(self, CorpNum, UserID=None):
        """기업정보조회 단가 확인.
        args
            CorpNum : 팝빌회원 사업자번호
        return
            발행단가 by float
        raise
            PopbillException
        """

        result = self._httpget("/BizInfo/UnitCost", CorpNum, UserID)

        return float(result.unitCost)

    def checkBizInfo(self, MemberCorpNum, CheckCorpNum, UserID=None):
        """기업정보조회 - 단건
        args
            MemberCorpNum : 팝빌회원 사업자번호
            CheckCorpNum : 조회할 사업자번호
            UserID : 팝빌회원 아이디
        return
            기업정보정보 object
        raise
            PopbillException
        """

        if MemberCorpNum == None or MemberCorpNum == "":
            raise PopbillException(-99999999, "팝빌회원 사업자번호가 입력되지 않았습니다.")

        if CheckCorpNum == None or CheckCorpNum == "":
            raise PopbillException(-99999999, "조회할 사업자번호가 입력되지 않았습니다.")

        return self._httpget("/BizInfo/Check?CN=" + CheckCorpNum, MemberCorpNum, UserID)
