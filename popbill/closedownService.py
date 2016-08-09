# -*- coding: utf-8 -*-
# Module for Popbill Closedown API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Jeong Yohan (yhjeong@linkhub.co.kr)
# Written : 2015-07-16
# Updated : 2016-07-25
# Thanks for your interest.

from .base import PopbillBase,PopbillException

class ClosedownService(PopbillBase):
    """ 팝빌 휴폐업조회 API Service Implementation. """

    def __init__(self,LinkID,SecretKey):
        """생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """

        super(self.__class__,self).__init__(LinkID,SecretKey)
        self._addScope("170")

    def getChargeInfo(self, CorpNum, UserID = None):
        """ 과금정보 확인
            args
                CorpNum : 회원 사업자번호
                UserID : 팝빌 회원아이디
            return
                과금정보 객체
            raise
                PopbillException
        """
        return self._httpget('/CloseDown/ChargeInfo', CorpNum, UserID)

    def getUnitCost(self, CorpNum):
        """ 휴폐업조회 단가 확인.
            args
                CorpNum : 팝빌회원 사업자번호
            return
                발행단가 by float
            raise
                PopbillException
        """

        result = self._httpget('/CloseDown/UnitCost', CorpNum)

        return float(result.unitCost)

    def checkCorpNum(self, MemberCorpNum, CheckCorpNum):
        """ 휴폐업조회 - 단건
            args
                MemberCorpNum : 팝빌회원 사업자번호
                CorpNum : 조회할 사업자번호
                MgtKey : 문서관리번호
            return
                휴폐업정보 object
            raise
                PopbillException
        """

        if MemberCorpNum == None or MemberCorpNum == "" :
            raise PopbillException(-99999999,"팝빌회원 사업자번호가 입력되지 않았습니다.")

        if CheckCorpNum == None or CheckCorpNum == "" :
            raise PopbillException(-99999999,"조회할 사업자번호가 입력되지 않았습니다.")

        return self._httpget('/CloseDown?CN=' +CheckCorpNum, MemberCorpNum)

    def checkCorpNums(self, MemberCorpNum, CorpNumList):
        """ 휴폐업조회 대량 확인, 최대 1000건
            args
                MemberCorpNum : 팝빌회원 사업자번호
                CorpNumList : 조회할 사업자번호 배열
            return
                휴폐업정보 Object as List
            raise
                PopbillException
        """
        if CorpNumList == None or len(CorpNumList) < 1:
            raise PopbillException(-99999999,"조죄할 사업자번호 목록이 입력되지 않았습니다.")

        postData = self._stringtify(CorpNumList)

        return self._httppost('/CloseDown',postData,MemberCorpNum)
