# -*- coding: utf-8 -*-
# Module for Popbill Cashbill API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Contributor : Linkhub Dev (code@linkhubcorp.com)
# Updated : 2025-08-27
# Thanks for your interest.

from datetime import datetime

from .base import PopbillBase, PopbillException


class CashbillService(PopbillBase):
    """팝빌 현금영수증 API Service Implementation."""

    def __init__(self, LinkID, SecretKey):


        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("140")

    def getChargeInfo(self, CorpNum, UserID=None):

        return self._httpget("/Cashbill/ChargeInfo", CorpNum, UserID)

    def getURL(self, CorpNum, UserID, ToGo):

        result = self._httpget("/Cashbill?TG=" + ToGo, CorpNum, UserID)

        return result.url

    def getUnitCost(self, CorpNum):

        result = self._httpget("/Cashbill?cfg=UNITCOST", CorpNum)

        return float(result.unitCost)

    def checkMgtKeyInUse(self, CorpNum, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        try:
            result = self._httpget("/Cashbill/" + MgtKey, CorpNum)

            return result.itemKey != None and result.itemKey != ""

        except PopbillException as PE:
            if PE.code == -14000003:
                return False
            raise PE

    def registIssue(self, CorpNum, cashbill, Memo, UserID=None, EmailSubject=None):

        if cashbill == None:
            raise PopbillException(-99999999, "현금영수증 정보가 입력되지 않았습니다.")

        postData = ""

        if Memo != None or Memo != "":
            cashbill.memo = Memo

        if EmailSubject != None or EmailSubject != "":
            cashbill.emailSubject = EmailSubject

        postData = self._stringtify(cashbill)

        response = self._httppost("/Cashbill", postData, CorpNum, UserID, "ISSUE")

        if response.tradeDT != None:
            delattr(response, "tradeDT")

        return response

    def bulkSubmit(self, CorpNum, SubmitID, cashbillList, UserID=None):

        cb = BulkCashbillSubmit(cashbills=cashbillList)

        postData = self._stringtify(cb)

        bcb = postData.encode("utf-8")

        response = self._httpBulkPost(
            "/Cashbill", bcb, SubmitID, CorpNum, UserID, "BULKISSUE"
        )

        return IssueResponse(**response.__dict__)

    def getBulkResult(self, CorpNum, SubmitID, UserID=None):

        if SubmitID == None or SubmitID == "":
            raise PopbillException(-99999999, "제출아이디가 입력되지 않았습니다.")

        response = self._httpget(
            "/Cashbill/BULK/" + SubmitID + "/State", CorpNum, UserID
        )

        return BulkCashbillResult(**response.__dict__)

    def register(self, CorpNum, cashbill, UserID=None):

        postData = self._stringtify(cashbill)

        return self._httppost("/Cashbill", postData, CorpNum, UserID)

    def revokeRegistIssue(
        self,
        CorpNum,
        mgtKey,
        orgConfirmNum,
        orgTradeDate,
        smssendYN=False,
        memo=None,
        UserID=None,
        isPartCancel=False,
        cancelType=None,
        supplyCost=None,
        tax=None,
        serviceFee=None,
        totalAmount=None,
        emailSubject=None,
        tradeDT=None,
    ):

        postData = self._stringtify(
            {
                "mgtKey": mgtKey,
                "orgConfirmNum": orgConfirmNum,
                "orgTradeDate": orgTradeDate,
                "smssendYN": smssendYN,
                "memo": memo,
                "isPartCancel": isPartCancel,
                "cancelType": cancelType,
                "supplyCost": supplyCost,
                "tax": tax,
                "serviceFee": serviceFee,
                "totalAmount": totalAmount,
                "emailSubject": emailSubject,
                "tradeDT": tradeDT,
            }
        )

        return self._httppost("/Cashbill", postData, CorpNum, UserID, "REVOKEISSUE")

    def revokeRegister(
        self,
        CorpNum,
        mgtKey,
        orgConfirmNum,
        orgTradeDate,
        smssendYN=False,
        UserID=None,
        isPartCancel=False,
        cancelType=None,
        supplyCost=None,
        tax=None,
        serviceFee=None,
        totalAmount=None,
    ):

        postData = self._stringtify(
            {
                "mgtKey": mgtKey,
                "orgConfirmNum": orgConfirmNum,
                "orgTradeDate": orgTradeDate,
                "smssendYN": smssendYN,
                "isPartCancel": isPartCancel,
                "cancelType": cancelType,
                "supplyCost": supplyCost,
                "tax": tax,
                "serviceFee": serviceFee,
                "totalAmount": totalAmount,
            }
        )

        return self._httppost("/Cashbill", postData, CorpNum, UserID, "REVOKE")

    def update(self, CorpNum, MgtKey, cashbill, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify(cashbill)

        return self._httppost("/Cashbill/" + MgtKey, postData, CorpNum, UserID, "PATCH")

    def issue(self, CorpNum, MgtKey, Memo=None, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = ""
        req = {}

        if Memo != None or Memo != "":
            req["memo"] = Memo

        postData = self._stringtify(req)

        return self._httppost("/Cashbill/" + MgtKey, postData, CorpNum, UserID, "ISSUE")

    def cancelIssue(self, CorpNum, MgtKey, Memo=None, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = ""
        req = {}

        if Memo != None or Memo != "":
            req["memo"] = Memo

        postData = self._stringtify(req)

        return self._httppost(
            "/Cashbill/" + MgtKey, postData, CorpNum, UserID, "CANCELISSUE"
        )

    def delete(self, CorpNum, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httppost("/Cashbill/" + MgtKey, "", CorpNum, UserID, "DELETE")

    def search(
        self,
        CorpNum,
        DType,
        SDate,
        EDate,
        State,
        TradeType,
        TradeUsage,
        TaxationType,
        Page,
        PerPage,
        Order,
        UserID=None,
        QString=None,
        TradeOpt=None,
        FranchiseTaxRegID=None,
    ):

        uri = "/Cashbill/Search"
        uri += "?DType=" + DType
        uri += "&SDate=" + SDate
        uri += "&EDate=" + EDate

        if State is not None and len(State) > 0:
            uri += "&State=" + ",".join(State)
        if TradeType is not None and len(TradeType) > 0:
            uri += "&TradeType=" + ",".join(TradeType)
        if TradeUsage is not None and len(TradeUsage) > 0:
            uri += "&TradeUsage=" + ",".join(TradeUsage)
        if TaxationType is not None and len(TaxationType) > 0:
            uri += "&TaxationType=" + ",".join(TaxationType)
        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)
        if PerPage is not None and (PerPage > 0 and PerPage <= 1000) :
            uri += "&PerPage=" + str(PerPage)
        if Order is not None and Order != "":
            uri += "&Order=" + Order
        if QString is not None and QString != "":
            uri += "&QString=" + QString
        if TradeOpt is not None and len(TradeOpt) > 0:
            uri += "&TradeOpt=" + ",".join(TradeOpt)
        if FranchiseTaxRegID is not None and FranchiseTaxRegID != "":
            uri += "&FranchiseTaxRegID=" + FranchiseTaxRegID

        response = self._httpget(uri, CorpNum, UserID)
        return CBSearchResult(**response.__dict__)

    def getInfo(self, CorpNum, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        resposne = self._httpget("/Cashbill/" + MgtKey, CorpNum)
        return CashbillInfo(**resposne.__dict__)

    def getInfos(self, CorpNum, MgtKeyList):

        if MgtKeyList == None or len(MgtKeyList) < 1:
            raise PopbillException(-99999999, "문서번호 목록이 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        response = self._httppost("/Cashbill/States", postData, CorpNum)
        return [CashbillInfo(**info.__dict__) for info in response]

    def getDetailInfo(self, CorpNum, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget("/Cashbill/" + MgtKey + "?Detail", CorpNum)

    def sendEmail(self, CorpNum, MgtKey, ReceiverEmail, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        postData = self._stringtify({"receiver": ReceiverEmail})

        return self._httppost("/Cashbill/" + MgtKey, postData, CorpNum, UserID, "EMAIL")

    def sendSMS(self, CorpNum, MgtKey, Sender, Receiver, Contents, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")


        postData = self._stringtify(
            {"sender": Sender, "receiver": Receiver, "contents": Contents}
        )

        return self._httppost("/Cashbill/" + MgtKey, postData, CorpNum, UserID, "SMS")

    def sendFAX(self, CorpNum, MgtKey, Sender, Receiver, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")


        postData = self._stringtify({"sender": Sender, "receiver": Receiver})

        return self._httppost("/Cashbill/" + MgtKey, postData, CorpNum, UserID, "FAX")

    def getLogs(self, CorpNum, MgtKey):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        return self._httpget("/Cashbill/" + MgtKey + "/Logs", CorpNum)

    def getPopUpURL(self, CorpNum, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget("/Cashbill/" + MgtKey + "?TG=POPUP", CorpNum, UserID)

        return result.url

    def getViewURL(self, CorpNum, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget("/Cashbill/" + MgtKey + "?TG=VIEW", CorpNum, UserID)

        return result.url

    def getPDFURL(self, CorpNum, MgtKey, UserID=None):
        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget("/Cashbill/" + MgtKey + "?TG=PDF", CorpNum, UserID)

        return result.url

    def getPrintURL(self, CorpNum, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget("/Cashbill/" + MgtKey + "?TG=PRINT", CorpNum, UserID)

        return result.url

    def getEPrintURL(self, CorpNum, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget("/Cashbill/" + MgtKey + "?TG=EPRINT", CorpNum, UserID)

        return result.url

    def getMailURL(self, CorpNum, MgtKey, UserID=None):

        if MgtKey == None or MgtKey == "":
            raise PopbillException(-99999999, "문서번호가 입력되지 않았습니다.")

        result = self._httpget("/Cashbill/" + MgtKey + "?TG=MAIL", CorpNum, UserID)

        return result.url

    def getMassPrintURL(self, CorpNum, MgtKeyList, UserID=None):

        if MgtKeyList == None:
            raise PopbillException(-99999999, "문서번호 배열이 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        result = self._httppost("/Cashbill/Prints", postData, CorpNum, UserID)

        return result.url

    def listEmailConfig(self, CorpNum, UserID=None):

        return self._httpget("/Cashbill/EmailSendConfig", CorpNum, UserID)

    def updateEmailConfig(self, Corpnum, EmailType, SendYN, UserID=None):

        if EmailType == None or EmailType == "":
            raise PopbillException(-99999999, "메일전송 타입이 입력되지 않았습니다.")

        if SendYN == None or SendYN == "":
            raise PopbillException(-99999999, "메일전송 여부 항목이 입력되지 않았습니다.")

        uri = (
            "/Cashbill/EmailSendConfig?EmailType="
            + EmailType
            + "&SendYN="
            + str(SendYN)
        )
        return self._httppost(uri, "", Corpnum, UserID)

    def assignMgtKey(self, CorpNum, ItemKey, MgtKey, UserID=None):

        if ItemKey == None or ItemKey == "":
            raise PopbillException(-99999999, "팝빌에서 할당한 식별번호가 입력되지 않았습니다.")

        postDate = "MgtKey=" + MgtKey
        return self._httppost(
            "/Cashbill/" + ItemKey,
            postDate,
            CorpNum,
            UserID,
            "",
            "application/x-www-form-urlencoded; charset=utf-8",
        )


class Cashbill(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class BulkCashbillSubmit(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class IssueResponse(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class BulkCashbillResult(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

        self.__dict__["issueResult"] = []
        for info in self.__dict__["issueResult"]:
            # tradeDT 제거
            if info.tradeDT != None:
                delattr(info, "tradeDT")

            # issueDT 추가
            if info.issueDT == None:
                now = datetime.now()
                info.issueDT = now.strftime("%Y%m%d%H%M%S")
            self.__dict__["issueResult"].append(
                BulkCashbillIssueResult(**info.__dict__)
            )


class BulkCashbillIssueResult(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class CashbillInfo(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class CBSearchResult(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        self.__dict__["list"] = [
            CashbillInfo(**info.__dict__) for info in kwargs["list"]
        ]
