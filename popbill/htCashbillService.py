# -*- coding: utf-8 -*-
# Module for Popbill Hometax Cashbill API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Contributor : Linkhub Dev (code@linkhubcorp.com)
# Updated : 2025-08-27
# Thanks for your interest.

from .base import PopbillBase, PopbillException


class HTCashbillService(PopbillBase):


    def __init__(self, LinkID, SecretKey):


        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("141")

    def getChargeInfo(self, CorpNum, UserID=None):


        return self._httpget("/HomeTax/Cashbill/ChargeInfo", CorpNum, UserID)

    def requestJob(self, CorpNum, Type, SDate, EDate, UserID=None):

        if Type == None or Type == "":
            raise PopbillException(-99999999, "현금영수증 유형이 입력되지 않았습니다.")

        uri = "/HomeTax/Cashbill/" + Type
        uri += "?SDate=" + SDate
        uri += "&EDate=" + EDate

        return self._httppost(uri, "", CorpNum, UserID).jobID

    def getJobState(self, CorpNum, JobID, UserID=None):

        if JobID == None or JobID == "":
            raise PopbillException(-99999999, "작업아이디가 입력되지 않았습니다.")

        return self._httpget("/HomeTax/Cashbill/" + JobID + "/State", CorpNum, UserID)

    def listActiveJob(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Cashbill/JobList", CorpNum, UserID)

    def search(self, CorpNum, JobID, TradeType, TradeUsage, Page, PerPage, Order, UserID=None):

        if JobID == None or JobID == "":
            raise PopbillException(-99999999, "작업아이디가 입력되지 않았습니다.")

        uri = "/HomeTax/Cashbill/" + JobID + "?TradeType="

        if TradeType is not None and len(TradeType) > 0:
            uri += ",".join(TradeType)

        if TradeUsage is not None and len(TradeUsage) > 0:
            uri += "&TradeUsage=" + ",".join(TradeUsage)

        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)

        if PerPage is not None and (PerPage > 0 and PerPage <= 1000):
            uri += "&PerPage=" + str(PerPage)

        if Order is not None and Order != "":
            uri += "&Order=" + Order

        return self._httpget(uri, CorpNum, UserID)

    def summary(self, CorpNum, JobID, TradeType, TradeUsage, UserID=None):

        if JobID == None or JobID == "":
            raise PopbillException(-99999999, "작업아이디가 입력되지 않았습니다.")

        uri = "/HomeTax/Cashbill/" + JobID + "/Summary" + "?TradeType="

        if TradeType is not None and len(TradeType) > 0:
            uri += ",".join(TradeType)
        if TradeUsage is not None and len(TradeUsage) > 0:
            uri += "&TradeUsage=" + ",".join(TradeUsage)

        return self._httpget(uri, CorpNum, UserID)

    def getFlatRatePopUpURL(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Cashbill?TG=CHRG", CorpNum, UserID).url

    def getCertificatePopUpURL(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Cashbill?TG=CERT", CorpNum, UserID).url

    def getFlatRateState(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Cashbill/Contract", CorpNum, UserID)

    def getCertificateExpireDate(self, CorpNum, UserID=None):

        return self._httpget(
            "/HomeTax/Cashbill/CertInfo", CorpNum, UserID
        ).certificateExpiration

    def checkCertValidation(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Cashbill/CertCheck", CorpNum, UserID)

    def registDeptUser(self, CorpNum, DeptUserID, DeptUserPWD, IdentityNum=None, UserID=None):

        req = {}
        req["id"] = DeptUserID
        req["pwd"] = DeptUserPWD
        req["secAuth"] = IdentityNum

        postData = self._stringtify(req)

        return self._httppost("/HomeTax/Cashbill/DeptUser", postData, CorpNum, UserID)

    def checkDeptUser(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Cashbill/DeptUser", CorpNum, UserID)

    def checkLoginDeptUser(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Cashbill/DeptUser/Check", CorpNum, UserID)

    def deleteDeptUser(self, CorpNum, UserID=None):

        return self._httppost(
            "/HomeTax/Cashbill/DeptUser", "", CorpNum, UserID, "DELETE"
        )
