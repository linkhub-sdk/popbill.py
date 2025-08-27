# -*- coding: utf-8 -*-
# Module for Popbill Hometax Taxinvoice API. It include base functionality of the
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


class HTTaxinvoiceService(PopbillBase):


    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("111")

    def getChargeInfo(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Taxinvoice/ChargeInfo", CorpNum, UserID)

    def requestJob(self, CorpNum, Type, DType, SDate, EDate, UserID=None):
        if Type == None or Type == "":
            raise PopbillException(-99999999, "전자세금계산서 유형이 입력되지 않았습니다.")

        uri = "/HomeTax/Taxinvoice/" + Type
        uri += "?DType=" + DType
        uri += "&SDate=" + SDate
        uri += "&EDate=" + EDate

        return self._httppost(uri, "", CorpNum, UserID).jobID

    def getJobState(self, CorpNum, JobID, UserID=None):

        if JobID == None or JobID == "":
            raise PopbillException(-99999999, "작업아이디가 입력되지 않았습니다.")

        return self._httpget("/HomeTax/Taxinvoice/" + JobID + "/State", CorpNum, UserID)

    def listActiveJob(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Taxinvoice/JobList", CorpNum, UserID)

    def search(
        self,CorpNum, JobID, Type, TaxType, PurposeType, TaxRegIDType, TaxRegIDYN,
        TaxRegID, Page, PerPage, Order, UserID=None, SearchString=None,
    ):

        if JobID == None or JobID == "":
            raise PopbillException(-99999999, "작업아이디가 입력되지 않았습니다.")

        uri = "/HomeTax/Taxinvoice/" + JobID + "?Type="

        if Type is not None and len(Type) > 0:
            uri += ",".join(Type)

        if TaxType is not None and len(TaxType) > 0:
            uri += "&TaxType=" + ",".join(TaxType)

        if PurposeType is not None and len(PurposeType) > 0:
            uri += "&PurposeType=" + ",".join(PurposeType)

        if TaxRegIDType is not None and TaxRegIDType != "":
            uri += "&TaxRegIDType=" + TaxRegIDType

        if TaxRegIDYN is not None and TaxRegIDYN != "":
            uri += "&TaxRegIDYN=" + TaxRegIDYN

        if TaxRegID is not None and TaxRegID != "":
            uri += "&TaxRegID=" + TaxRegID

        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)

        if PerPage is not None and (PerPage > 0 and PerPage <= 1000):
            uri += "&PerPage=" + str(PerPage)

        if Order is not None and Order != "":
            uri += "&Order=" + Order

        if SearchString is not None and SearchString != "":
            uri += "&SearchString=" + parse.quote(SearchString)

        return self._httpget(uri, CorpNum, UserID)

    def summary(
        self, CorpNum, JobID, Type, TaxType, PurposeType, TaxRegIDType, TaxRegIDYN,
        TaxRegID, UserID=None, SearchString=None,
    ):

        if JobID == None or JobID == "":
            raise PopbillException(-99999999, "작업아이디가 입력되지 않았습니다.")

        uri = "/HomeTax/Taxinvoice/" + JobID + "/Summary" + "?Type="

        if Type is not None and len(Type) > 0:
            uri += ",".join(Type)
        if TaxType is not None and len(TaxType) > 0:
            uri += "&TaxType=" + ",".join(TaxType)
        if PurposeType is not None and len(PurposeType) > 0:
            uri += "&PurposeType=" + ",".join(PurposeType)
        if TaxRegIDType is not None and TaxRegIDType != "":
            uri += "&TaxRegIDType=" + TaxRegIDType
        if TaxRegIDYN is not None and TaxRegIDYN != "":
            uri += "&TaxRegIDYN=" + TaxRegIDYN
        if TaxRegID is not None and TaxRegID != "":
            uri += "&TaxRegID=" + TaxRegID
        if SearchString is not None and SearchString != "":
            uri += "&SearchString=" + parse.quote(SearchString)

        return self._httpget(uri, CorpNum, UserID)

    def getTaxinvoice(self, CorpNum, NTSConfirmNum, UserID=None):

        if NTSConfirmNum == None or NTSConfirmNum == "":
            raise PopbillException(-99999999, "국세청승인번호가 입력되지 않았습니다.")

        return self._httpget("/HomeTax/Taxinvoice/" + NTSConfirmNum, CorpNum, UserID)

    def getXML(self, CorpNum, NTSConfirmNum, UserID=None):

        if NTSConfirmNum == None or NTSConfirmNum == "":
            raise PopbillException(-99999999, "국세청승인번호가 입력되지 않았습니다.")

        return self._httpget(
            "/HomeTax/Taxinvoice/" + NTSConfirmNum + "?T=xml", CorpNum, UserID
        )

    def getFlatRatePopUpURL(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Taxinvoice?TG=CHRG", CorpNum, UserID).url

    def getCertificatePopUpURL(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Taxinvoice?TG=CERT", CorpNum, UserID).url

    def getFlatRateState(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Taxinvoice/Contract", CorpNum, UserID)

    def getCertificateExpireDate(self, CorpNum, UserID=None):

        return self._httpget(
            "/HomeTax/Taxinvoice/CertInfo", CorpNum, UserID
        ).certificateExpiration

    def getPopUpURL(self, CorpNum, NTSConfirmNum, UserID=None):

        if NTSConfirmNum == None or NTSConfirmNum == "":
            raise PopbillException(-99999999, "국세청승인번호가 입력되지 않았습니다.")

        return self._httpget(
            "/HomeTax/Taxinvoice/" + NTSConfirmNum + "/PopUp", CorpNum, UserID
        ).url

    def getPrintURL(self, CorpNum, NTSConfirmNum, UserID=None):

        if NTSConfirmNum == None or NTSConfirmNum == "":
            raise PopbillException(-99999999, "국세청승인번호가 입력되지 않았습니다.")

        return self._httpget(
            "/HomeTax/Taxinvoice/" + NTSConfirmNum + "/Print", CorpNum, UserID
        ).url

    def checkCertValidation(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Taxinvoice/CertCheck", CorpNum, UserID)

    def registDeptUser(self, CorpNum, DeptUserID, DeptUserPWD, IdentityNum=None, UserID=None):

        req = {}
        req["id"] = DeptUserID
        req["pwd"] = DeptUserPWD
        req["secAuth"] = IdentityNum

        postData = self._stringtify(req)

        return self._httppost("/HomeTax/Taxinvoice/DeptUser", postData, CorpNum, UserID)

    def checkDeptUser(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Taxinvoice/DeptUser", CorpNum, UserID)

    def checkLoginDeptUser(self, CorpNum, UserID=None):

        return self._httpget("/HomeTax/Taxinvoice/DeptUser/Check", CorpNum, UserID)

    def deleteDeptUser(self, CorpNum, UserID=None):

        return self._httppost(
            "/HomeTax/Taxinvoice/DeptUser", "", CorpNum, UserID, "DELETE"
        )
