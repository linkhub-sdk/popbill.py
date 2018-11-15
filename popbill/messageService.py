# -*- coding: utf-8 -*-
# Module for Popbill Message API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : John Yohan (yhjeong@linkhub.co.kr)
# Written : 2015-03-20
# Updated : 2018-08-09
# Thanks for your interest.
from .base import PopbillBase, PopbillException, File


class MessageService(PopbillBase):
    """ 팝빌 문자 API Service Implementation. """

    __MsgTypes = ["SMS", "LMS", "MMS"]

    def __init__(self, LinkID, SecretKey):
        """생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """
        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("150")
        self._addScope("151")
        self._addScope("152")

    def getChargeInfo(self, CorpNum, MsgType, UserID=None):
        """ 과금정보 확인
            args
                CorpNum : 회원 사업자번호
                MsgType : 문자전송 유형
                UserID : 팝빌 회원아이디
            return
                과금정보 객체
            raise
                PopbillException
        """
        if MsgType == None or MsgType == "":
            raise PopbillException(-99999999, "전송유형이 입력되지 않았습니다.")

        return self._httpget('/Message/ChargeInfo?Type=' + MsgType, CorpNum, UserID)

    def getAutoDenyList(self, CorpNum, UserID=None):
        """ 080수신거부 목록 확인
            args
                number : 수신거부번호
                regDT : 등록일시
            return
                수신거부 목록
            raise
                PopbillException
        """
        return self._httpget('/Message/Denied', CorpNum, UserID)

    def getUnitCost(self, CorpNum, MsgType):
        """ 문자 전송 단가 확인
            args
                CorpNum : 팝빌회원 사업자번호
                MsgType : 문자 유형(SMS, LMS)
            return
                전송 단가 by float
            raise
                PopbillException
        """
        if MsgType == None or MsgType == "":
            raise PopbillException(-99999999, "전송유형이 입력되지 않았습니다.")

        result = self._httpget('/Message/UnitCost?Type=' + MsgType, CorpNum)
        return float(result.unitCost)

    def sendSMS(self, CorpNum, Sender, Receiver, ReceiverName, Contents, reserveDT, adsYN=False, UserID=None,
                SenderName=None, RequestNum=None):
        """ 단문 문자메시지 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신번호
                Receiver : 수신번호
                ReceiverName : 수신자명
                Contents : 메시지 내용(90Byte 초과시 길이가 조정되어 전송됨)
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                SenderName : 발신자명
                RequestNum : 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """
        Messages = []
        Messages.append(MessageReceiver(
            snd=Sender,
            sndnm=SenderName,
            rcv=Receiver,
            rcvnm=ReceiverName,
            msg=Contents)
        )

        return self.sendMessage("SMS", CorpNum, Sender, '', '', Contents, Messages, reserveDT, adsYN, UserID,
                                RequestNum)

    def sendSMS_multi(self, CorpNum, Sender, Contents, Messages, reserveDT, adsYN=False, UserID=None, RequestNum=None):
        """ 단문 문자메시지 다량전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Contents : 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                RequestNum : 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """

        return self.sendMessage("SMS", CorpNum, Sender, '', '', Contents, Messages, reserveDT, adsYN, UserID,
                                RequestNum)

    def sendLMS(self, CorpNum, Sender, Receiver, ReceiverName, Subject, Contents, reserveDT, adsYN=False, UserID=None,
                SenderName=None, RequestNum=None):
        """ 장문 문자메시지 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신번호
                Receiver : 수신번호
                ReceiverName : 수신자명
                Subject : 메시지 제목
                Contents : 메시지 내용(2000Byte 초과시 길이가 조정되어 전송됨)
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                SenderName : 발신자명
                RequestNum = 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """

        Messages = []
        Messages.append(MessageReceiver(
            snd=Sender,
            sndnm=SenderName,
            rcv=Receiver,
            rcvnm=ReceiverName,
            msg=Contents,
            sjt=Subject)
        )

        return self.sendMessage("LMS", CorpNum, Sender, '', Subject, Contents, Messages, reserveDT, adsYN, UserID,
                                RequestNum)

    def sendLMS_multi(self, CorpNum, Sender, Subject, Contents, Messages, reserveDT, adsYN=False, UserID=None,
                      RequestNum=None):
        """ 장문 문자메시지 다량전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Subject : 장문 메시지 제목 (동보전송용)
                Contents : 장문 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                reserveDT : 예약시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                RequestNum = 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """

        return self.sendMessage("LMS", CorpNum, Sender, '', Subject, Contents, Messages, reserveDT, adsYN, UserID,
                                RequestNum)

    def sendMMS(self, CorpNum, Sender, Receiver, ReceiverName, Subject, Contents, filePath, reserveDT, adsYN=False,
                UserID=None, SenderName=None, RequestNum=None):
        """ 멀티 문자메시지 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신번호
                Receiver : 수신번호
                ReceiverName : 수신자명
                Subject : 메시지 제목
                Contents : 메시지 내용(2000Byte 초과시 길이가 조정되어 전송됨)
                filePath : 전송하고자 하는 파일 경로
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                SenderName : 발신자명
                RequestNum = 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """
        Messages = []
        Messages.append(MessageReceiver(
            snd=Sender,
            sndnm=SenderName,
            rcv=Receiver,
            rcvnm=ReceiverName,
            msg=Contents,
            sjt=Subject)
        )

        return self.sendMMS_Multi(CorpNum, Sender, Subject, Contents, Messages, filePath, reserveDT, adsYN, UserID,
                                  RequestNum)

    def sendMMS_Multi(self, CorpNum, Sender, Subject, Contents, Messages, FilePath, reserveDT, adsYN=False, UserID=None,
                      RequestNum=None):
        """ 멀티 문자메시지 다량 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Subject : 장문 메시지 제목 (동보전송용)
                Contents : 장문 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                FilePath : 전송하고자 하는 파일 경로
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                RequestNum = 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """
        if Messages == None or len(Messages) < 1:
            raise PopbillException(-99999999, "전송할 메시지가 입력되지 않았습니다.")

        req = {}

        if Sender != None or Sender != '':
            req['snd'] = Sender
        if Contents != None or Contents != '':
            req['content'] = Contents
        if Subject != None or Subject != '':
            req['subject'] = Subject
        if reserveDT != None or reserveDT != '':
            req['sndDT'] = reserveDT
        if Messages != None or Messages != '':
            req['msgs'] = Messages
        if RequestNum != None or RequestNum != '':
            req['requestNum'] = RequestNum
        if adsYN:
            req['adsYN'] = True

        postData = self._stringtify(req)

        files = []
        try:
            with open(FilePath, "rb") as F:
                files = [File(fieldName='file',
                              fileName=F.name,
                              fileData=F.read())]
        except IOError:
            raise PopbillException(-99999999, "해당경로에 파일이 없거나 읽을 수 없습니다.")

        result = self._httppost_files('/MMS', postData, files, CorpNum, UserID)

        return result.receiptNum

    def sendXMS(self, CorpNum, Sender, Receiver, ReceiverName, Subject, Contents, reserveDT, adsYN=False, UserID=None,
                SenderName=None, RequestNum=None):
        """ 단/장문 자동인식 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신번호
                Receiver : 수신번호
                ReceiverName : 수신자명
                Subject : 메시지 제목
                Contents : 메시지 내용(90Byte를 기준으로 문자유형이 자동인식 되어 전송)
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                RequestNum = 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """

        Messages = []
        Messages.append(MessageReceiver(
            snd=Sender,
            sndnm=SenderName,
            rcv=Receiver,
            rcvnm=ReceiverName,
            msg=Contents,
            sjt=Subject)
        )

        return self.sendMessage("XMS", CorpNum, Sender, '', Subject, Contents, Messages, reserveDT, adsYN, UserID,
                                RequestNum)

    def sendXMS_multi(self, CorpNum, Sender, Subject, Contents, Messages, reserveDT, adsYN=False, UserID=None,
                      RequestNum=None):
        """ 단/장문 자동인식 다량 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Subject : 장문 메시지 제목 (동보전송용)
                Contents : 장문 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                RequestNum = 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """

        return self.sendMessage("XMS", CorpNum, Sender, '', Subject, Contents, Messages, reserveDT, adsYN, UserID,
                                RequestNum)

    def sendMessage(self, MsgType, CorpNum, Sender, SenderName, Subject, Contents, Messages, reserveDT, adsYN=False,
                    UserID=None, RequestNum=None):
        """ 문자 메시지 전송
            args
                MsgType : 문자 전송 유형(단문:SMS, 장문:LMS, 단/장문:XMS)
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Subject : 장문 메시지 제목 (동보전송용)
                Contents : 장문 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
                RequestNum : 전송요청번호
            return
                접수번호 (receiptNum)
            raise
                PopbillException
        """
        if MsgType == None or MsgType == '':
            raise PopbillException(-99999999, "문자 전송 유형이 입력되지 않았습니다.")

        if Messages == None or len(Messages) < 1:
            raise PopbillException(-99999999, "전송할 메시지가 입력되지 않았습니다.")

        req = {}

        if Sender != None or Sender != '':
            req['snd'] = Sender
        if SenderName != None or SenderName != '':
            req['sndnm'] = SenderName
        if Contents != None or Contents != '':
            req['content'] = Contents
        if Subject != None or Subject != '':
            req['subject'] = Subject
        if reserveDT != None or reserveDT != '':
            req['sndDT'] = reserveDT
        if Messages != None or Messages != '':
            req['msgs'] = Messages
        if RequestNum != None or RequestNum != '':
            req['requestnum'] = RequestNum
        if adsYN:
            req['adsYN'] = True

        postData = self._stringtify(req)

        result = self._httppost('/' + MsgType, postData, CorpNum, UserID)

        return result.receiptNum

    def getMessages(self, CorpNum, ReceiptNum, UserID=None):
        """ 문자 전송결과 조회
            args
                CorpNum : 팝빌회원 사업자번호
                ReceiptNum : 전송요청시 발급받은 접수번호
                UserID : 팝빌회원 아이디
            return
                전송정보 as list
            raise
                PopbillException
        """
        if ReceiptNum == None or len(ReceiptNum) != 18:
            raise PopbillException(-99999999, "접수번호가 올바르지 않습니다.")

        return self._httpget('/Message/' + ReceiptNum, CorpNum, UserID)

    def getMessagesRN(self, CorpNum, RequestNum, UserID=None):
        """ 문자 전송결과 조회
            args
                CorpNum : 팝빌회원 사업자번호
                RequestNum : 전송요청시 할당한 전송요청번호
                UserID : 팝빌회원 아이디
            return
                전송정보 as list
            raise
                PopbillException
        """
        if RequestNum == None or RequestNum == '':
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        return self._httpget('/Message/Get/' + RequestNum, CorpNum, UserID)

    def cancelReserve(self, CorpNum, ReceiptNum, UserID=None):
        """ 문자 예약전송 취소
            args
                CorpNum : 팝빌회원 사업자번호
                ReceiptNum : 전송요청시 발급받은 접수번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if ReceiptNum == None or len(ReceiptNum) != 18:
            raise PopbillException(-99999999, "접수번호가 올바르지 않습니다.")

        return self._httpget('/Message/' + ReceiptNum + '/Cancel', CorpNum, UserID)

    def cancelReserveRN(self, CorpNum, RequestNum, UserID=None):
        """ 문자 예약전송 취소
            args
                CorpNum : 팝빌회원 사업자번호
                RequestNum : 전송요청시 할당한 전송요청번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        if RequestNum == None or RequestNum == '':
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        return self._httpget('/Message/Cancel/' + RequestNum, CorpNum, UserID)

    def search(self, CorpNum, SDate, EDate, State, Item, ReserveYN, SenderYN, Page, PerPage, Order, UserID=None, QString=None):
        """ 문자전송 목록조회
            args
                CorpNum : 팝빌회원 사업자번호
                SDate : 시작일자, 표시형식(yyyyMMdd)
                EDate : 종료일자, 표시형식(yyyyMMdd)
                State : 전송상태 배열, 1-대기, 2-성공, 3-실패, 4-취소
                Item : 검색대상, SMS-단문, LMS-장문, MMS-포토
                ReserveYN : 예약여부 0-전체조회, 1-예약전송 조회
                SenderYN : 개인조회 여부, 0-전체조회, 1-개인조회
                Page : 페이지번호
                PerPage : 페이지당 목록개수
                Order : 정렬방향, D-내림차순, A-오름차순
                UserID : 팝빌 회원아이디
                QString : 조회 검색어, 발신자명 또는 수신자명 기재
        """

        if SDate == None or SDate == '':
            raise PopbillException(-99999999, "시작일자가 입력되지 않았습니다.")

        if EDate == None or EDate == '':
            raise PopbillException(-99999999, "종료일자가 입력되지 않았습니다.")

        uri = '/Message/Search'
        uri += '?SDate=' + SDate
        uri += '&EDate=' + EDate
        uri += '&State=' + ','.join(State)
        uri += '&Item=' + ','.join(Item)
        uri += '&ReserveYN=' + ReserveYN
        uri += '&SenderYN=' + SenderYN
        uri += '&Page=' + str(Page)
        uri += '&PerPage=' + str(PerPage)
        uri += '&Order=' + Order

        if QString is not None:
            uri += '&QString=' + QString

        return self._httpget(uri, CorpNum, UserID)

    def getURL(self, CorpNum, UserID, ToGo):
        """ 문자 관련 팝빌 URL
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
                TOGO : BOX (전송내역조회 팝업)
            return
                팝빌 URL
            raise
                PopbillException
        """
        if ToGo == None or ToGo == '':
            raise PopbillException(-99999999, "TOGO값이 입력되지 않았습니다.")

        result = self._httpget('/Message/?TG=' + ToGo, CorpNum, UserID)

        return result.url

    def getSentListURL(self, CorpNum, UserID):
        """ 발신번호 관리 팝업 URL
            args
                CorpNum : 회원 사업자번호
                UserID  : 회원 팝빌아이디
            return
                30초 보안 토큰을 포함한 url
            raise
                PopbillException
        """
        result = self._httpget('/Message/?TG=BOX', CorpNum, UserID)
        return result.url

    def getSenderNumberMgtURL(self, CorpNum, UserID):
        """ 문자 전송내역 팝업 URL
            args
                CorpNum : 회원 사업자번호
                UserID  : 회원 팝빌아이디
            return
                30초 보안 토큰을 포함한 url
            raise
                PopbillException
        """
        result = self._httpget('/Message/?TG=SENDER', CorpNum, UserID)
        return result.url

    def getSenderNumberList(self, CorpNum, UserID=None):
        """ 문자 발신번호 목록 확인
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
            return
                처리결과. list of SenderNumber
            raise
                PopbillException
        """
        return self._httpget('/Message/SenderNumber', CorpNum, UserID)

    def getStates(self, Corpnum, reciptNumList, UserID=None):
        """ 전송내역 요약정보 확인
            args
                CorpNum : 팝빌회원 사업자번호
                reciptNumList : 문자전송 접수번호 배열
                UserID : 팝빌회원 아이디
            return
                전송정보 as list
            raise
                PopbillException
        """
        if reciptNumList == None or len(reciptNumList) < 1:
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        postData = self._stringtify(reciptNumList)

        return self._httppost('/Message/States', postData, Corpnum, UserID)


class MessageReceiver(object):
    def __init__(self, **kwargs):
        self.__dict__ = dict.fromkeys(['snd', 'rcv', 'rcvnm', 'msg', 'sjt'])
        self.__dict__.update(kwargs)
