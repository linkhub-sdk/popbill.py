# -*- coding: utf-8 -*-
# Module for Popbill Message API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Contributor : Linkhub Dev (code@linkhubcorp.com)
# Updated : 2025-08-27
# Thanks for your interest.
from .base import File, PopbillBase, PopbillException

try:
    from urllib import parse as parse
except ImportError:
    import urllib as parse


class MessageService(PopbillBase):

    __MsgTypes = ["SMS", "LMS", "MMS"]

    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("150")
        self._addScope("151")
        self._addScope("152")

    def getChargeInfo(self, CorpNum, MsgType, UserID=None):

        if MsgType == None or MsgType == "":
            raise PopbillException(-99999999, "문자 유형이 입력되지 않았습니다.")

        return self._httpget("/Message/ChargeInfo?Type=" + MsgType, CorpNum, UserID)

    def getAutoDenyList(self, CorpNum, UserID=None):

        return self._httpget("/Message/Denied", CorpNum, UserID)

    def getUnitCost(self, CorpNum, MsgType):

        if MsgType == None or MsgType == "":
            raise PopbillException(-99999999, "문자 유형이 입력되지 않았습니다.")

        result = self._httpget("/Message/UnitCost?Type=" + MsgType, CorpNum)
        return float(result.unitCost)

    def sendSMS(
        self, CorpNum, Sender, Receiver, ReceiverName, Contents, reserveDT,
        adsYN=False, UserID=None, SenderName=None, RequestNum=None,
    ):

        Messages = []
        Messages.append(
            MessageReceiver(
                snd=Sender,
                sndnm=SenderName,
                rcv=Receiver,
                rcvnm=ReceiverName,
                msg=Contents,
            )
        )

        return self.sendMessage(
            "SMS", CorpNum, Sender, "", "", Contents, Messages, reserveDT,
            adsYN, UserID, RequestNum
        )

    def sendSMS_multi(
        self,
        CorpNum,
        Sender,
        Contents,
        Messages,
        reserveDT,
        adsYN=False,
        UserID=None,
        RequestNum=None,
    ):


        return self.sendMessage(
            "SMS",
            CorpNum,
            Sender,
            "",
            "",
            Contents,
            Messages,
            reserveDT,
            adsYN,
            UserID,
            RequestNum,
        )

    def sendLMS(
        self,
        CorpNum,
        Sender,
        Receiver,
        ReceiverName,
        Subject,
        Contents,
        reserveDT,
        adsYN=False,
        UserID=None,
        SenderName=None,
        RequestNum=None,
    ):


        Messages = []
        Messages.append(
            MessageReceiver(
                snd=Sender,
                sndnm=SenderName,
                rcv=Receiver,
                rcvnm=ReceiverName,
                msg=Contents,
                sjt=Subject,
            )
        )

        return self.sendMessage(
            "LMS",
            CorpNum,
            Sender,
            "",
            Subject,
            Contents,
            Messages,
            reserveDT,
            adsYN,
            UserID,
            RequestNum,
        )

    def sendLMS_multi(
        self,
        CorpNum,
        Sender,
        Subject,
        Contents,
        Messages,
        reserveDT,
        adsYN=False,
        UserID=None,
        RequestNum=None,
    ):


        return self.sendMessage(
            "LMS",
            CorpNum,
            Sender,
            "",
            Subject,
            Contents,
            Messages,
            reserveDT,
            adsYN,
            UserID,
            RequestNum,
        )

    def sendMMS(
        self,
        CorpNum,
        Sender,
        Receiver,
        ReceiverName,
        Subject,
        Contents,
        filePath,
        reserveDT,
        adsYN=False,
        UserID=None,
        SenderName=None,
        RequestNum=None,
    ):

        Messages = []
        Messages.append(
            MessageReceiver(
                snd=Sender,
                sndnm=SenderName,
                rcv=Receiver,
                rcvnm=ReceiverName,
                msg=Contents,
                sjt=Subject,
            )
        )

        return self.sendMMS_Multi(
            CorpNum,
            Sender,
            Subject,
            Contents,
            Messages,
            filePath,
            reserveDT,
            adsYN,
            UserID,
            RequestNum,
        )

    def sendMMS_Multi(
        self,
        CorpNum,
        Sender,
        Subject,
        Contents,
        Messages,
        FilePath,
        reserveDT,
        adsYN=False,
        UserID=None,
        RequestNum=None,
    ):

        if Messages == None or len(Messages) < 1:
            raise PopbillException(-99999999, "문자 정보가 입력되지 않았습니다.")

        req = {}

        if Sender != None or Sender != "":
            req["snd"] = Sender
        if Contents != None or Contents != "":
            req["content"] = Contents
        if Subject != None or Subject != "":
            req["subject"] = Subject
        if reserveDT != None or reserveDT != "":
            req["sndDT"] = reserveDT
        if Messages != None or Messages != "":
            req["msgs"] = Messages
        if RequestNum != None or RequestNum != "":
            req["requestNum"] = RequestNum
        if adsYN:
            req["adsYN"] = True

        postData = self._stringtify(req)

        files = []
        try:
            with open(FilePath, "rb") as F:
                files = [File(fieldName="file", fileName=F.name, fileData=F.read())]
        except IOError:
            raise PopbillException(-99999999, "해당경로에 파일이 없거나 읽을 수 없습니다.")

        result = self._httppost_files("/MMS", postData, files, CorpNum, UserID)

        return result.receiptNum

    def sendMMSBinary(
        self,
        CorpNum,
        Sender,
        Receiver,
        ReceiverName,
        Subject,
        Contents,
        FileDatas,
        reserveDT,
        adsYN=False,
        UserID=None,
        SenderName=None,
        RequestNum=None,
    ):

        Messages = []
        Messages.append(
            MessageReceiver(
                snd=Sender,
                sndnm=SenderName,
                rcv=Receiver,
                rcvnm=ReceiverName,
                msg=Contents,
                sjt=Subject,
            )
        )

        return self.sendMMSBinary_Multi(
            CorpNum,
            Sender,
            Subject,
            Contents,
            Messages,
            FileDatas,
            reserveDT,
            adsYN,
            UserID,
            RequestNum,
        )

    def sendMMSBinary_Multi(
        self,
        CorpNum,
        Sender,
        Subject,
        Contents,
        Messages,
        FileDatas,
        reserveDT,
        adsYN=False,
        UserID=None,
        RequestNum=None,
    ):

        if Messages == None or len(Messages) < 1:
            raise PopbillException(-99999999, "문자 정보가 입력되지 않았습니다.")

        if FileDatas == None:
            raise PopbillException(-99999999, "파일 정보가 입력되지 않았습니다.")

        req = {}

        if Sender != None or Sender != "":
            req["snd"] = Sender
        if Contents != None or Contents != "":
            req["content"] = Contents
        if Subject != None or Subject != "":
            req["subject"] = Subject
        if reserveDT != None or reserveDT != "":
            req["sndDT"] = reserveDT
        if Messages != None or Messages != "":
            req["msgs"] = Messages
        if RequestNum != None or RequestNum != "":
            req["requestNum"] = RequestNum
        if adsYN:
            req["adsYN"] = True

        postData = self._stringtify(req)

        files = []
        for file in FileDatas:
            files.append(
                File(
                    fieldName="file",
                    fileName=file.fileName,
                    fileData=file.fileData,
                )
            )

        result = self._httppost_files("/MMS", postData, files, CorpNum, UserID)

        return result.receiptNum

    def sendXMS(
        self,
        CorpNum,
        Sender,
        Receiver,
        ReceiverName,
        Subject,
        Contents,
        reserveDT,
        adsYN=False,
        UserID=None,
        SenderName=None,
        RequestNum=None,
    ):


        Messages = []
        Messages.append(
            MessageReceiver(
                snd=Sender,
                sndnm=SenderName,
                rcv=Receiver,
                rcvnm=ReceiverName,
                msg=Contents,
                sjt=Subject,
            )
        )

        return self.sendMessage(
            "XMS",
            CorpNum,
            Sender,
            "",
            Subject,
            Contents,
            Messages,
            reserveDT,
            adsYN,
            UserID,
            RequestNum,
        )

    def sendXMS_multi(
        self,
        CorpNum,
        Sender,
        Subject,
        Contents,
        Messages,
        reserveDT,
        adsYN=False,
        UserID=None,
        RequestNum=None,
    ):


        return self.sendMessage(
            "XMS",
            CorpNum,
            Sender,
            "",
            Subject,
            Contents,
            Messages,
            reserveDT,
            adsYN,
            UserID,
            RequestNum,
        )

    def sendMessage(
        self,
        MsgType,
        CorpNum,
        Sender,
        SenderName,
        Subject,
        Contents,
        Messages,
        reserveDT,
        adsYN=False,
        UserID=None,
        RequestNum=None,
    ):

        if MsgType == None or MsgType == "":
            raise PopbillException(-99999999, "문자 유형이 입력되지 않았습니다.")

        if Messages == None or len(Messages) < 1:
            raise PopbillException(-99999999, "문자 정보가 입력되지 않았습니다.")


        req = {}

        if Sender != None or Sender != "":
            req["snd"] = Sender
        if SenderName != None or SenderName != "":
            req["sndnm"] = SenderName
        if Contents != None or Contents != "":
            req["content"] = Contents
        if Subject != None or Subject != "":
            req["subject"] = Subject
        if reserveDT != None or reserveDT != "":
            req["sndDT"] = reserveDT
        if Messages != None or Messages != "":
            req["msgs"] = Messages
        if RequestNum != None or RequestNum != "":
            req["requestnum"] = RequestNum
        if adsYN:
            req["adsYN"] = True

        postData = self._stringtify(req)

        result = self._httppost("/" + MsgType, postData, CorpNum, UserID)

        return result.receiptNum

    def getMessages(self, CorpNum, ReceiptNum, UserID=None):

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        return self._httpget("/Message/" + ReceiptNum, CorpNum, UserID)

    def getMessagesRN(self, CorpNum, RequestNum, UserID=None):

        if RequestNum == None or RequestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        return self._httpget("/Message/Get/" + RequestNum, CorpNum, UserID)

    def cancelReserve(self, CorpNum, ReceiptNum, UserID=None):

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        return self._httpget("/Message/" + ReceiptNum + "/Cancel", CorpNum, UserID)

    def cancelReserveRN(self, CorpNum, RequestNum, UserID=None):

        if RequestNum == None or RequestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        return self._httpget("/Message/Cancel/" + RequestNum, CorpNum, UserID)

    def cancelReservebyRCV(self, CorpNum, ReceiptNum, ReceiveNum, UserID=None):

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        postData = self._stringtify(ReceiveNum)

        return self._httppost(
            "/Message/" + ReceiptNum + "/Cancel", postData, CorpNum, UserID
        )

    def cancelReserveRNbyRCV(self, CorpNum, RequestNum, ReceiveNum, UserID=None):

        if RequestNum == None or RequestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        postData = self._stringtify(ReceiveNum)

        return self._httppost(
            "/Message/Cancel/" + RequestNum, postData, CorpNum, UserID
        )

    def search(
        self,
        CorpNum,
        SDate,
        EDate,
        State,
        Item,
        ReserveYN,
        SenderYN,
        Page,
        PerPage,
        Order,
        UserID=None,
        QString=None,
    ):

        uri = "/Message/Search"
        uri += "?SDate=" + SDate
        uri += "&EDate=" + EDate
        uri += "&State=" + ",".join(State)

        if Item is not None and len(Item) > 0:
            uri += "&Item=" + ",".join(Item)
        if ReserveYN is not None:
            uri += "&ReserveYN=" + str(ReserveYN)
        if SenderYN is not None:
            uri += "&SenderOnly=" + str(SenderYN)
        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)
        if PerPage is not None and (PerPage > 0 and PerPage <= 1000):
            uri += "&PerPage=" + str(PerPage)
        if Order is not None and Order != "":
            uri += "&Order=" + Order
        if QString is not None and QString != "":
            uri += "&QString=" + parse.quote(QString)

        return self._httpget(uri, CorpNum, UserID)

    def getURL(self, CorpNum, UserID, ToGo):

        result = self._httpget("/Message/?TG=" + ToGo, CorpNum, UserID)

        return result.url

    def checkSenderNumber(self, CorpNum, SenderNumber, UserID=None):

        if SenderNumber == None or SenderNumber == "":
            raise PopbillException(-99999999, "발신번호가 입력되지 않았습니다.")

        return self._httpget(
            "/Message/CheckSenderNumber/" + SenderNumber, CorpNum, UserID
        )

    def getSentListURL(self, CorpNum, UserID):

        result = self._httpget("/Message/?TG=BOX", CorpNum, UserID)
        return result.url

    def getSenderNumberMgtURL(self, CorpNum, UserID):

        result = self._httpget("/Message/?TG=SENDER", CorpNum, UserID)
        return result.url

    def getSenderNumberList(self, CorpNum, UserID=None):

        return self._httpget("/Message/SenderNumber", CorpNum, UserID)

    def getStates(self, Corpnum, reciptNumList, UserID=None):

        postData = self._stringtify(reciptNumList)

        return self._httppost("/Message/States", postData, Corpnum, UserID)

    def checkAutoDenyNumber(self, CorpNum, UserID=None):

        response = self._httpget("/Message/AutoDenyNumberInfo", CorpNum, UserID)

        return AutoDenyNumberInfo(**response.__dict__)


class MessageReceiver(object):
    def __init__(self, **kwargs):
        self.__dict__ = dict.fromkeys(
            ["snd", "rcv", "rcvnm", "msg", "sjt", "interOPRefKey"]
        )
        self.__dict__.update(kwargs)


class AutoDenyNumberInfo(object):
    def __init__(self, **kwargs):
        self.__dict__ = dict.fromkeys(["smsdenyNumber", "regDT"])
        self.__dict__.update(kwargs)
