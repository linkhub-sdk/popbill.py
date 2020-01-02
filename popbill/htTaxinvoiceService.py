# -*- coding: utf-8 -*-
# Module for Popbill Hometax Taxinvoice API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Jeong Yohan (code@linkhub.co.kr)
# Written : 2015-07-16
# Updated : 2020-01-02
# Thanks for your interest.

from .base import PopbillBase, PopbillException


class HTTaxinvoiceService(PopbillBase):
    """ 팝빌 홈택스 전자세금계산서 연계 API Service Implementation. """

    def __init__(self, LinkID, SecretKey):
        """ 생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("111")

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

        return self._httpget('/HomeTax/Taxinvoice/ChargeInfo', CorpNum, UserID)

    def requestJob(self, CorpNum, Type, DType, SDate, EDate, UserID=None):
        """ 수집 요청
            args
                CorpNum : 팝빌회원 사업자번호
                Type : 전자세금계산서 유형, SELL-매출, BUY-매입, TRUSTEE-위수탁
                DType : 일자유형, W-작성일자, I-발행일자, S-전송일자
                SDate : 시작일자, 표시형식(yyyyMMdd)
                EDate : 종료일자, 표시형식(yyyyMMdd)
                UserID : 팝빌회원 아이디
            return
                작업아이디 (jobID)
            raise
                PopbillException
        """
        if Type == None or Type == '':
            raise PopbillException(-99999999, "전자세금계산서 유형이 입력되지 않았습니다.")

        if SDate == None or SDate == '':
            raise PopbillException(-99999999, "시작일자가 입력되지 않았습니다.")

        if EDate == None or EDate == '':
            raise PopbillException(-99999999, "종료일자가 입력되지 않았습니다.")

        uri = '/HomeTax/Taxinvoice/' + Type
        uri += '?DType=' + DType
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

        return self._httpget('/HomeTax/Taxinvoice/' + JobID + '/State', CorpNum, UserID)

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

        return self._httpget('/HomeTax/Taxinvoice/JobList', CorpNum, UserID)

    def search(self, CorpNum, JobID, Type, TaxType, PurposeType, TaxRegIDType, TaxRegIDYN, TaxRegID, Page, PerPage,
               Order, UserID=None, SearchString=None):
        """ 수집 결과 조회
            args
                CorpNum : 팝빌회원 사업자번호
                JobID : 작업아이디
                Type : 문서형태 배열, N-일반전자세금계산서, M-수정전자세금계산서
                TaxType : 과세형태 배열, T-과세, N-면세, Z-영세
                PurposeType : 영수/청구, R-영수, C-청구, N-없음
                TaxRegIDType : 종사업장번호 사업자유형, S-공급자, B-공급받는자, T-수탁자
                TaxRegIDYN : 종사업장번호 유무, 공백-전체조회, 0-종사업장번호 없음, 1-종사업장번호 있음
                TaxRegID : 종사업장번호, 콤마(",")로 구분 하여 구성 ex) '0001,0002'
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

        uri = '/HomeTax/Taxinvoice/' + JobID
        uri += '?Type=' + ','.join(Type)
        uri += '&TaxType=' + ','.join(TaxType)
        uri += '&PurposeType=' + ','.join(PurposeType)
        uri += '&TaxRegIDType=' + TaxRegIDType
        uri += '&TaxRegID=' + TaxRegID
        uri += '&Page=' + str(Page)
        uri += '&PerPage=' + str(PerPage)
        uri += '&Order=' + Order

        if TaxRegIDYN != '':
            uri += '&TaxRegIDYN=' + TaxRegIDYN

        if SearchString is not None:
            uri += '&SearchString=' + SearchString

        return self._httpget(uri, CorpNum, UserID)

    def summary(self, CorpNum, JobID, Type, TaxType, PurposeType, TaxRegIDType, TaxRegIDYN, TaxRegID, UserID=None, SearchString=None ):
        """ 수집 결과 요약정보 조회
            args
                CorpNum : 팝빌회원 사업자번호
                JobID : 작업아이디
                Type : 문서형태 배열, N-일반전자세금계산서, M-수정전자세금계산서
                TaxType : 과세형태 배열, T-과세, N-면세, Z-영세
                PurposeType : 영수/청구, R-영수, C-청구, N-없음
                TaxRegIDType : 종사업장번호 사업자유형, S-공급자, B-공급받는자, T-수탁자
                TaxRegIDYN : 종사업장번호 유무, 공백-전체조회, 0-종사업장번호 없음, 1-종사업장번호 있음
                TaxRegID : 종사업장번호, 콤마(",")로 구분 하여 구성 ex) '0001,0002'
                UserID : 팝빌회원 아이디
            return
                수집 결과 요약정보
            raise
                PopbillException
        """
        if JobID == None or len(JobID) != 18:
            raise PopbillException(-99999999, "작업아이디(jobID)가 올바르지 않습니다.")

        uri = '/HomeTax/Taxinvoice/' + JobID + '/Summary'
        uri += '?Type=' + ','.join(Type)
        uri += '&TaxType=' + ','.join(TaxType)
        uri += '&PurposeType=' + ','.join(PurposeType)
        uri += '&TaxRegIDType=' + TaxRegIDType
        uri += '&TaxRegID=' + TaxRegID

        if TaxRegIDYN != '':
            uri += '&TaxRegIDYN=' + TaxRegIDYN

        if SearchString is not None:
            uri += '&SearchString=' + SearchString

        return self._httpget(uri, CorpNum, UserID)

    def getTaxinvoice(self, CorpNum, NTSConfirmNum, UserID=None):
        """ 전자세금계산서 상세정보 확인
            args
                CorpNum : 팝빌회원 사업자번호
                NTSConfirmNum : 국세청 승인번호
                UserID : 팝빌회원 아이디
            return
                전자세금계산서 정보객체
            raise
                PopbillException
        """
        if NTSConfirmNum == None or len(NTSConfirmNum) != 24:
            raise PopbillException(-99999999, "국세청승인번호(NTSConfirmNum)가 올바르지 않습니다.")

        return self._httpget('/HomeTax/Taxinvoice/' + NTSConfirmNum, CorpNum, UserID)

    def getXML(self, CorpNum, NTSConfirmNum, UserID=None):
        """ 전자세금계산서 상세정보 확인 - XML
            args
                CorpNum : 팝빌회원 사업자번호
                NTSConfirmNum : 국세청 승인번호
                UserID : 팝빌회원 아이디
            return
                전자세금계산서 정보객체
            raise
                PopbillException
        """
        if NTSConfirmNum == None or len(NTSConfirmNum) != 24:
            raise PopbillException(-99999999, "국세청승인번호(NTSConfirmNum)가 올바르지 않습니다.")

        return self._httpget('/HomeTax/Taxinvoice/' + NTSConfirmNum + '?T=xml', CorpNum, UserID)

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
        return self._httpget('/HomeTax/Taxinvoice?TG=CHRG', CorpNum, UserID).url

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
        return self._httpget('/HomeTax/Taxinvoice?TG=CERT', CorpNum, UserID).url

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
        return self._httpget('/HomeTax/Taxinvoice/Contract', CorpNum, UserID)

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

        return self._httpget('/HomeTax/Taxinvoice/CertInfo', CorpNum, UserID).certificateExpiration

    def getPopUpURL(self, CorpNum, NTSConfirmNum, UserID=None):
        """ 홈택스 전자세금계산서 보기 팝업 URL
            args
                CorpNum : 팝빌회원 사업자번호
                NTSConfirmNum : 국세청 승인 번호
                UserID : 팝빌회원 아이디
            return
                전자세금계산서 보기 팝업 URL 반환
            raise
                PopbillException
        """

        if NTSConfirmNum == None or len(NTSConfirmNum) != 24:
            raise PopbillException(-99999999, "국세청승인번호(NTSConfirmNum)가 올바르지 않습니다.")

        return self._httpget('/HomeTax/Taxinvoice/' + NTSConfirmNum + '/PopUp', CorpNum, UserID).url

    def getPrintURL(self, CorpNum, NTSConfirmNum, UserID=None):
        """ 홈택스 전자세금계산서 인쇄 팝업 URL
            args
                CorpNum : 팝빌회원 사업자번호
                NTSConfirmNum : 국세청 승인 번호
                UserID : 팝빌회원 아이디
            return
                전자세금계산서 보기 인쇄 URL 반환
            raise
                PopbillException
        """

        if NTSConfirmNum == None or len(NTSConfirmNum) != 24:
            raise PopbillException(-99999999, "국세청승인번호(NTSConfirmNum)가 올바르지 않습니다.")

        return self._httpget('/HomeTax/Taxinvoice/' + NTSConfirmNum + '/Print', CorpNum, UserID).url

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

        return self._httpget('/HomeTax/Taxinvoice/CertCheck', CorpNum, UserID)

    def registDeptUser(self, CorpNum, DeptUserID, DeptUserPWD, UserID=None):
        """ 홈택스 전자세금계산서 부서사용자 계정 등록
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

        return self._httppost("/HomeTax/Taxinvoice/DeptUser", postData, CorpNum, UserID)

    def checkDeptUser(self, CorpNum, UserID=None):
        """ 홈택스 전자세금계산서 부서사용자 등록정보 확인
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        return self._httpget('/HomeTax/Taxinvoice/DeptUser', CorpNum, UserID)

    def checkLoginDeptUser(self, CorpNum, UserID=None):
        """ 홈택스 전자세금계산서 부서사용자 로그인 테스트
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        return self._httpget('/HomeTax/Taxinvoice/DeptUser/Check', CorpNum, UserID)

    def deleteDeptUser(self, CorpNum, UserID=None):
        """ 홈택스 전자세금계산서 부서사용자 등록정보 삭제
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        return self._httppost("/HomeTax/Taxinvoice/DeptUser", "", CorpNum, UserID, "DELETE")
