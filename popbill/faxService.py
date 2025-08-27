# -*- coding: utf-8 -*-
# Module for Popbill FAX API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Contributor : Linkhub Dev (code@linkhubcorp.com)
# Updated : 2025-08-27
# Thanks for your interest.

from datetime import datetime

from .base import File, PopbillBase, PopbillException

try:
    from urllib import parse as parse
except ImportError:
    import urllib as parse


class FaxService(PopbillBase):

    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("160")
        self._addScope("161")

    def getChargeInfo(self, CorpNum, UserID=None, ReceiveNumType=None):

        url = "/FAX/ChargeInfo"
        if ReceiveNumType != None and ReceiveNumType != "":
            url = "/FAX/ChargeInfo?receiveNumType=" + parse.quote(ReceiveNumType)
        return self._httpget(url, CorpNum, UserID)

    def getURL(self, CorpNum, UserID, ToGo):

        result = self._httpget("/FAX/?TG=" + ToGo, CorpNum, UserID)

        return result.url

    def getSentListURL(self, CorpNum, UserID):

        result = self._httpget("/FAX/?TG=BOX", CorpNum, UserID)

        return result.url

    def getSenderNumberMgtURL(self, CorpNum, UserID):

        result = self._httpget("/FAX/?TG=SENDER", CorpNum, UserID)

        return result.url

    def getUnitCost(self, CorpNum, ReceiveNumType=None):

        url = "/FAX/UnitCost"

        if ReceiveNumType != None and ReceiveNumType != "":
            url = "/FAX/UnitCost?receiveNumType=" + parse.quote(ReceiveNumType)

        result = self._httpget(url, CorpNum)

        return int(result.unitCost)

    def search(
        self,
        CorpNum,
        SDate,
        EDate,
        State,
        ReserveYN,
        SenderOnly,
        Page,
        PerPage,
        Order,
        UserID=None,
        QString=None,
    ):

        uri = "/FAX/Search"
        uri += "?SDate=" + SDate
        uri += "&EDate=" + EDate

        if State is not None and len(State) > 0:
            uri += "&State=" + ",".join(State)
        if ReserveYN is not None:
            uri += "&ReserveYN=" + str(ReserveYN)
        if SenderOnly is not None:
            uri += "&SenderOnly=" + str(SenderOnly)
        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)
        if PerPage is not None and (PerPage > 0 and PerPage <= 1000):
            uri += "&PerPage=" + str(PerPage)
        if Order is not None and Order != "":
            uri += "&Order=" + Order
        if QString is not None and QString != "":
            uri += "&QString=" + parse.quote(QString)

        return self._httpget(uri, CorpNum, UserID)

    def getFaxResult(self, CorpNum, ReceiptNum, UserID=None):

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        return self._httpget("/FAX/" + ReceiptNum, CorpNum, UserID)

    def getFaxResultRN(self, CorpNum, RequestNum, UserID=None):

        if RequestNum == None or RequestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        return self._httpget("/FAX/Get/" + RequestNum, CorpNum, UserID)

    def cancelReserve(self, CorpNum, ReceiptNum, UserID=None):

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        return self._httpget("/FAX/" + ReceiptNum + "/Cancel", CorpNum, UserID)

    def cancelReserveRN(self, CorpNum, RequestNum, UserID=None):

        if RequestNum == None or RequestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        return self._httpget("/FAX/Cancel/" + RequestNum, CorpNum, UserID)

    def sendFax(
        self,
        CorpNum,
        SenderNum,
        ReceiverNum,
        ReceiverName,
        FilePath,
        ReserveDT=None,
        UserID=None,
        SenderName=None,
        adsYN=False,
        title=None,
        RequestNum=None,
    ):

        receivers = []
        receivers.append(FaxReceiver(receiveNum=ReceiverNum, receiveName=ReceiverName))

        return self.sendFax_multi(
            CorpNum,
            SenderNum,
            receivers,
            FilePath,
            ReserveDT,
            UserID,
            SenderName,
            adsYN,
            title,
            RequestNum,
        )

    def sendFax_multi(
        self,
        CorpNum,
        SenderNum,
        Receiver,
        FilePath,
        ReserveDT=None,
        UserID=None,
        SenderName=None,
        adsYN=False,
        title=None,
        RequestNum=None,
    ):
        if FilePath == None:
            raise PopbillException(-99999999, "파일경로가 입력되지 않았습니다.")

        req = {
            "snd": SenderNum,
            "sndnm": SenderName,
            "fCnt": 1 if type(FilePath) is str else len(FilePath),
            "rcvs": [],
            "sndDT": None,
        }

        if type(Receiver) is str:
            Receiver = FaxReceiver(receiveNum=Receiver)

        if type(Receiver) is FaxReceiver:
            Receiver = [Receiver]

        if adsYN:
            req["adsYN"] = True

        for r in Receiver:
            req["rcvs"].append(
                {
                    "rcv": r.receiveNum,
                    "rcvnm": r.receiveName,
                    "interOPRefKey": r.interOPRefKey,
                }
            )

        if ReserveDT != None:
            req["sndDT"] = ReserveDT

        if title != None:
            req["title"] = title

        if RequestNum != None:
            req["requestNum"] = RequestNum

        postData = self._stringtify(req)

        if type(FilePath) is str:
            FilePath = [FilePath]

        files = []

        for filePath in FilePath:
            with open(filePath, "rb") as f:
                files.append(File(fieldName="file", fileName=f.name, fileData=f.read()))
        result = self._httppost_files("/FAX", postData, files, CorpNum, UserID)

        return result.receiptNum

    def sendFaxBinary(
        self,
        CorpNum,
        SenderNum,
        ReceiverNum,
        ReceiverName,
        FileDatas,
        ReserveDT=None,
        UserID=None,
        SenderName=None,
        adsYN=False,
        title=None,
        RequestNum=None,
    ):

        receivers = []
        receivers.append(FaxReceiver(receiveNum=ReceiverNum, receiveName=ReceiverName))

        return self.sendFaxBinary_multi(
            CorpNum,
            SenderNum,
            receivers,
            FileDatas,
            ReserveDT,
            UserID,
            SenderName,
            adsYN,
            title,
            RequestNum,
        )

    def sendFaxBinary_multi(
        self,
        CorpNum,
        SenderNum,
        Receiver,
        FileDatas,
        ReserveDT=None,
        UserID=None,
        SenderName=None,
        adsYN=False,
        title=None,
        RequestNum=None,
    ):
        if FileDatas == None:
            raise PopbillException(-99999999, "파일 정보가 입력되지 않았습니다.")

        req = {
            "snd": SenderNum,
            "sndnm": SenderName,
            "fCnt": len(FileDatas),
            "rcvs": [],
            "sndDT": None,
        }

        if type(Receiver) is str:
            Receiver = FaxReceiver(receiveNum=Receiver)

        if type(Receiver) is FaxReceiver:
            Receiver = [Receiver]

        if adsYN:
            req["adsYN"] = True

        for r in Receiver:
            req["rcvs"].append(
                {
                    "rcv": r.receiveNum,
                    "rcvnm": r.receiveName,
                    "interOPRefKey": r.interOPRefKey,
                }
            )

        if ReserveDT != None:
            req["sndDT"] = ReserveDT

        if title != None:
            req["title"] = title

        if RequestNum != None:
            req["requestNum"] = RequestNum

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

        result = self._httppost_files("/FAX", postData, files, CorpNum, UserID)

        return result.receiptNum

    def resendFax(
        self,
        CorpNum,
        ReceiptNum,
        SenderNum,
        SenderName,
        ReceiverNum,
        ReceiverName,
        ReserveDT=None,
        UserID=None,
        title=None,
        RequestNum=None,
    ):

        receivers = None

        if ReceiverNum != "" or ReceiverName != "":
            receivers = []
            receivers.append(
                FaxReceiver(receiveNum=ReceiverNum, receiveName=ReceiverName)
            )
        return self.resendFax_multi(
            CorpNum,
            ReceiptNum,
            SenderNum,
            SenderName,
            receivers,
            ReserveDT,
            UserID,
            title,
            RequestNum,
        )

    def resendFax_multi(
        self,
        CorpNum,
        ReceiptNum,
        SenderNum,
        SenderName,
        Receiver,
        ReserveDT=None,
        UserID=None,
        title=None,
        RequestNum=None,
    ):

        req = {}

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        if SenderNum != "":
            req["snd"] = SenderNum

        if SenderName != "":
            req["sndnm"] = SenderName

        if ReserveDT != None:
            req["sndDT"] = ReserveDT

        if title != None:
            req["title"] = title

        if RequestNum != None:
            req["requestNum"] = RequestNum

        if Receiver != None:
            req["rcvs"] = []
            if type(Receiver) is str:
                Receiver = FaxReceiver(receiveNum=Receiver)
            if type(Receiver) is FaxReceiver:
                Receiver = [Receiver]
            for r in Receiver:
                req["rcvs"].append(
                    {
                        "rcv": r.receiveNum,
                        "rcvnm": r.receiveName,
                        "interOPRefKey": r.interOPRefKey,
                    }
                )

        postData = self._stringtify(req)

        return self._httppost(
            "/FAX/" + ReceiptNum, postData, CorpNum, UserID
        ).receiptNum

    def resendFaxRN(
        self,
        CorpNum,
        OrgRequestNum,
        SenderNum,
        SenderName,
        ReceiverNum,
        ReceiverName,
        ReserveDT=None,
        UserID=None,
        title=None,
        RequestNum=None,
    ):

        receivers = None

        if ReceiverNum != "" or ReceiverName != "":
            receivers = []
            receivers.append(
                FaxReceiver(receiveNum=ReceiverNum, receiveName=ReceiverName)
            )
        return self.resendFaxRN_multi(
            CorpNum,
            OrgRequestNum,
            SenderNum,
            SenderName,
            receivers,
            ReserveDT,
            UserID,
            title,
            RequestNum,
        )

    def resendFaxRN_multi(
        self,
        CorpNum,
        OrgRequestNum,
        SenderNum,
        SenderName,
        Receiver,
        ReserveDT=None,
        UserID=None,
        title=None,
        RequestNum=None,
    ):

        req = {}

        if OrgRequestNum == None or OrgRequestNum == "":
            raise PopbillException(-99999999, "원본 팩스 요청번호가 입력되지 않았습니다.")

        if SenderNum != "":
            req["snd"] = SenderNum

        if SenderName != "":
            req["sndnm"] = SenderName

        if ReserveDT != None:
            req["sndDT"] = ReserveDT

        if title != None:
            req["title"] = title

        if RequestNum != None:
            req["requestNum"] = RequestNum

        if Receiver != None:
            req["rcvs"] = []
            if type(Receiver) is str:
                Receiver = FaxReceiver(receiveNum=Receiver)
            if type(Receiver) is FaxReceiver:
                Receiver = [Receiver]
            for r in Receiver:
                req["rcvs"].append(
                    {
                        "rcv": r.receiveNum,
                        "rcvnm": r.receiveName,
                        "interOPRefKey": r.interOPRefKey,
                    }
                )

        postData = self._stringtify(req)

        return self._httppost(
            "/FAX/Resend/" + OrgRequestNum, postData, CorpNum, UserID
        ).receiptNum

    def getSenderNumberList(self, CorpNum, UserID=None):

        return self._httpget("/FAX/SenderNumber", CorpNum, UserID)

    def checkSenderNumber(self, CorpNum, SenderNumber, UserID=None):

        if SenderNumber == None or SenderNumber == "":
            raise PopbillException(-99999999, "발신번호가 입력되지 않았습니다.")

        return self._httpget("/FAX/CheckSenderNumber/" + SenderNumber, CorpNum, UserID)

    def getPreviewURL(self, CorpNum, ReceiptNum, UserID):

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        return self._httpget("/FAX/Preview/" + ReceiptNum, CorpNum, UserID).url


class FaxReceiver(object):
    def __init__(self, **kwargs):
        self.__dict__ = dict.fromkeys(
            ["receiveNum", "receiveName", "altSubject", "interOPRefKey"]
        )
        self.__dict__.update(kwargs)


class FileData(object):
    def __init__(self, **kwargs):
        self.__dict__ = dict.fromkeys(["fileName", "fileData"])
        self.__dict__.update(kwargs)
