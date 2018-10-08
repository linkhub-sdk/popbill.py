# -*- coding: utf-8 -*-
# Module for Popbill Hometax Cashbill API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Jeong Yohan (code@linkhub.co.kr)
# Written : 2015-07-16
# Updated : 2016-07-27
# Thanks for your interest.

from .base import PopbillBase, PopbillException


class HTCashbillService(PopbillBase):
    """ 팝빌 홈택스 현금영수증 연계 API Service Implementation. """

    def __init__(self, LinkID, SecretKey):
        """ 생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("141")

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

        return self._httpget('/HomeTax/Cashbill/ChargeInfo', CorpNum, UserID)

    def requestJob(self, CorpNum, Type, SDate, EDate, UserID=None):
        """ 수집 요청
            args
                CorpNum : 팝빌회원 사업자번호
                Type : 문서형태, SELL-매출, BUY-매입,
                SDate : 시작일자, 표시형식(yyyyMMdd)
                EDate : 종료일자, 표시형식(yyyyMMdd)
                UserID : 팝빌회원 아이디
            return
                작업아이디 (jobID)
            raise
                PopbillException
        """

        if Type == None or Type == '':
            raise PopbillException(-99999999, "문서형태이 입력되지 않았습니다.")

        if SDate == None or SDate == '':
            raise PopbillException(-99999999, "시작일자가 입력되지 않았습니다.")

        if EDate == None or EDate == '':
            raise PopbillException(-99999999, "종료일자가 입력되지 않았습니다.")

        uri = '/HomeTax/Cashbill/' + Type
        uri += '?SDate=' + SDate
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

        return self._httpget('/HomeTax/Cashbill/' + JobID + '/State', CorpNum, UserID)

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

        return self._httpget('/HomeTax/Cashbill/JobList', CorpNum, UserID)

    def search(self, CorpNum, JobID, TradeType, TradeUsage, Page, PerPage, Order, UserID=None):
        """ 수집 결과 조회
            args
                CorpNum : 팝빌회원 사업자번호
                JobID : 작업아이디
                TradeType : 문서형태 배열, N-일반 현금영수증, C-취소 현금영수증
                TradeUsage : 거래구분 배열, P-소등공제용, C-지출증빙용
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

        uri = '/HomeTax/Cashbill/' + JobID
        uri += '?TradeType=' + ','.join(TradeType)
        uri += '&TradeUsage=' + ','.join(TradeUsage)
        uri += '&Page=' + str(Page)
        uri += '&PerPage=' + str(PerPage)
        uri += '&Order=' + Order

        return self._httpget(uri, CorpNum, UserID)

    def summary(self, CorpNum, JobID, TradeType, TradeUsage, UserID=None):
        """ 수집 결과 요약정보 조회
            args
                CorpNum : 팝빌회원 사업자번호
                JobID : 작업아이디
                TradeType : 문서형태 배열, N-일반 현금영수증, C-취소 현금영수증
                TradeUsage : 거래구분 배열, P-소등공제용, C-지출증빙용
                UserID : 팝빌회원 아이디
            return
                수집 결과 요약정보
            raise
                PopbillException
        """
        if JobID == None or len(JobID) != 18:
            raise PopbillException(-99999999, "작업아이디(jobID)가 올바르지 않습니다.")

        uri = '/HomeTax/Cashbill/' + JobID + '/Summary'
        uri += '?TradeType=' + ','.join(TradeType)
        uri += '&TradeUsage=' + ','.join(TradeUsage)

        return self._httpget(uri, CorpNum, UserID)

    def getFlatRatePopUpURL(self, CorpNum, UserID=None):
        """ 정액제 서비스 신청 URL
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                정액제 서비스 팝업 URL
            raise
                PopbillException
        """
        return self._httpget('/HomeTax/Cashbill?TG=CHRG', CorpNum, UserID).url

    def getCertificatePopUpURL(self, CorpNum, UserID=None):
        """ 홈택스 공인인증서 등록 URL
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                공인인증서 등록 팝업 URL
            raise
                PopbillException
        """
        return self._httpget('/HomeTax/Cashbill?TG=CERT', CorpNum, UserID).url

    def getFlatRateState(self, CorpNum, UserID=None):
        """ 정액제 서비스 상태 확인
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                정액제 서비스 상태 정보
            raise
                PopbillException
        """
        return self._httpget('/HomeTax/Cashbill/Contract', CorpNum, UserID)

    def getCertificateExpireDate(self, CorpNum, UserID=None):
        """ 공인인증서 만료일자 확인
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                공인인증서 만료일자
            raise
                PopbillException
        """

        return self._httpget('/HomeTax/Cashbill/CertInfo', CorpNum, UserID).certificateExpiration

    def checkCertValidation(self, CorpNum, UserID=None):
        """ 홈택스 공인인증서 로그인 테스트
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """

        return self._httpget('/HomeTax/Cashbill/CertCheck', CorpNum, UserID)

    def registDeptUser(self, CorpNum, DeptUserID, DeptUserPWD, UserID=None):
        """ 홈택스 현금영수증 부서사용자 계정 등록
            args
                CorpNum : 팝빌회원 사업자번호
                DeptUserID : 홈택스 부서사용자 계정아이디
                DeptUserPWD : 홈택스 부서사용자 계정비밀번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if DeptUserID == None or len(DeptUserID) == 0:
            raise PopbillException(-99999999, "홈택스 부서사용자 계정 아이디가 입력되지 않았습니다.")

        if DeptUserPWD == None or len(DeptUserPWD) == 0:
            raise PopbillException(-99999999, "홈택스 부서사용자 계정 비밀번호가 입력되지 않았습니다.")

        req = {}
        req["id"] = DeptUserID
        req["pwd"] = DeptUserPWD

        postData = self._stringtify(req)

        return self._httppost("/HomeTax/Cashbill/DeptUser", postData, CorpNum, UserID)

    def checkDeptUser(self, CorpNum, UserID=None):
        """ 홈택스 현금영수증 부서사용자 등록정보 확인
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        return self._httpget('/HomeTax/Cashbill/DeptUser', CorpNum, UserID)

    def checkLoginDeptUser(self, CorpNum, UserID=None):
        """ 홈택스 현금영수증 부서사용자 로그인 테스트
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        return self._httpget('/HomeTax/Cashbill/DeptUser/Check', CorpNum, UserID)

    def deleteDeptUser(self, CorpNum, UserID=None):
        """ 홈택스 현금영수증 부서사용자 등록정보 삭제
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        return self._httppost("/HomeTax/Cashbill/DeptUser", "", CorpNum, UserID, "DELETE")
