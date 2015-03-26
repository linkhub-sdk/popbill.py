# -*- coding: utf-8 -*-
# Module for Popbill Taxinvoice API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : John Yohan (yhjeong@linkhub.co.kr)
# Written : 2015-03-20
# Thanks for your interest.
from .base import PopbillBase,PopbillException,File

class StatementService(PopbillBase):
    """ 팝빌 전자명세서 API Service Implementation. """

    def __init__(self,LinkID,SecretKey):
        """생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """
        super(self.__class__,self).__init__(LinkID,SecretKey)
        self._addScope("121")
        self._addScope("122")
        self._addScope("123")
        self._addScope("124")
        self._addScope("125")
        self._addScope("126")

    def getURL(self, CorpNum, UserID, ToGo):
        """ 팝빌 전자명세서 관련 URL 
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌 회원아이디
                ToGo : 전자명세서 관련 기능 지정 문자.(TBOX-임시문서함, SBOX-매출문서함)
            return
                30초 보안 토큰을 포함한 url
            raise 
                PopbillException
        """

        result = self._httpget('/Statement?TG=' + ToGo, CorpNum, UserID)
        return result.url

    def getUnitCost(self, CorpNum, ItemCode):
        """ 전자명세서 발행단가 확인.
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
            return
                발행단가 by float
            raise 
                PopbillException
        """
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        result = self._httpget('/Statement/' + str(ItemCode) + '?cfg=UNITCOST', CorpNum)
        return float(result.unitCost)

    def checkMgtKeyInUse(self, CorpNum, ItemCode, MgtKey):
        """ 파트너 문서관리번호 사용여부 확인.
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 문서관리번호(최대 24자리, 숫자,영문,'-','_'로 구성)
            return
                사용 여부 by True/False
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        try:
            result = self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey, CorpNum)
            return result.itemKey != None and result.itemKey != ""

        except PopbillException as PE:
            if PE.code == -12000004:
                return False
            raise PE

    def register(self, CorpNum, statement, UserID = None):
        """ 임시저장
            args
                CorpNum : 팝빌회원 사업자번호
                statement : 등록할 전자명세서 object. made with Statement(...)
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if statement == None:
            raise PopbillException(-99999999, "등록할 전자명세서 정보가 입력되지 않았습니다.")

        postData = self._stringtify(statement)

        return self._httppost('/Statement', postData, CorpNum, UserID)

    def update(self, CorpNum, ItemCode, MgtKey, Statement, UserID = None):
        """ 임시저장
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                Statement : 등록할 전자명세서 object. made with Statement(...)
                UserID : 팝빌회원 아이디 
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        if Statement == None:
            raise PopbillException(-99999999, "등록할 전자명세서 정보가 입력되지 않았습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        postData = self._stringtify(Statement)

        return self._httppost('/Statement/' + str(ItemCode) + '/' + MgtKey, postData, CorpNum, UserID, 'PATCH')

    def issue(self, CorpNum, ItemCode, MgtKey, Memo = None, EmailSubject = None, UserID = None):
        """ 발행
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                Memo : 처리메모 
                EmailSubject : 발행메일 제목(미기재시 기본양식으로 전송) 
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")
        
        req = {}
        postData = ""

        if Memo != None and Memo != '':
            req["memo"] = Memo
        if EmailSubject != None and EmailSubject != '':
            req["emailSubject"] = EmailSubject

        postData = self._stringtify(req)

        return self._httppost('/Statement/' + str(ItemCode) + '/' + MgtKey, postData, CorpNum, UserID, "ISSUE")

    def cancel(self, CorpNum, ItemCode, MgtKey, Memo = None, UserID = None):
        """ 발행취소
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                Memo : 처리메모 
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        postData = ''


        if Memo != None and Memo != '':
            postData = self._stringtify({"memo" : Memo})

        return self._httppost('/Statement/' + str(ItemCode) + '/' + MgtKey, postData, CorpNum, UserID, "CANCEL")

    def delete(self, CorpNum, ItemCode, MgtKey, UserID = None):
        """ 삭제
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """     
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        return self._httppost('/Statement/' + str(ItemCode) + '/' + MgtKey,'', CorpNum, UserID, "DELETE")


    def getInfo(self, CorpNum, ItemCode, MgtKey):
        """ 상태/요약 정보 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
            return
                문서 상태/요약정보 object
            raise 
                PopbillException
        """     
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        return self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey, CorpNum)

    def getDetailInfo(self, CorpNum, ItemCode, MgtKey):
        """ 전자명세서 상세정보 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
            return
                문서 상세정보 object
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        return self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey + '?Detail', CorpNum)

    def sendEmail(self, CorpNum, ItemCode, MgtKey, ReceiverEmail, UserID = None):
        """ 메일 재전송
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                ReceiverEmail : 수신자 메일주소
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        postData = self._stringtify({"receiver" : ReceiverEmail})

        return self._httppost('/Statement/' + str(ItemCode) + '/' + MgtKey, postData, CorpNum, UserID, "EMAIL")

    def sendSMS(self, CorpNum, ItemCode, MgtKey, Sender, Receiver, Contents, UserID = None):
        """ 알림문자 전송
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                Sender : 발신번호 
                Receiver : 수신번호
                Contents : 문자메시지 내용(최대 90Byte), 최대길이를 초과한경우 길이가 조정되어 전송됨
                UserID : 팝빌 회원아이디 
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        postData = self._stringtify({
                                        "sender" : Sender,
                                        "receiver" : Receiver, 
                                        "contents" : Contents
                                    })

        return self._httppost('/Statement/' + str(ItemCode) + '/' + MgtKey, postData, CorpNum, UserID, "SMS")

    def sendFAX(self, CorpNum, ItemCode, MgtKey, Sender, Receiver, UserID = None):
        """ 전자명세서 팩스 전송
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                Sender : 발신번호 
                Receiver : 수신 팩스번호
                UserID : 팝빌 회원아이디 
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        postData = self._stringtify({
                                        "sender" : Sender,
                                        "receiver" : Receiver 
                                    })

        return self._httppost('/Statement/' + str(ItemCode) + '/' + MgtKey, postData, CorpNum, UserID, "FAX")

    def getLogs(self, CorpNum, ItemCode, MgtKey):
        """ 전자명세서 문서이력 목록 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
            return
                문서이력 정보 목록 as List
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        return self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey + '/Logs',CorpNum)

    def attachFile(self, CorpNum, ItemCode, MgtKey, FilePath, UserID = None):
        """ 파일 첨부
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                FilePath : 첨부파일의 경로
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if FilePath == None or FilePath == "" :
            raise PopbillException(-99999999,"파일경로가 입력되지 않았습니다.")
        
        files = []

        try:
            with open(FilePath,"rb") as F:
                files = [File(fieldName='Filedata',
                              fileName=F.name,
                              fileData=F.read())]
        except IOError :
            raise PopbillException(-99999999,"해당경로에 파일이 없거나 읽을 수 없습니다.")

        return self._httppost_files('/Statement/' + str(ItemCode) + '/' + MgtKey + '/Files', None, files, CorpNum, UserID)

    def getFiles(self, CorpNum, ItemCode, MgtKey):
        """ 첨부파일 목록 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
            return
                첨부파일 목록 as List
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")


        return self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey + '/Files', CorpNum)


    def deleteFile(self, CorpNum, ItemCode, MgtKey, FileID, UserID = None):
        """ 첨부파일 삭제
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                FileID : 파일아이디, 첨부파일 목록확인(getFiles) API 응답전문의 AttachedFile 변수값 
                UserID : 팝빌회원 아이디
            return
                첨부파일 정보 목록 as List
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")
        if FileID == None or FileID == "" :
            raise PopbillException(-99999999,"파일아이디가 입력되지 않았습니다.")

        postData = ''

        return self._httppost('/Statement/' + str(ItemCode) + '/' + MgtKey + '/Files/' + FileID, postData, CorpNum, UserID, 'DELETE')


    def getPopUpURL(self, CorpNum, ItemCode, MgtKey, UserID):
        """ 전자명세서 1장의 팝빌 화면을 볼수있는 PopUp URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        result = self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey + '?TG=POPUP', CorpNum, UserID)

        return result.url

    def getPrintURL(self, CorpNum, ItemCode, MgtKey, UserID):
        """ 공급자용 인쇄 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        result = self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey + '?TG=PRINT', CorpNum, UserID)

        return result.url


    def getEPrintURL(self, CorpNum, ItemCode, MgtKey, UserID):
        """ 공급받는자용 인쇄 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        result = self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey + '?TG=EPRINT', CorpNum, UserID)

        return result.url


    def getMailURL(self, CorpNum, ItemCode, MgtKey, UserID):
        """ 공급받는자용 메일 링크 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKey : 파트너 문서관리번호
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")


        result = self._httpget('/Statement/' + str(ItemCode) + '/' + MgtKey + '?TG=MAIL', CorpNum, UserID)

        return result.url


    def getMassPrintURL(self, CorpNum, ItemCode, MgtKeyList, UserID):
        """ 다량 인쇄 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                ItemCode : 명세서 코드 
                    [121 - 거래명세서], [122 - 청구서], [123 - 견적서],
                    [124 - 발주서], [125 - 입금표], [126 - 영수증]
                MgtKeyList : 파트너 문서관리번호 목록
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKeyList == None:
            raise PopbillException(-99999999,"관리번호 배열이 입력되지 않았습니다.")
        if ItemCode == None:
            raise PopbillException(-99999999,"명세서 코드가 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        result = self._httppost('/Statement/' + str(ItemCode) + '?Print', postData, CorpNum, UserID)

        return result.url


class Statement(object):
    def __init__(self,**kwargs):
        self.__dict__ = kwargs


class StatementDetail(object):
    def __init__(self,**kwargs):
        self.__dict__ = kwargs