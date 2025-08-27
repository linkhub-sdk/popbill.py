# -*- coding: utf-8 -*-
# Module for Popbill Statement API. It include base functionality of the
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


class StatementService(PopbillBase):


    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("121")
        self._addScope("122")
        self._addScope("123")
        self._addScope("124")
        self._addScope("125")
        self._addScope("126")

    def getChargeInfo(self, CorpNum, ItemCode, UserID=None):

        return self._httpget("/Statement/ChargeInfo/" + ItemCode, CorpNum, UserID)

    def getURL(self, CorpNum, UserID, ToGo):

        result = self._httpget("/Statement?TG=" + ToGo, CorpNum, UserID)

        return result.url

    def getUnitCost(self, CorpNum, ItemCode):

        result = self._httpget("/Statement/" + str(ItemCode) + "?cfg=UNITCOST", CorpNum)

        return float(result.unitCost)

    def checkMgtKeyInUse(self, CorpNum, ItemCode, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        try:
            result = self._httpget(
                "/Statement/" + str(ItemCode) + "/" + MgtKey, CorpNum
            )
            return result.itemKey != None and result.itemKey != ""

        except PopbillException as PE:
            if PE.code == -12000004:
                return False
            raise PE

    def FAXSend(self, CorpNum, statement, SendNum, ReceiveNum, UserID=None):

        if statement == None:
            raise PopbillException(-99999999, "전자명세서 정보가 입력되지 않았습니다.")

        statement.sendNum = SendNum
        statement.receiveNum = ReceiveNum

        postData = self._stringtify(statement)

        return self._httppost("/Statement", postData, CorpNum, UserID, "FAX").receiptNum

    def registIssue(
        self, CorpNum, statement, Memo=None, UserID=None, EmailSubject=None
    ):

        if statement == None:
            raise PopbillException(-99999999, "전자명세서 정보가 입력되지 않았습니다.")

        if Memo != None or Memo != "":
            statement.memo = Memo

        if EmailSubject != None or EmailSubject != "":
            statement.emailSubject = EmailSubject

        postData = self._stringtify(statement)

        return self._httppost("/Statement", postData, CorpNum, UserID, "ISSUE")

    def register(self, CorpNum, statement, UserID=None):

        if statement == None:
            raise PopbillException(-99999999, "전자명세서 정보가 입력되지 않았습니다.")

        postData = self._stringtify(statement)

        return self._httppost("/Statement", postData, CorpNum, UserID)

    def update(self, CorpNum, ItemCode, MgtKey, Statement, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify(Statement)

        return self._httppost(
            "/Statement/" + str(ItemCode) + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "PATCH",
        )

    def issue(
        self,
        CorpNum,
        ItemCode,
        MgtKey,
        Memo=None,
        UserID=None,
        EmailSubject=None,
    ):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        req = {}
        postData = ""

        if Memo != None and Memo != "":
            req["memo"] = Memo
        if EmailSubject != None and EmailSubject != "":
            req["emailSubject"] = EmailSubject

        postData = self._stringtify(req)

        return self._httppost(
            "/Statement/" + str(ItemCode) + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "ISSUE",
        )

    def cancel(self, CorpNum, ItemCode, MgtKey, Memo=None, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = ""

        if Memo != None and Memo != "":
            postData = self._stringtify({"memo": Memo})

        return self._httppost(
            "/Statement/" + str(ItemCode) + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "CANCEL",
        )

    def delete(self, CorpNum, ItemCode, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httppost(
            "/Statement/" + str(ItemCode) + "/" + MgtKey,
            "",
            CorpNum,
            UserID,
            "DELETE",
        )

    def search(
        self,
        CorpNum,
        DType,
        SDate,
        EDate,
        State,
        ItemCode,
        Page,
        PerPage,
        Order,
        UserID=None,
        QString=None,
    ):

        uri = "/Statement/Search"
        uri += "?DType=" + DType
        uri += "&SDate=" + SDate
        uri += "&EDate=" + EDate

        if State is not None and len(State) > 0:
            uri += "&State=" + ",".join(State)

        if ItemCode is not None and len(ItemCode) > 0:
            uri += "&ItemCode=" + ",".join(ItemCode)

        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)

        if PerPage is not None and (PerPage > 0 and PerPage <= 1000):
            uri += "&PerPage=" + str(PerPage)

        if Order is not None and Order != "":
            uri += "&Order=" + Order

        if QString is not None and QString != "":
            uri += "&QString=" + parse.quote(QString)

        return self._httpget(uri, CorpNum, UserID)

    def getInfo(self, CorpNum, ItemCode, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget("/Statement/" + str(ItemCode) + "/" + MgtKey, CorpNum)

    def getInfos(self, CorpNum, ItemCode, MgtKeyList):

        if MgtKeyList == None or len(MgtKeyList) < 1:
            raise PopbillException(-99999999, "문서번호 목록이 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        return self._httppost("/Statement/" + str(ItemCode), postData, CorpNum)

    def getDetailInfo(self, CorpNum, ItemCode, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "?Detail", CorpNum
        )

    def sendEmail(self, CorpNum, ItemCode, MgtKey, ReceiverEmail, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify({"receiver": ReceiverEmail})

        return self._httppost(
            "/Statement/" + str(ItemCode) + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "EMAIL",
        )

    def sendSMS(
        self, CorpNum, ItemCode, MgtKey, Sender, Receiver, Contents, UserID=None
    ):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify(
            {"sender": Sender, "receiver": Receiver, "contents": Contents}
        )

        return self._httppost(
            "/Statement/" + str(ItemCode) + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "SMS",
        )

    def sendFAX(self, CorpNum, ItemCode, MgtKey, Sender, Receiver, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify({"sender": Sender, "receiver": Receiver})

        return self._httppost(
            "/Statement/" + str(ItemCode) + "/" + MgtKey,
            postData,
            CorpNum,
            UserID,
            "FAX",
        )

    def getLogs(self, CorpNum, ItemCode, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "/Logs", CorpNum
        )

    def getSealURL(self, CorpNum, UserID):

        result = self._httpget("/Member?TG=SEAL", CorpNum, UserID)
        return result.url

    def attachFile(self, CorpNum, ItemCode, MgtKey, FilePath, UserID=None, DisplayName=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")
        if FilePath == None or FilePath == "":
            raise PopbillException(-99999999, "파일경로가 입력되지 않았습니다.")

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
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "/Files",
            None,
            files,
            CorpNum,
            UserID,
        )

    def getFiles(self, CorpNum, ItemCode, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")


        return self._httpget(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "/Files", CorpNum
        )

    def deleteFile(self, CorpNum, ItemCode, MgtKey, FileID, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        if FileID == None or FileID == "":
            raise PopbillException(-99999999, "파일 식별번호가 입력되지 않았습니다.")

        postData = ""

        return self._httppost(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "/Files/" + FileID,
            postData,
            CorpNum,
            UserID,
            "DELETE",
        )

    def getPopUpURL(self, CorpNum, ItemCode, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")
        if ItemCode == None or ItemCode == "":
            raise PopbillException(-99999999, "명세서 종류 코드가 입력되지 않았습니다.")

        result = self._httpget(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "?TG=POPUP",
            CorpNum,
            UserID,
        )

        return result.url

    def getPrintURL(self, CorpNum, ItemCode, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "?TG=PRINT",
            CorpNum,
            UserID,
        )

        return result.url

    def getViewURL(self, CorpNum, ItemCode, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "?TG=VIEW",
            CorpNum,
            UserID,
        )

        return result.url

    def getEPrintURL(self, CorpNum, ItemCode, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "?TG=EPRINT",
            CorpNum,
            UserID,
        )

        return result.url

    def getMailURL(self, CorpNum, ItemCode, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/Statement/" + str(ItemCode) + "/" + MgtKey + "?TG=MAIL",
            CorpNum,
            UserID,
        )

        return result.url

    def getMassPrintURL(self, CorpNum, ItemCode, MgtKeyList, UserID=None):

        if MgtKeyList == None:
            raise PopbillException(-99999999, "문서번호 배열이 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        result = self._httppost(
            "/Statement/" + str(ItemCode) + "?Print", postData, CorpNum, UserID
        )

        return result.url

    def attachStatement(
        self, CorpNum, ItemCode, MgtKey, SubItemCode, SubMgtKey, UserID=None
    ):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        uri = "/Statement/" + ItemCode + "/" + MgtKey + "/AttachStmt"

        postData = self._stringtify({"ItemCode": ItemCode, "MgtKey": SubMgtKey})

        return self._httppost(uri, postData, CorpNum, UserID)

    def detachStatement(
        self, CorpNum, ItemCode, MgtKey, SubItemCode, SubMgtKey, UserID=None
    ):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")
        if ItemCode == None or ItemCode == "":
            raise PopbillException(-99999999, "명세서 종류 코드가 입력되지 않았습니다.")

        uri = "/Statement/" + ItemCode + "/" + MgtKey + "/DetachStmt"

        req = {}

        postData = self._stringtify({"ItemCode": ItemCode, "MgtKey": SubMgtKey})

        return self._httppost(uri, postData, CorpNum, UserID)

    def listEmailConfig(self, CorpNum, UserID=None):

        return self._httpget("/Statement/EmailSendConfig", CorpNum, UserID)

    def updateEmailConfig(self, Corpnum, EmailType, SendYN, UserID=None):

        if SendYN == None:
            raise PopbillException(-99999999, "메일 전송 여부가 입력되지 않았습니다.")

        uri = (
            "/Statement/EmailSendConfig?EmailType="
            + EmailType
            + "&SendYN="
            + str(SendYN)
        )
        return self._httppost(uri, "", Corpnum, UserID)


class Statement(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class StatementDetail(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
