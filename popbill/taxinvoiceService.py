# -*- coding: utf-8 -*-
# Module for Popbill Taxinvoice API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Kim Seongjun (pallet027@gmail.com)
# Written : 2015-01-21
# Thanks for your interest. 
from datetime import datetime
from .base import PopbillBase,PopbillException,File


class TaxinvoiceService(PopbillBase):
    """ 팝빌 세금계산서 API Service Implementation."""

    __MgtKeyTypes = ["SELL","BUY","TRUSTEE"]

    def __init__(self,LinkID,SecretKey):
        """ 생성자. 
            args
                LinkID : 링크허브에서 발급받은 LinkID
                SecretKey : 링크허브에서 발급받은 SecretKey
        """
        super(self.__class__,self).__init__(LinkID,SecretKey)
        self._addScope("110")
        
    def getURL(self,CorpNum, UserID , ToGo):
        """ 팝빌 세금계산서 관련 URL을 확인. 
            args
                CorpNum : 회원 사업자번호
                UserID : 팝빌 회원아이디
                ToGo : 세금계산서 관련 기능 지정 문자. (SBOX,PBOX)
            return
                30초 보안 토큰을 포함한 url
            raise
                PopbillException
        """
        result = self._httpget('/Taxinvoice/?TG=' + ToGo , CorpNum,UserID)
        return result.url

    def getUnitCost(self,CorpNum):
        """ 세금계산서 발행 단가 확인. 
            args
                CorpNum : 확인할 회원 사업자번호
            return
                발행단가 by float
            raise
                PopbillException
        """
        result = self._httpget('/Taxinvoice?cfg=UNITCOST' , CorpNum)
        return float(result.unitCost)

    def getCertificateExpireDate(self,CorpNum):
        """ 공인인증서 만료일 확인, 등록여부 확인용도로 활용가능
            args
                CorpNum : 확인할 회원 사업자번호
            return
                등록시 만료일자, 미등록시 해당 PopbillException raise.
            raise
                PopbillException
        """
        result = self._httpget('/Taxinvoice?cfg=CERT' , CorpNum)
        return datetime.strptime( result.certificateExpiration,'%Y%m%d%H%M%S')

    def getEmailPublicKeys(self,CorpNum):
        """ 국세청 대량사업자 이메일 목록 확인. 이메일 유통기능 사용시에 활용.
            args
                CorpNum : 확인할 회원 사업자번호
            return
                대량사업자 이메일 목록 by List
            raise
                PopbillException
        """
        return self._httpget('/Taxinvoice/EmailPublicKeys' , CorpNum)

    def checkMgtKeyInUse(self,CorpNum,MgtKeyType,MgtKey):
        """ 파트너 관리번호 사용중 여부 확인.
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
            return
                사용중 여부 by True/False
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        try:
            result = self._httpget('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,CorpNum)
            return result.itemKey != None and result.itemKey != ""
        except PopbillException as PE:
            if PE.code == -11000005:
                return False
            raise PE

    def register(self,CorpNum,taxinvoice,writeSpecification = False,UserID = None):
        """ 임시저장
            args
                CorpNum : 회원 사업자 번호
                taxinvoice : 등록할 세금계산서 object. Made with Taxinvoice(...)
                writeSpecification : 등록시 거래명세서 동시 작성 여부
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if taxinvoice == None : 
            raise PopbillException(-99999999,"등록할 세금계산서 정보가 입력되지 않았습니다.")
        if writeSpecification :
            taxinvoice.writeSpecification = True

        postData = self._stringtify(taxinvoice)

        return self._httppost('/Taxinvoice',postData,CorpNum,UserID)

    def update(self,CorpNum,MgtKeyType,MgtKey,taxinvoice, writeSpecification = False, UserID = None ):
        """ 수정
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                taxinvoice : 수정할 세금계산서 object. Made with Taxinvoice(...)
                writeSpecification : 등록시 거래명세서 동시 작성 여부
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if taxinvoice == None : 
            raise PopbillException(-99999999,"수정할 세금계산서 정보가 입력되지 않았습니다.")
        if writeSpecification :
            taxinvoice.writeSpecification = True

        postData = self._stringtify(taxinvoice)

        return self._httppost('/Taxinvoice/' + MgtKeyType + '/' + MgtKey,postData,CorpNum,UserID,'PATCH')

    def getInfo(self,CorpNum,MgtKeyType,MgtKey):
        """ 상태정보 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        return self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey,CorpNum)

    def getDetailInfo(self,CorpNum,MgtKeyType,MgtKey):
        """ 상세정보 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        return self._httpget('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + "?Detail",CorpNum)

    def delete(self,CorpNum,MgtKeyType,MgtKey,UserID = None):
        """ 삭제
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,'',CorpNum,UserID,"DELETE")

    def send(self,CorpNum,MgtKeyType,MgtKey,Memo = None, EmailSubject = None, UserID = None):
        """ 승인요청
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        
        req = {} 

        if Memo != None and Memo != '':
            req["memo"] = Memo
        if EmailSubject != None and EmailSubject != '':
            req["emailSubject"] = EmailSubject

        postData = self._stringtify(req)

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"SEND")

    def cancelSend(self,CorpNum,MgtKeyType,MgtKey,Memo = None, UserID = None):
        """ 승인요청 취소
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo" : Memo})
        else :
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"CANCELSEND")

    def accept(self,CorpNum,MgtKeyType,MgtKey,Memo = None, UserID = None):
        """ 승인요청 승인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo" : Memo})
        else :
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"ACCEPT")

    def deny(self,CorpNum,MgtKeyType,MgtKey,Memo = None, UserID = None):
        """ 승인요청 거부
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo" : Memo})
        else :
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"DENY")

    def issue(self,CorpNum,MgtKeyType,MgtKey,Memo = None , EmailSubject = None , ForceIssue = False , UserID = None):
        """ 발행
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                EmailSubject : 발행메일 이메일 제목
                ForceIssue : 지연발행 세금계산서 강제발행 여부. 
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        req = {"forceIssue" : ForceIssue}

        if Memo != None and Memo != '':
            req["memo"] = Memo

        if EmailSubject != None and EmailSubject != '':
            req["emailSubject"] = EmailSubject
        
        postData = self._stringtify(req)

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"ISSUE")

    def cancelIssue(self,CorpNum,MgtKeyType,MgtKey,Memo = None, UserID = None):
        """ 발행취소
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo" : Memo})
        else :
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"CANCELISSUE")

    def request(self,CorpNum,MgtKeyType,MgtKey,Memo = None, UserID = None):
        """ 역)발행요청
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo" : Memo})
        else :
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"REQUEST")

    def refuse(self,CorpNum,MgtKeyType,MgtKey,Memo = None, UserID = None):
        """ 역)발행요청 거부
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo" : Memo})
        else :
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"REFUSE")

    def cancelRequest(self,CorpNum,MgtKeyType,MgtKey,Memo = None, UserID = None):
        """ 역)발행요청 취소
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Memo : 처리 메모
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo" : Memo})
        else :
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"CANCELREQUEST")

    def sendToNTS(self,CorpNum,MgtKeyType,MgtKey, UserID = None):
        """ 국세청 즉시전송
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"NTS")

    def sendEmail(self,CorpNum,MgtKeyType,MgtKey, ReceiverEmail , UserID = None):
        """ 이메일 재전송
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                ReceiverEmail : 수신자 이메일주소
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        postData = self._stringtify({"receiver" : ReceiverEmail})

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"EMAIL")

    def sendSMS(self,CorpNum,MgtKeyType,MgtKey, Sender,Receiver,Contents, UserID = None):
        """ 세금계산서관련 문자 전송
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Sender : 발신번호
                Receiver : 수신번호
                Contents : 문자메시지 내용 Max 90bytes.
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        postData = self._stringtify({
                                    "sender" : Sender,
                                    "receiver" : Receiver,
                                    "contents" : Contents
                                    })

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"SMS")

    def sendFax(self,CorpNum,MgtKeyType,MgtKey, Sender,Receiver, UserID = None):
        """ 세금계산서 팩스 전송
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                Sender : 발신번호
                Receiver : 수신번호
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        postData = self._stringtify({
                                    "sender" : Sender,
                                    "receiver" : Receiver
                                    })

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey,postData,CorpNum,UserID,"FAX")

    def getLogs(self,CorpNum,MgtKeyType,MgtKey):
        """ 세금계산서 문서이력 목록 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
            return
                문서이력 정보 목록 as List
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        
        return self._httpget('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + "/Logs",CorpNum)

    def attachFile(self,CorpNum,MgtKeyType,MgtKey,FilePath,UserID = None):
        """ 파일 첨부 
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                FilePath : 첨부파일의 경로
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if FilePath == None or FilePath == "" :
            raise PopbillException(-99999999,"파일 경로가 입력되지 않았습니다.")
        
        files = []
        try:
            with open(FilePath,"rb") as F:
                files = [File(fieldName='Filedata',
                              fileName=F.name,
                              fileData=F.read())]
        except IOError :
            raise PopbillException(-99999999,"해당경로에 파일이 없거나 읽을 수 없습니다.")

        return self._httppost_files('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + '/Files',None,files,CorpNum,UserID)

    def getFiles(self,CorpNum,MgtKeyType,MgtKey):
        """ 첨부파일 목록 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
            return
                첩부파일 정보 목록 as List
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        
        return self._httpget('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + "/Files",CorpNum)

    def deleteFile(self,CorpNum,MgtKeyType,MgtKey,FileID , UserID = None):
        """ 첨부파일 삭제
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                UserID : 팝빌 회원아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if FileID == None or FileID == "" :
            raise PopbillException(-99999999,"파일아이디가 입력되지 않았습니다.")

        postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + "/Files/" + FileID ,postData,CorpNum,UserID,'DELETE')

    def getPopUpURL(self,CorpNum,MgtKeyType,MgtKey, UserID):
        """ 세금계산서 1장의 팝빌 화면을 볼수 있는 PopUp URL 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                UserID : 팝빌 회원아이디
            return
                팝빌 URL as str
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=POPUP',CorpNum,UserID)

        return result.url

    def getPrintURL(self,CorpNum,MgtKeyType,MgtKey, UserID):
        """ 공급자용 인쇄 URL 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                UserID : 팝빌 회원아이디
            return
                팝빌 URL as str
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=PRINT',CorpNum,UserID)

        return result.url

    def getEPrintURL(self,CorpNum,MgtKeyType,MgtKey, UserID):
        """ 공급받는자용 인쇄 URL 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                UserID : 팝빌 회원아이디
            return
                팝빌 URL as str
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=EPRINT',CorpNum,UserID)

        return result.url

    def getMailURL(self,CorpNum,MgtKeyType,MgtKey, UserID):
        """ 공급받는자용 메일 링크 URL 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKey : 파트너 관리번호
                UserID : 팝빌 회원아이디
            return
                팝빌 URL as str
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes :
            raise PopbillException(-99999999,"관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=MAIL',CorpNum,UserID)

        return result.url

    def getInfos(self,CorpNum,MgtKeyType,MgtKeyList):
        """ 상태정보 다량 확인, 최대 1000건
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKeyList : 파트너 관리번호 목록
            return
                상태정보 목록 as List
            raise
                PopbillException
        """
        if MgtKeyList == None or len(MgtKeyList) < 1:
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
       
        postData = self._stringtify(MgtKeyList)

        return self._httppost('/Taxinvoice/' + MgtKeyType ,postData,CorpNum)

    def getMassPrintURL(self,CorpNum,MgtKeyType,MgtKeyList,UserID):
        """ 다량 인쇄 URL 확인
            args
                CorpNum : 회원 사업자 번호
                MgtKeyType : 관리번호 유형 one of ['SELL','BUY','TRUSTEE']
                MgtKeyList : 파트너 관리번호 목록
                UserID : 팝빌 회원아이디 
            return
                팝빌 URL as str
            raise
                PopbillException
        """
        if MgtKeyList == None or len(MgtKeyList) < 1:
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
       
        postData = self._stringtify(MgtKeyList)

        Result = self._httppost('/Taxinvoice/' + MgtKeyType + "?Print" ,postData,CorpNum,UserID)

        return Result.url


class Taxinvoice(object):
    def __init__(self,**kwargs):
        self.__dict__ = kwargs


class TaxinvoiceDetail(object):
    def __init__(self,**kwargs):
        self.__dict__ = kwargs


class Contact(object):
    def __init__(self,**kwargs):
        self.__dict__ = kwargs