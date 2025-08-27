# -*- coding: utf-8 -*-
# Module for Popbill Base API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Contributor : Linkhub Dev (code@linkhubcorp.com)
# Updated : 2025-08-27
# Thanks for your interest.
import base64
import json
import zlib
from collections import namedtuple
# from functools import total_ordering
from hashlib import sha1
from io import BytesIO
from json import JSONEncoder
from time import time as stime

try:
    import http.client as httpclient
except ImportError:
    import httplib as httpclient

import linkhub
from linkhub import LinkhubException

ServiceID_REAL = "POPBILL"
ServiceID_TEST = "POPBILL_TEST"

ServiceURL_REAL = "popbill.linkhub.co.kr"
ServiceURL_TEST = "popbill-test.linkhub.co.kr"

ServiceURL_Static_REAL = "static-popbill.linkhub.co.kr"
ServiceURL_Static_TEST = "static-popbill-test.linkhub.co.kr"

ServiceURL_GA_REAL = "ga-popbill.linkhub.co.kr"
ServiceURL_GA_TEST = "ga-popbill-test.linkhub.co.kr"

APIVersion = "1.0"


def __with_metaclass(meta, *bases):
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, "temporary_class", (), {})


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PopbillBase(__with_metaclass(Singleton, object)):
    IsTest = False
    IPRestrictOnOff = True
    UseStaticIP = False
    UseGAIP = False
    UseLocalTimeYN = True

    def __init__(self, LinkID, SecretKey, timeOut=180):

        self.__linkID = LinkID
        self.__secretKey = SecretKey
        self.__scopes = ["member"]
        self.__tokenCache = {}
        self.__conn = None
        self.__connectedAt = stime()
        self.__timeOut = timeOut

    def _getConn(self):
        if stime() - self.__connectedAt >= self.__timeOut or self.__conn == None:
            if self.UseGAIP:
                self.__conn = httpclient.HTTPSConnection(
                    ServiceURL_GA_TEST if self.IsTest else ServiceURL_GA_REAL
                )
            elif self.UseStaticIP:
                self.__conn = httpclient.HTTPSConnection(
                    ServiceURL_Static_TEST if self.IsTest else ServiceURL_Static_REAL
                )
            else:
                self.__conn = httpclient.HTTPSConnection(
                    ServiceURL_TEST if self.IsTest else ServiceURL_REAL
                )

            self.__connectedAt = stime()
            return self.__conn
        else:
            return self.__conn

    def _addScope(self, newScope):
        self.__scopes.append(newScope)

    # 파트너 포인트 충전 팝업 URL 추가 - 2017/08/29
    def getPartnerURL(self, CorpNum, TOGO):

        try:
            return linkhub.getPartnerURL(
                self._getToken(CorpNum), TOGO, self.UseStaticIP, self.UseGAIP
            )
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getBalance(self, CorpNum):

        try:
            return linkhub.getBalance(
                self._getToken(CorpNum), self.UseStaticIP, self.UseGAIP
            )
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getPartnerBalance(self, CorpNum):

        try:
            return linkhub.getPartnerBalance(
                self._getToken(CorpNum), self.UseStaticIP, self.UseGAIP
            )
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getPopbillURL(self, CorpNum, UserID, ToGo):

        result = self._httpget("/Member?TG=" + ToGo, CorpNum, UserID)

        return result.url

    def getPaymentURL(self, CorpNum, UserID=None):

        result = self._httpget("/Member?TG=PAYMENT", CorpNum, UserID)

        return result.url

    def getUseHistoryURL(self, CorpNum, UserID=None):

        result = self._httpget("/Member?TG=USEHISTORY", CorpNum, UserID)

        return result.url

    def getAccessURL(self, CorpNum, UserID):

        result = self._httpget("/Member?TG=LOGIN", CorpNum, UserID)

        return result.url

    def getChargeURL(self, CorpNum, UserID):

        result = self._httpget("/Member?TG=CHRG", CorpNum, UserID)

        return result.url

    def checkIsMember(self, CorpNum):

        return self._httpget(
            "/Join?CorpNum=" + CorpNum + "&LID=" + self.__linkID, None, None
        )

    def joinMember(self, JoinInfo):

        JoinInfo.LinkID = self.__linkID

        postData = self._stringtify(JoinInfo)

        return self._httppost("/Join", postData)

    def checkID(self, checkID):

        return self._httpget("/IDCheck?ID=" + checkID)

    def getContactInfo(self, CorpNum, ContactID, UserID=None):

        postData = "{'id':" + "'" + ContactID + "'}"

        return self._httppost("/Contact", postData, CorpNum, UserID)

    def listContact(self, CorpNum, UserID=None):

        return self._httpget("/IDs", CorpNum, UserID)

    def updateContact(self, CorpNum, ContactInfo, UserID=None):

        postData = self._stringtify(ContactInfo)

        return self._httppost("/IDs", postData, CorpNum, UserID)

    def getCorpInfo(self, CorpNum, UserID=None):

        return self._httpget("/CorpInfo", CorpNum, UserID)

    def updateCorpInfo(self, CorpNum, CorpInfo, UserID=None):

        postData = self._stringtify(CorpInfo)

        return self._httppost("/CorpInfo", postData, CorpNum, UserID)

    def registContact(self, CorpNum, ContactInfo, UserID=None):

        postData = self._stringtify(ContactInfo)

        return self._httppost("/IDs/New", postData, CorpNum, UserID)

    def deleteContact(self, CorpNum, TargetUserID, UserID):

        return self._httppost('/Contact/Delete?ContactID=' + TargetUserID, None, CorpNum, UserID)

    def _getToken(self, CorpNum):

        if CorpNum == None or CorpNum == "":
            raise PopbillException(-99999999, "팝빌회원 사업자번호가 입력되지 않았습니다.")

        try:
            token = self.__tokenCache[CorpNum]
        except KeyError:
            token = None

        refreshToken = True

        if token != None:
            refreshToken = token.expiration[:-5] < linkhub.getTime(
                self.UseStaticIP, self.UseLocalTimeYN, self.UseGAIP
            )

        if refreshToken:
            try:
                token = linkhub.generateToken(
                    self.__linkID,
                    self.__secretKey,
                    ServiceID_TEST if self.IsTest else ServiceID_REAL,
                    CorpNum,
                    self.__scopes,
                    None if self.IPRestrictOnOff else "*",
                    self.UseStaticIP,
                    self.UseLocalTimeYN,
                    self.UseGAIP,
                )

                try:
                    del self.__tokenCache[CorpNum]
                except KeyError:
                    pass

                self.__tokenCache[CorpNum] = token

            except LinkhubException as LE:
                raise PopbillException(LE.code, LE.message)

        return token

    def getUseHistory(
            self,
            CorpNum,
            SDate,
            EDate,
            Page=None,
            PerPage=None,
            Order=None,
            UserID=None,
    ):

        try:
            url = "/UseHistory"
            url += "?SDate=" + SDate if SDate != None else ""
            url += "&EDate=" + EDate if EDate != None else ""
            url += "&Page=" + str(Page) if Page != None else ""
            url += "&PerPage=" + str(PerPage) if PerPage != None else ""
            url += "&Order=" + Order if Order != None else ""
            response = self._httpget(url, CorpNum, UserID)
            return response
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getPaymentHistory(
            self, CorpNum, SDate, EDate, Page=None, PerPage=None, UserID=None
    ):

        try:
            url = "/PaymentHistory"
            url += "?SDate=" + SDate if SDate != None else ""
            url += "&EDate=" + EDate if EDate != None else ""
            url += "&Page=" + str(Page) if Page != None else ""
            url += "&PerPage=" + str(PerPage) if PerPage != None else ""

            response = self._httpget(url, CorpNum, UserID)
            return response
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getRefundHistory(self, CorpNum, Page=None, PerPage=None, UserID=None):

        try:
            url = "/RefundHistory"
            url += "?Page=" + str(Page) if Page != None else ""
            url += "&PerPage=" + str(PerPage) if PerPage != None else ""

            response = self._httpget(url, CorpNum, UserID)
            return response
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def refund(self, CorpNum, RefundForm, UserID=None):

        try:
            postData = self._stringtify(RefundForm)
            response = self._httppost(
                "/Refund", postData, CorpNum=CorpNum, UserID=UserID
            )
            return response
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def paymentRequest(self, CorpNum, PaymentForm, UserID=None):

        try:
            postData = self._stringtify(PaymentForm)
            response = self._httppost(
                "/Payment", postData, CorpNum=CorpNum, UserID=UserID
            )
            return response
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getSettleResult(self, CorpNum, settleCode, UserID=None):

        if settleCode == None or settleCode == "":
            raise PopbillException(-99999999, "정산코드가 입력되지 않았습니다.")

        try:
            response = self._httpget(
                "/Payment/" + settleCode, CorpNum=CorpNum, UserID=UserID
            )
            return response
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def quitMember(self, CorpNum, QuitReason, UserID=None):

        try:
            reason = {"quitReason": QuitReason}

            postData = self._stringtify(reason)

            response = self._httppost(
                "/QuitRequest", postData, CorpNum=CorpNum, UserID=UserID
            )

            return response
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getRefundInfo(self, CorpNum, RefundCode, UserID=None):

        if RefundCode == None or RefundCode == "":
            raise PopbillException( -99999999, "환불코드가 입력되지 않았습니다.")

        try:
            response = self._httpget(
                "/Refund/" + RefundCode, CorpNum=CorpNum, UserID=UserID
            )

            return response

        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getRefundableBalance(self, CorpNum, UserID=None):
        try:
            return self._httpget("/RefundPoint", CorpNum=CorpNum, UserID=UserID).refundableBalance
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def _httpget(self, url, CorpNum=None, UserID=None):
        conn = self._getConn()

        headers = {"x-pb-version": APIVersion}

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token

        if UserID != None:
            headers["x-pb-userid"] = UserID

        headers["Accept-Encoding"] = "gzip,deflate"

        headers["User-Agent"] = "PYTHON POPBILL SDK"

        conn.request("GET", url, "", headers)

        response = conn.getresponse()
        responseString = response.read()

        if Utils.isGzip(response, responseString):
            responseString = Utils.gzipDecomp(responseString)

        if response.status != 200:
            err = Utils.json2obj(responseString)
            raise PopbillException(int(err.code), err.message)
        else:
            return Utils.json2obj(responseString)

    def _httppost(
            self,
            url,
            postData,
            CorpNum=None,
            UserID=None,
            ActionOverride=None,
            contentsType=None,
    ):
        conn = self._getConn()

        headers = {"x-pb-version": APIVersion}

        if contentsType != None:
            headers["Content-Type"] = contentsType
        else:
            headers["Content-Type"] = "application/json; charset=utf8"

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token
        if UserID != None:
            headers["x-pb-userid"] = UserID

        if ActionOverride != None:
            headers["X-HTTP-Method-Override"] = ActionOverride

        headers["Accept-Encoding"] = "gzip,deflate"

        headers["User-Agent"] = "PYTHON POPBILL SDK"

        conn.request("POST", url, postData, headers)

        response = conn.getresponse()
        responseString = response.read()

        if Utils.isGzip(response, responseString):
            responseString = Utils.gzipDecomp(responseString)

        if response.status != 200:
            err = Utils.json2obj(responseString)
            raise PopbillException(int(err.code), err.message)
        else:
            return Utils.json2obj(responseString)

    def _httpBulkPost(
            self,
            url,
            postData,
            SubmitID,
            CorpNum=None,
            UserID=None,
            ActionOverride=None,
    ):
        conn = self._getConn()

        headers = {"x-pb-version": APIVersion}

        headers["Content-Type"] = "application/json; charset=utf8"

        headers["x-pb-message-digest"] = base64.b64encode(
            sha1(postData).digest()
        ).decode("utf-8")
        headers["x-pb-submit-id"] = SubmitID

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token
        if UserID != None:
            headers["x-pb-userid"] = UserID

        if ActionOverride != None:
            headers["X-HTTP-Method-Override"] = ActionOverride

        headers["Accept-Encoding"] = "gzip,deflate"

        headers["User-Agent"] = "PYTHON POPBILL SDK"

        conn.request("POST", url, postData, headers)

        response = conn.getresponse()
        responseString = response.read()

        if Utils.isGzip(response, responseString):
            responseString = Utils.gzipDecomp(responseString)

        if response.status != 200:
            err = Utils.json2obj(responseString)
            raise PopbillException(int(err.code), err.message)
        else:
            return Utils.json2obj(responseString)

    def _httppost_files(self, url, postData, Files, CorpNum, UserID=None):
        conn = self._getConn()

        boundary = "--POPBILL_PYTHON--"

        headers = {
            "x-pb-version": APIVersion,
            "Content-Type": "multipart/form-data; boundary=%s" % boundary,
        }

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token

        if UserID != None:
            headers["x-pb-userid"] = UserID

        headers["Accept-Encoding"] = "gzip,deflate"

        headers["User-Agent"] = "PYTHON POPBILL SDK"

        # oraganize postData
        CRLF = "\r\n"

        buff = BytesIO()

        if postData != None and postData != "":
            buff.write((CRLF + "--" + boundary + CRLF).encode("utf-8"))
            buff.write(
                ('Content-Disposition: form-data; name="form"' + CRLF).encode("utf-8")
            )
            buff.write(CRLF.encode("utf-8"))
            buff.write(postData.encode("utf-8"))

        for f in Files:
            buff.write((CRLF + "--" + boundary + CRLF).encode("utf-8"))
            buff.write(
                (
                        'Content-Disposition: form-data; name="%s"; filename="%s"'
                        % (f.fieldName, f.fileName)
                        + CRLF
                ).encode("utf-8")
            )
            buff.write(
                ("Content-Type: Application/octet-stream" + CRLF).encode("utf-8")
            )
            buff.write(CRLF.encode("utf-8"))
            buff.write(f.fileData)

        buff.write((CRLF + "--" + boundary + "--" + CRLF + CRLF).encode("utf-8"))

        multiparted = buff.getvalue()

        conn.request("POST", url, multiparted, headers)

        response = conn.getresponse()
        responseString = response.read()

        if Utils.isGzip(response, responseString):
            responseString = Utils.gzipDecomp(responseString)

        if response.status != 200:
            err = Utils.json2obj(responseString)
            raise PopbillException(int(err.code), err.message)
        else:
            return Utils.json2obj(responseString)

    def _parse(self, jsonString):
        return Utils.json2obj(jsonString)

    def _stringtify(self, obj):
        return json.dumps(obj, cls=PopbillEncoder)


class JoinForm(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class ContactInfo(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class CorpInfo(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class BizCheckInfo(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class File(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class PopbillException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class JsonObject(object):
    def __init__(self, dic):
        try:
            d = dic.__dict__
        except AttributeError:
            d = dic._asdict()

        self.__dict__.update(d)

    def __getattr__(self, name):
        return None


class PaymentForm(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class RefundForm(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class UseHistory(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class Response(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class PopbillEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Utils:
    @staticmethod
    def _json_object_hook(d):
        return JsonObject(namedtuple("JsonObject", d.keys())(*d.values()))

    @staticmethod
    def json2obj(data):
        if type(data) is bytes:
            data = data.decode("utf-8")
        return json.loads(data, object_hook=Utils._json_object_hook)

    @staticmethod
    def isGzip(response, data):
        if response.getheader(
                "Content-Encoding"
        ) != None and "gzip" in response.getheader("Content-Encoding"):
            return True
        else:
            return False

    @staticmethod
    def gzipDecomp(data):
        return zlib.decompress(data, 16 + zlib.MAX_WBITS)
