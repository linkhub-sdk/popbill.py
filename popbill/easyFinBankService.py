# -*- coding: utf-8 -*-
# Module for Popbill EasyFinBank API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Contributor : Linkhub Dev (code@linkhubcorp.com)
# Updated : 2025-08-27
# Thanks for your interest.

from .base import PopbillBase, PopbillException

try:
    from urllib import parse as parse
except ImportError:
    import urllib as parse


class EasyFinBankService(PopbillBase):

    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)

        self._addScope("180")

    def registBankAccount(self, CorpNum, AccountInfo, UserID=None):
        if AccountInfo == None:
            raise PopbillException(-99999999, "계좌 정보가 입력되지 않았습니다.")

        uri = "/EasyFin/Bank/BankAccount/Regist"

        uri += "?UsePeriod=" + AccountInfo.UsePeriod

        postData = self._stringtify(AccountInfo)

        return self._httppost(uri, postData, CorpNum, UserID)

    def updateBankAccount(self, CorpNum, AccountInfo, UserID=None):

        if AccountInfo == None:
            raise PopbillException(-99999999, "계좌 정보가 입력되지 않았습니다.")

        uri = (
            "/EasyFin/Bank/BankAccount/"
            + AccountInfo.BankCode
            + "/"
            + AccountInfo.AccountNumber
            + "/Update"
        )

        postData = self._stringtify(AccountInfo)

        return self._httppost(uri, postData, CorpNum, UserID)

    def closeBankAccount(
        self, CorpNum, BankCode, AccountNumber, CloseType, UserID=None
    ):

        uri = "/EasyFin/Bank/BankAccount/Close"
        uri += "?BankCode=" + BankCode
        uri += "&AccountNumber=" + AccountNumber
        uri += "&CloseType=" + parse.quote(CloseType)

        return self._httppost(uri, "", CorpNum, UserID)

    def revokeCloseBankAccount(self, CorpNum, BankCode, AccountNumber, UserID=None):

        uri = "/EasyFin/Bank/BankAccount/RevokeClose"
        uri += "?BankCode=" + BankCode
        uri += "&AccountNumber=" + AccountNumber

        return self._httppost(uri, "", CorpNum, UserID)

    def deleteBankAccount(self, CorpNum, BankCode, AccountNumber, UserID=None):
        if BankCode == None or BankCode == "":
            raise PopbillException(-99999999, "기관코드가 입력되지 않았습니다.")

        if AccountNumber == None or AccountNumber == "":
            raise PopbillException(-99999999, "계좌번호가 입력되지 않았습니다.")

        uri = "/EasyFin/Bank/BankAccount/Delete"

        postData = (
            "{'BankCode':" + BankCode + ", 'AccountNumber':" + AccountNumber + "}"
        )

        return self._httppost(uri, postData, CorpNum, UserID)

    def getBankAccountMgtURL(self, CorpNum, UserID=None):

        return self._httpget("/EasyFin/Bank?TG=BankAccount", CorpNum, UserID).url

    def getBankAccountInfo(self, CorpNum, BankCode, AccountNumber, UserID=None):

        if BankCode == None or BankCode == "":
            raise PopbillException(-99999999, "기관코드가 입력되지 않았습니다.")

        if AccountNumber == None or AccountNumber == "":
            raise PopbillException(-99999999, "계좌번호가 입력되지 않았습니다.")


        uri = "/EasyFin/Bank/BankAccount/" + BankCode + "/" + AccountNumber

        return self._httpget(uri, CorpNum, UserID)

    def listBankAccount(self, CorpNum, UserID=None):

        return self._httpget("/EasyFin/Bank/ListBankAccount", CorpNum, UserID)

    def requestJob(self, CorpNum, BankCode, AccountNumber, SDate, EDate, UserID=None):

        uri = "/EasyFin/Bank/BankAccount"
        uri += "?AccountNumber=" + AccountNumber
        uri += "&BankCode=" + BankCode
        uri += "&SDate=" + SDate
        uri += "&EDate=" + EDate

        return self._httppost(uri, "", CorpNum, UserID).jobID

    def getJobState(self, CorpNum, JobID, UserID=None):

        if JobID == None or JobID == "":
            raise PopbillException(-99999999, "작업아이디가 입력되지 않았습니다.")

        return self._httpget("/EasyFin/Bank/" + JobID + "/State", CorpNum, UserID)

    def listActiveJob(self, CorpNum, UserID=None):

        return self._httpget("/EasyFin/Bank/JobList", CorpNum, UserID)

    def search(
        self,
        CorpNum,
        JobID,
        TradeType,
        SearchString,
        Page,
        PerPage,
        Order,
        UserID=None,
    ):

        if JobID == None or len(JobID) != 18:
            raise PopbillException(-99999999, "작업아이디(jobID)가 올바르지 않습니다.")

        uri = "/EasyFin/Bank/" + JobID + "?TradeType="

        if TradeType is not None and len(TradeType) > 0:
            uri += ",".join(TradeType)
        if SearchString is not None and SearchString != "":
            uri += "&SearchString=" + parse.quote(SearchString)
        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)
        if PerPage is not None and (PerPage > 0 and PerPage <= 1000):
            uri += "&PerPage=" + str(PerPage)
        if Order is not None and Order != "":
            uri += "&Order=" + Order

        return self._httpget(uri, CorpNum, UserID)

    def summary(self, CorpNum, JobID, TradeType, SearchString, UserID=None):

        if JobID == None or JobID == "":
            raise PopbillException(-99999999, "작업아이디가 입력되지 않았습니다.")

        uri = "/EasyFin/Bank/" + JobID + "/Summary" + "?TradeType="

        if TradeType is not None and len(TradeType) > 0:
            uri += ",".join(TradeType)
        if SearchString is not None and SearchString != "":
            uri += "&SearchString=" + parse.quote(SearchString)

        return self._httpget(uri, CorpNum, UserID)

    def saveMemo(self, CorpNum, TID, Memo, UserID=None):

        uri = "/EasyFin/Bank/SaveMemo"
        uri += "?TID=" + TID
        uri += "&Memo=" + parse.quote(Memo)

        return self._httppost(uri, "", CorpNum, UserID)

    def getFlatRatePopUpURL(self, CorpNum, UserID=None):

        return self._httpget("/EasyFin/Bank?TG=CHRG", CorpNum, UserID).url

    def getFlatRateState(self, CorpNum, BankCode, AccountNumber, UserID=None):

        if BankCode == None or BankCode == "":
            raise PopbillException(-99999999, "기관코드가 입력되지 않았습니다.")

        if AccountNumber == None or AccountNumber == "":
            raise PopbillException(-99999999, "계좌번호가 입력되지 않았습니다.")

        uri = "/EasyFin/Bank/Contract/" + BankCode + "/" + AccountNumber

        return self._httpget(uri, CorpNum, UserID)

    def getChargeInfo(self, CorpNum, UserID=None):

        return self._httpget("/EasyFin/Bank/ChargeInfo", CorpNum, UserID)


class BankAccountInfo(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
