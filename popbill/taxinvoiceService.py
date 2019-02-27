# -*- coding: utf-8 -*-
# Module for Popbill Taxinvoice API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Kim Seongjun (pallet027@gmail.com)
# Written : 2015-01-21
# Contributor : Jeong Yohan (code@linkhub.co.kr)
# Updated : 2019-02-27
# Thanks for your interest.
from datetime import datetime
from .base import PopbillBase, PopbillException, File


class TaxinvoiceService(PopbillBase):
    """ 팝빌 세금계산서 API Service Implementation."""

    __MgtKeyTypes = ["SELL", "BUY", "TRUSTEE"]

    def __init__(self, LinkID, SecretKey):
        """ 생성자.
            args
                LinkID : 링크허브에서 발급받은 LinkID
                SecretKey : 링크허브에서 발급받은 SecretKey
        """
        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("110")

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
        return self._httpget('/Taxinvoice/ChargeInfo', CorpNum, UserID)

    def getURL(self, CorpNum, UserID, ToGo):
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

        if ToGo == None or ToGo == '':
            raise PopbillException(-99999999, "TOGO값이 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/?TG=' + ToGo, CorpNum, UserID)
        return result.url

    def getUnitCost(self, CorpNum):
        """ 세금계산서 발행 단가 확인.
            args
                CorpNum : 확인할 회원 사업자번호
            return
                발행단가 by float
            raise
                PopbillException
        """
        result = self._httpget('/Taxinvoice?cfg=UNITCOST', CorpNum)
        return float(result.unitCost)

    def getCertificateExpireDate(self, CorpNum):
        """ 공인인증서 만료일 확인, 등록여부 확인용도로 활용가능
            args
                CorpNum : 확인할 회원 사업자번호
            return
                등록시 만료일자, 미등록시 해당 PopbillException raise.
            raise
                PopbillException
        """
        result = self._httpget('/Taxinvoice?cfg=CERT', CorpNum)
        return datetime.strptime(result.certificateExpiration, '%Y%m%d%H%M%S')

    def getEmailPublicKeys(self, CorpNum):
        """ 국세청 대량사업자 이메일 목록 확인. 이메일 유통기능 사용시에 활용.
            args
                CorpNum : 확인할 회원 사업자번호
            return
                대량사업자 이메일 목록 by List
            raise
                PopbillException
        """
        return self._httpget('/Taxinvoice/EmailPublicKeys', CorpNum)

    def checkMgtKeyInUse(self, CorpNum, MgtKeyType, MgtKey):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        try:
            result = self._httpget('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, CorpNum)
            return result.itemKey != None and result.itemKey != ""
        except PopbillException as PE:
            if PE.code == -11000005:
                return False
            raise PE

    def register(self, CorpNum, taxinvoice, writeSpecification=False, UserID=None):
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
        if taxinvoice == None:
            raise PopbillException(-99999999, "등록할 세금계산서 정보가 입력되지 않았습니다.")
        if writeSpecification:
            taxinvoice.writeSpecification = True

        postData = self._stringtify(taxinvoice)

        return self._httppost('/Taxinvoice', postData, CorpNum, UserID)

    def registIssue(self, CorpNum, taxinvoice, writeSpecification=False, forceIssue=False, dealInvoiceMgtKey=None,
                    memo=None, emailSubject=None, UserID=None):
        """ 즉시 발행
            args
                CorpNum : 팝빌회원 사업자번호
                taxinvoice : 세금계산서 객체
                writeSpecification : 거래명세서 동시작성 여부
                forceIssue : 지연발행 강제여부
                dealInvoiceMgtKey : 거래명세서 문서관리번호
                memo : 메모
                emailSubject : 메일제목, 미기재시 기본제목으로 전송
                UsreID : 팝빌회원 아이디
            return
                검색결과 정보
            raise
                PopbillException
        """
        if writeSpecification:
            taxinvoice.writeSpecification = True

        if forceIssue:
            taxinvoice.forceIssue = True

        if dealInvoiceMgtKey != None and dealInvoiceMgtKey != '':
            taxinvoice.dealInvoiceMgtKey = dealInvoiceMgtKey

        if memo != None and memo != '':
            taxinvoice.memo = memo

        if emailSubject != None and emailSubject != '':
            taxinvoice.emailSubject = emailSubject

        postData = self._stringtify(taxinvoice)

        return self._httppost('/Taxinvoice', postData, CorpNum, UserID, "ISSUE")

    def update(self, CorpNum, MgtKeyType, MgtKey, taxinvoice, writeSpecification=False, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")
        if taxinvoice == None:
            raise PopbillException(-99999999, "수정할 세금계산서 정보가 입력되지 않았습니다.")
        if writeSpecification:
            taxinvoice.writeSpecification = True

        postData = self._stringtify(taxinvoice)

        return self._httppost('/Taxinvoice/' + MgtKeyType + '/' + MgtKey, postData, CorpNum, UserID, 'PATCH')

    def getInfo(self, CorpNum, MgtKeyType, MgtKey):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        return self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey, CorpNum)

    def getDetailInfo(self, CorpNum, MgtKeyType, MgtKey):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        return self._httpget('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + "?Detail", CorpNum)

    def delete(self, CorpNum, MgtKeyType, MgtKey, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, '', CorpNum, UserID, "DELETE")

    def send(self, CorpNum, MgtKeyType, MgtKey, Memo=None, EmailSubject=None, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        req = {}

        if Memo != None and Memo != '':
            req["memo"] = Memo
        if EmailSubject != None and EmailSubject != '':
            req["emailSubject"] = EmailSubject

        postData = self._stringtify(req)

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "SEND")

    def cancelSend(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "CANCELSEND")

    def accept(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "ACCEPT")

    def deny(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "DENY")

    def issue(self, CorpNum, MgtKeyType, MgtKey, Memo=None, EmailSubject=None, ForceIssue=False, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        req = {"forceIssue": ForceIssue}

        if Memo != None and Memo != '':
            req["memo"] = Memo

        if EmailSubject != None and EmailSubject != '':
            req["emailSubject"] = EmailSubject

        postData = self._stringtify(req)

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "ISSUE")

    def cancelIssue(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "CANCELISSUE")

    def registRequest(self, CorpNum, taxinvoice, memo=None, UserID=None):
        """ 즉시 요청
            args
                CorpNum : 팝빌회원 사업자번호
                taxinvoice : 세금계산서 객체
                memo : 메모
                UsreID : 팝빌회원 아이디
            return
                검색결과 정보
            raise
                PopbillException
        """

        if memo != None and memo != '':
            taxinvoice.memo = memo

        postData = self._stringtify(taxinvoice)

        return self._httppost('/Taxinvoice', postData, CorpNum, UserID, "REQUEST")

    def request(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "REQUEST")

    def refuse(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "REFUSE")

    def cancelRequest(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        if Memo != None and Memo != '':
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "CANCELREQUEST")

    def sendToNTS(self, CorpNum, MgtKeyType, MgtKey, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "NTS")

    def sendEmail(self, CorpNum, MgtKeyType, MgtKey, ReceiverEmail, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        postData = self._stringtify({"receiver": ReceiverEmail})

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "EMAIL")

    def sendSMS(self, CorpNum, MgtKeyType, MgtKey, Sender, Receiver, Contents, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        postData = self._stringtify({
            "sender": Sender,
            "receiver": Receiver,
            "contents": Contents
        })

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "SMS")

    def sendFax(self, CorpNum, MgtKeyType, MgtKey, Sender, Receiver, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        postData = self._stringtify({
            "sender": Sender,
            "receiver": Receiver
        })

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey, postData, CorpNum, UserID, "FAX")

    def getLogs(self, CorpNum, MgtKeyType, MgtKey):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        return self._httpget('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + "/Logs", CorpNum)

    def attachFile(self, CorpNum, MgtKeyType, MgtKey, FilePath, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")
        if FilePath == None or FilePath == "":
            raise PopbillException(-99999999, "파일 경로가 입력되지 않았습니다.")

        files = []
        try:
            with open(FilePath, "rb") as F:
                files = [File(fieldName='Filedata',
                              fileName=F.name,
                              fileData=F.read())]
        except IOError:
            raise PopbillException(-99999999, "해당경로에 파일이 없거나 읽을 수 없습니다.")

        return self._httppost_files('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + '/Files', None, files, CorpNum, UserID)

    def getFiles(self, CorpNum, MgtKeyType, MgtKey):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        return self._httpget('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + "/Files", CorpNum)

    def deleteFile(self, CorpNum, MgtKeyType, MgtKey, FileID, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")
        if FileID == None or FileID == "":
            raise PopbillException(-99999999, "파일아이디가 입력되지 않았습니다.")

        postData = ''

        return self._httppost('/Taxinvoice/' + MgtKeyType + "/" + MgtKey + "/Files/" + FileID, postData, CorpNum,
                              UserID, 'DELETE')

    def getPopUpURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=POPUP', CorpNum, UserID)

        return result.url

    def getViewURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=VIEW', CorpNum, UserID)

        return result.url

    def getPrintURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=PRINT', CorpNum, UserID)

        return result.url

    def getEPrintURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=EPRINT', CorpNum, UserID)

        return result.url

    def getMailURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):
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
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '?TG=MAIL', CorpNum, UserID)

        return result.url

    def getInfos(self, CorpNum, MgtKeyType, MgtKeyList):
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
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        return self._httppost('/Taxinvoice/' + MgtKeyType, postData, CorpNum)

    def getMassPrintURL(self, CorpNum, MgtKeyType, MgtKeyList, UserID=None):
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
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        Result = self._httppost('/Taxinvoice/' + MgtKeyType + "?Print", postData, CorpNum, UserID)

        return Result.url

    def search(self, CorpNum, MgtKeyType, DType, SDate, EDate, State, Type, TaxType, LateOnly, TaxRegIDYN, TaxRegIDType,
               TaxRegID, Page, PerPage, Order, UserID=None, QString=None, InterOPYN=None, IssueType=None):
        """ 목록 조회
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKeyType : 세금계산서유형, SELL-매출, BUY-매입, TRUSTEE-위수탁
                DType : 일자유형, R-등록일시, W-작성일자, I-발행일시 중 택 1
                SDate : 시작일자, 표시형식(yyyyMMdd)
                EDate : 종료일자, 표시형식(yyyyMMdd)
                State : 상태코드, 2,3번째 자리에 와일드카드(*) 사용가능
                Type : 문서형태 배열, N-일반세금계산서, M-수정세금계산서
                TaxType : 과세형태 배열, T-과세, N-면세, Z-영세
                LateOnly : 지연발행, 공백-전체조회, 0-정상발행조회, 1-지연발행 조회
                TaxRegIdYN : 종사업장번호 유무, 공백-전체조회, 0-종사업장번호 없음 1-종사업장번호 있음
                TaxRegIDType : 종사업장번호 사업자유형, S-공급자, B-공급받는자, T-수탁자
                TaxRegID : 종사업장번호, 콤마(,)로 구분하여 구성 ex)'0001,1234'
                Page : 페이지번호
                PerPage : 페이지당 목록개수
                Order : 정렬방향, D-내림차순, A-오름차순
                UserID : 팝빌 회원아이디
                QString : 거래처 정보, 거래처 상호 또는 사업자등록번호 기재, 미기재시 전체조회
                InterOPYN : 연동문서 여부, 공백-전체조회, 0-일반문서 조회, 1-연동문서 조회
                IssueType : 발행형태 배열, N-정발행, R-역발행, T-위수탁
            return
                조회목록 Object
            raise
                PopbillException
        """

        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")

        if DType == None or DType == '':
            raise PopbillException(-99999999, "일자유형이 입력되지 않았습니다.")

        if SDate == None or SDate == '':
            raise PopbillException(-99999999, "시작일자가 입력되지 않았습니다.")

        if EDate == None or EDate == '':
            raise PopbillException(-99999999, "종료일자가 입력되지 않았습니다.")

        uri = '/Taxinvoice/' + MgtKeyType
        uri += '?DType=' + DType
        uri += '&SDate=' + SDate
        uri += '&EDate=' + EDate
        uri += '&State=' + ','.join(State)
        uri += '&Type=' + ','.join(Type)
        uri += '&TaxType=' + ','.join(TaxType)
        uri += '&TaxRegIDType=' + TaxRegIDType
        uri += '&TaxRegID=' + TaxRegID
        uri += '&Page=' + str(Page)
        uri += '&PerPage=' + str(PerPage)
        uri += '&Order=' + Order
        uri += '&InterOPYN=' + InterOPYN

        if LateOnly != '':
            uri += '&LateOnly=' + LateOnly
        if TaxRegIDYN != '':
            uri += '&TaxRegIDType=' + TaxRegIDType

        if QString is not None:
            uri += '&QString=' + QString

        if IssueType is not None:
            uri += '&IssueType=' + ','.join(IssueType)

        return self._httpget(uri, CorpNum, UserID)

    def attachStatement(self, CorpNum, MgtKeyType, MgtKey, ItemCode, StmtMgtKey, UserID=None):
        """ 전자명세서 첨부
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKeyType : 세금계산서 유형, SELL-매출, BUY-매입, TRUSTEE-위수탁
                MgtKey : 세금계산서 문서관리번호
                StmtCode : 명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
                StmtMgtKey : 전자명세서 문서관리번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """

        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        uri = '/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '/AttachStmt'

        postData = self._stringtify({"ItemCode": ItemCode, "MgtKey": StmtMgtKey})

        return self._httppost(uri, postData, CorpNum, UserID)

    def detachStatement(self, CorpNum, MgtKeyType, MgtKey, ItemCode, StmtMgtKey, UserID=None):
        """ 전자명세서 첨부해제
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKeyType : 세금계산서 유형, SELL-매출, BUY-매입, TRUSTEE-위수탁
                MgtKey : 세금계산서 문서관리번호
                StmtCode : 명세서 종류코드, 121-명세서, 122-청구서, 123-견적서, 124-발주서 125-입금표, 126-영수증
                StmtMgtKey : 전자명세서 문서관리번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType not in self.__MgtKeyTypes:
            raise PopbillException(-99999999, "관리번호 형태가 올바르지 않습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        uri = '/Taxinvoice/' + MgtKeyType + '/' + MgtKey + '/DetachStmt'

        req = {}

        if ItemCode != None or ItemCode != '':
            req['ItemCode'] = ItemCode
        if StmtMgtKey != None or StmtMgtKey != '':
            req['MgtKey'] = StmtMgtKey

        postData = self._stringtify(req)

        return self._httppost(uri, postData, CorpNum, UserID)

    def assignMgtKey(self, CorpNum, MgtKeyType, ItemKey, MgtKey, UserID=None):
        """ 관리번호할당
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKeyType : 세금계산서 유형, SELL-매출, BUY-매입, TRUSTEE-위수탁
                ItemKey : 아이템키 (Search API로 조회 가능)
                MgtKey : 세금계산서에 할당할 파트너 관리 번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if MgtKeyType == None or MgtKeyType == '':
            raise PopbillException(-99999999, "세금계산서 발행유형이 입력되지 않았습니다.")

        if ItemKey == None or ItemKey == '':
            raise PopbillException(-99999999, "아이템키가 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == '':
            raise PopbillException(-99999999, "관리번호가 입력되지 않았습니다.")

        postDate = "MgtKey=" + MgtKey
        return self._httppost('/Taxinvoice/' + ItemKey + '/' + MgtKeyType, postDate, CorpNum, UserID, "",
                              "application/x-www-form-urlencoded; charset=utf-8")

    def listEmailConfig(self, CorpNum, UserID=None):
        """ 알림메일 전송목록 조회
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
               전자세금계산서 관련 메일전송 항목에 대한 전송여부 목록
            raise
                PopbillException
        """
        return self._httpget('/Taxinvoice/EmailSendConfig', CorpNum, UserID)

    def updateEmailConfig(self, Corpnum, EmailType, SendYN, UserID=None):
        """ 알림메일 전송설정 수정
            args
                CorpNum : 팝빌회원 사업자번호
                EmailType: 메일전송유형
                SendYN: 전송여부 (True-전송, False-미전송)
                UserID : 팝빌회원 아이디
            return
               처리결과. consist of code and message
            raise
                PopbillException
        """
        if EmailType == None or EmailType == '':
            raise PopbillException(-99999999, "메일전송 타입이 입력되지 않았습니다.")

        if SendYN == None or SendYN == '':
            raise PopbillException(-99999999, "메일전송 여부 항목이 입력되지 않았습니다.")

        uri = "/Taxinvoice/EmailSendConfig?EmailType=" + EmailType + "&SendYN=" + str(SendYN)
        return self._httppost(uri, "", Corpnum, UserID)

    def checkCertValidation(self, CorpNum, UserID=None):
        """ 팝빌에 등록된 공인인증서 유효성을 확인한다.
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
               처리결과. consist of code and message
            raise
                PopbillException
        """
        return self._httpget('/Taxinvoice/CertCheck', CorpNum, UserID)

    def getSealURL(self, CorpNum, UserID):
        """ 팝빌 인감 및 첨부문서 등록 URL
            args
                CorpNum : 회원 사업자번호
                UserID  : 회원 팝빌아이디
            return
                30초 보안 토큰을 포함한 url
            raise
                PopbillException
        """
        result = self._httpget('/?TG=SEAL', CorpNum, UserID)
        return result.url

    def getTaxCertURL(self, CorpNum, UserID):
        """ 공인인증서 등록 URL
            args
                CorpNum : 회원 사업자번호
                UserID  : 회원 팝빌아이디
            return
                30초 보안 토큰을 포함한 url
            raise
                PopbillException
        """
        result = self._httpget('/?TG=CERT', CorpNum, UserID)
        return result.url


class Taxinvoice(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class TaxinvoiceDetail(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class Contact(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
