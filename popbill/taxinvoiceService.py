# -*- coding: utf-8 -*-
# Module for Popbill Taxinvoice API. It include base functionality of the
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


class TaxinvoiceService(PopbillBase):

    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("110")

    def getChargeInfo(self, CorpNum, UserID=None):

        return self._httpget("/Taxinvoice/ChargeInfo", CorpNum, UserID)

    def getURL(self, CorpNum, UserID, ToGo):

        result = self._httpget("/Taxinvoice/?TG=" + ToGo, CorpNum, UserID)

        return result.url

    def getUnitCost(self, CorpNum):

        result = self._httpget("/Taxinvoice?cfg=UNITCOST", CorpNum)

        return float(result.unitCost)

    def getCertificateExpireDate(self, CorpNum):

        result = self._httpget("/Taxinvoice?cfg=CERT", CorpNum)

        return datetime.strptime(result.certificateExpiration, "%Y%m%d%H%M%S")

    def getEmailPublicKeys(self, CorpNum):

        return self._httpget("/Taxinvoice/EmailPublicKeys", CorpNum)

    def checkMgtKeyInUse(self, CorpNum, MgtKeyType, MgtKey):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        try:
            result = self._httpget("/Taxinvoice/" + MgtKeyType + "/" + MgtKey, CorpNum)
            return result.itemKey != None and result.itemKey != ""
        except PopbillException as PE:
            if PE.code == -11000005:
                return False
            raise PE

    def register(self, CorpNum, taxinvoice, writeSpecification=False, UserID=None):

        if taxinvoice == None:
            raise PopbillException(-99999999, "전자세금계산서 정보가 입력되지 않았습니다.")
        if writeSpecification:
            taxinvoice.writeSpecification = True

        postData = self._stringtify(taxinvoice)

        return self._httppost("/Taxinvoice", postData, CorpNum, UserID)

    def registIssue( self, CorpNum, taxinvoice, writeSpecification=False,
        forceIssue=False, dealInvoiceMgtKey=None, memo=None, emailSubject=None,
        UserID=None
    ):

        if taxinvoice == None:
            raise PopbillException(-99999999, "전자세금계산서 정보가 입력되지 않았습니다.")

        if writeSpecification:
            taxinvoice.writeSpecification = True

        if forceIssue:
            taxinvoice.forceIssue = True

        if dealInvoiceMgtKey != None and dealInvoiceMgtKey != "":
            taxinvoice.dealInvoiceMgtKey = dealInvoiceMgtKey

        if memo != None and memo != "":
            taxinvoice.memo = memo

        if emailSubject != None and emailSubject != "":
            taxinvoice.emailSubject = emailSubject

        postData = self._stringtify(taxinvoice)

        return self._httppost("/Taxinvoice", postData, CorpNum, UserID, "ISSUE")

    def update( self, CorpNum, MgtKeyType, MgtKey, taxinvoice, writeSpecification=False,
        UserID=None,
    ):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if taxinvoice == None:
            raise PopbillException(-99999999, "전자세금계산서 정보가 입력되지 않았습니다.")

        if writeSpecification:
            taxinvoice.writeSpecification = True

        postData = self._stringtify(taxinvoice)

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "PATCH",
        )

    def getInfo(self, CorpNum, MgtKeyType, MgtKey):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget("/Taxinvoice/" + MgtKeyType + "/" + MgtKey, CorpNum)

    def getDetailInfo(self, CorpNum, MgtKeyType, MgtKey):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?Detail", CorpNum
        )

    def getDetailInfoByItemKey(self, CorpNum, ItemKey):

        if ItemKey == None or ItemKey == "":
            raise PopbillException(-99999999, "팝빌 식별번호가 입력되지 않았습니다.")

        return self._httpget("/Taxinvoice/" + ItemKey + "?Detail", CorpNum)

    def getXML(self, CorpNum, MgtKeyType, MgtKey):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?XML", CorpNum
        )

    def delete(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            "",
            CorpNum,
            UserID,
            "DELETE",
        )

    def send( self, CorpNum, MgtKeyType, MgtKey, Memo=None, EmailSubject=None, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        req = {}

        if Memo != None and Memo != "":
            req["memo"] = Memo
        if EmailSubject != None and EmailSubject != "":
            req["emailSubject"] = EmailSubject

        postData = self._stringtify(req)

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "SEND",
        )

    def cancelSend(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if Memo != None and Memo != "":
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "CANCELSEND",
        )

    def accept(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if Memo != None and Memo != "":
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "ACCEPT",
        )

    def deny(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if Memo != None and Memo != "":
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "DENY",
        )

    def issue( self, CorpNum, MgtKeyType, MgtKey, Memo=None, EmailSubject=None,
        ForceIssue=False, UserID=None ):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        req = {"forceIssue": ForceIssue}

        if Memo != None and Memo != "":
            req["memo"] = Memo

        if EmailSubject != None and EmailSubject != "":
            req["emailSubject"] = EmailSubject

        postData = self._stringtify(req)

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "ISSUE",
        )

    def cancelIssue(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if Memo != None and Memo != "":
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "CANCELISSUE",
        )

    def registRequest(self, CorpNum, taxinvoice, memo=None, UserID=None):

        if memo != None and memo != "":
            taxinvoice.memo = memo

        postData = self._stringtify(taxinvoice)

        return self._httppost("/Taxinvoice", postData, CorpNum, UserID, "REQUEST")

    def request(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if Memo != None and Memo != "":
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "REQUEST",
        )

    def refuse(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if Memo != None and Memo != "":
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "REFUSE",
        )

    def cancelRequest(self, CorpNum, MgtKeyType, MgtKey, Memo=None, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if Memo != None and Memo != "":
            postData = self._stringtify({"memo": Memo})
        else:
            postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "CANCELREQUEST",
        )

    def sendToNTS(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "NTS",
        )

    def sendEmail(self, CorpNum, MgtKeyType, MgtKey, ReceiverEmail, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify({"receiver": ReceiverEmail})

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "EMAIL",
        )

    def sendSMS( self, CorpNum, MgtKeyType, MgtKey, Sender, Receiver, Contents,
        UserID=None,
    ):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify(
            {"sender": Sender, "receiver": Receiver, "contents": Contents}
        )

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "SMS",
        )

    def sendFax(self, CorpNum, MgtKeyType, MgtKey, Sender, Receiver, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify({"sender": Sender, "receiver": Receiver})

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "FAX",
        )

    def getLogs(self, CorpNum, MgtKeyType, MgtKey):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "/Logs", CorpNum
        )

    def attachFile(self, CorpNum, MgtKeyType, MgtKey, FilePath, UserID=None, DisplayName=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if FilePath == None or FilePath == "":
            raise PopbillException(-99999999, "파일 경로가 입력되지 않았습니다.")

        files = []
        try:
            with open(FilePath, "rb") as F:
                if DisplayName != None:
                    files = [File(fieldName="Filedata", fileName=DisplayName, fileData=F.read())]
                else:
                    files = [File(fieldName="Filedata", fileName=F.name, fileData=F.read())]

        except IOError:
            raise PopbillException(-99999999, "해당경로에 파일이 없거나 읽을 수 없습니다.")

        return self._httppost_files(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "/Files",
            None,
            files,
            CorpNum,
            UserID,
        )

    def getFiles(self, CorpNum, MgtKeyType, MgtKey):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "/Files", CorpNum
        )

    def deleteFile(self, CorpNum, MgtKeyType, MgtKey, FileID, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if FileID == None or FileID == "":
            raise PopbillException(-99999999, "파일 식별번호가 입력되지 않았습니다.")

        postData = ""

        return self._httppost(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "/Files/" + FileID,
            postData,
            CorpNum,
            UserID,
            "DELETE",
        )

    def getPopUpURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?TG=POPUP",
            CorpNum,
            UserID,
        )

        return result.url

    def getViewURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?TG=VIEW",
            CorpNum,
            UserID,
        )

        return result.url

    def getPrintURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?TG=PRINT",
            CorpNum,
            UserID,
        )

        return result.url

    def getOldPrintURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?TG=PRINTOLD",
            CorpNum,
            UserID,
        )

        return result.url

    def getPDFURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?TG=PDF",
            CorpNum,
            UserID,
        )

        return result.url

    def getEPrintURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?TG=EPRINT",
            CorpNum,
            UserID,
        )

        return result.url

    def getMailURL(self, CorpNum, MgtKeyType, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "?TG=MAIL",
            CorpNum,
            UserID,
        )

        return result.url

    def getInfos(self, CorpNum, MgtKeyType, MgtKeyList):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKeyList == None or len(MgtKeyList) < 1:
            raise PopbillException(-99999999, "문서번호 목록이 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        return self._httppost("/Taxinvoice/" + MgtKeyType, postData, CorpNum)

    def getMassPrintURL(self, CorpNum, MgtKeyType, MgtKeyList, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKeyList == None or len(MgtKeyList) < 1:
            raise PopbillException(-99999999, "문서번호 목록이 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        Result = self._httppost(
            "/Taxinvoice/" + MgtKeyType + "?Print", postData, CorpNum, UserID
        )

        return Result.url

    def search( self, CorpNum, MgtKeyType, DType, SDate, EDate, State, Type,
        TaxType, LateOnly, TaxRegIDYN, TaxRegIDType, TaxRegID, Page, PerPage, Order,
        UserID=None, QString=None, InterOPYN=None, IssueType=None, RegType=None,
        CloseDownState=None, MgtKey=None,
    ):
        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        uri = "/Taxinvoice/" + MgtKeyType
        uri += "?DType=" + DType
        uri += "&SDate=" + SDate
        uri += "&EDate=" + EDate

        if State is not None and len(State) > 0:
            uri += "&State=" + ",".join(State)

        if Type is not None and len(Type) > 0:
            uri += "&Type=" + ",".join(Type)

        if TaxType is not None and len(TaxType) > 0:
            uri += "&TaxType=" + ",".join(TaxType)

        if LateOnly is not None:
            uri += "&LateOnly=" + str(LateOnly)

        if Order is not None and Order != "":
            uri += "&Order=" + Order

        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)

        if PerPage is not None and (PerPage > 0 and PerPage <= 1000) :
            uri += "&PerPage=" + str(PerPage)

        if TaxRegIDType is not None and TaxRegIDType != "":
            uri += "&TaxRegIDType=" + TaxRegIDType

        if TaxRegIDYN is not None and TaxRegIDYN != "":
            uri += "&TaxRegIDYN=" + TaxRegIDYN

        if TaxRegID is not None and TaxRegID != "":
            uri += "&TaxRegID=" + TaxRegID

        if QString is not None and QString != "":
            uri += "&QString=" + parse.quote(QString)

        if InterOPYN is not None and InterOPYN != "":
            uri += "&InterOPYN=" + InterOPYN

        if IssueType is not None and len(IssueType) > 0:
            uri += "&IssueType=" + ",".join(IssueType)

        if RegType is not None and len(RegType) > 0:
            uri += "&RegType=" + ",".join(RegType)

        if CloseDownState is not None and len(CloseDownState) > 0:
            uri += "&CloseDownState=" + ",".join(CloseDownState)

        if MgtKey is not None and MgtKey != "":
            uri += "&MgtKey=" + MgtKey

        return self._httpget(uri, CorpNum, UserID)

    def attachStatement(
        self, CorpNum, MgtKeyType, MgtKey, ItemCode, StmtMgtKey, UserID=None
    ):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        uri = "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "/AttachStmt"

        postData = self._stringtify({"ItemCode": ItemCode, "MgtKey": StmtMgtKey})

        return self._httppost(uri, postData, CorpNum, UserID)

    def detachStatement(
        self, CorpNum, MgtKeyType, MgtKey, ItemCode, StmtMgtKey, UserID=None
    ):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        uri = "/Taxinvoice/" + MgtKeyType + "/" + MgtKey + "/DetachStmt"

        req = {}

        if ItemCode != None or ItemCode != "":
            req["ItemCode"] = ItemCode
        if StmtMgtKey != None or StmtMgtKey != "":
            req["MgtKey"] = StmtMgtKey

        postData = self._stringtify(req)

        return self._httppost(uri, postData, CorpNum, UserID)

    def assignMgtKey(self, CorpNum, MgtKeyType, ItemKey, MgtKey, UserID=None):

        if MgtKeyType == None:
            raise PopbillException(-99999999, "문서번호 유형이 입력되지 않았습니다.")

        if ItemKey == None or ItemKey == "":
            raise PopbillException(-99999999, "팝빌에서 할당한 식별번호가 입력되지 않았습니다.")

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postDate = "MgtKey=" + MgtKey

        return self._httppost(
            "/Taxinvoice/" + ItemKey + "/" + MgtKeyType,
            postDate,
            CorpNum,
            UserID,
            "",
            "application/x-www-form-urlencoded; charset=utf-8",
        )

    def listEmailConfig(self, CorpNum, UserID=None):

        return self._httpget("/Taxinvoice/EmailSendConfig", CorpNum, UserID)

    def updateEmailConfig(self, Corpnum, EmailType, SendYN, UserID=None):

        if SendYN == None or SendYN == "":
            raise PopbillException(-99999999, "메일 전송 여부가 입력되지 않았습니다.")

        uri = (
            "/Taxinvoice/EmailSendConfig?EmailType="
            + EmailType
            + "&SendYN="
            + str(SendYN)
        )
        return self._httppost(uri, "", Corpnum, UserID)

    def checkCertValidation(self, CorpNum, UserID=None):

        return self._httpget("/Taxinvoice/CertCheck", CorpNum, UserID)

    def getSealURL(self, CorpNum, UserID):

        result = self._httpget("/Member?TG=SEAL", CorpNum, UserID)
        return result.url

    def getTaxCertURL(self, CorpNum, UserID):

        result = self._httpget("/Member?TG=CERT", CorpNum, UserID)
        return result.url

    def getTaxCertInfo(self, CorpNum, UserID=None):

        return self._httpget("/Taxinvoice/Certificate", CorpNum)

    def bulkSubmit(
        self, CorpNum, SubmitID, taxinvoiceList, forceIssue=False, UserID=None
    ):

        tx = BulkTaxinvoiceSubmit(forceIssue=forceIssue, invoices=taxinvoiceList)

        postData = self._stringtify(tx)

        btx = postData.encode("utf-8")

        return self._httpBulkPost(
            "/Taxinvoice", btx, SubmitID, CorpNum, UserID, "BULKISSUE"
        )

    def getBulkResult(self, CorpNum, SubmitID, UserID=None):

        if SubmitID == None or SubmitID == "":
            raise PopbillException(-99999999, "제출아이디가 입력되지 않았습니다.")

        return self._httpget("/Taxinvoice/BULK/" + SubmitID + "/State", CorpNum, UserID)

    def getSendToNTSConfig(self, CorpNum):

        return self._httpget("/Taxinvoice/SendToNTSConfig", CorpNum).sendToNTS


class Taxinvoice(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class TaxinvoiceDetail(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class Contact(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class BulkTaxinvoiceSubmit(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class BulkTaxinvoiceIssueResult(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
