# -*- coding: utf-8 -*-
# Module for Popbill Base API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Kim Seongjun (pallet027@gmail.com)
# Written : 2015-01-21
# Contributor : Jeong Yohan (code@linkhub.co.kr)
# Updated : 2019-09-16
# Thanks for your interest.
from io import BytesIO
import json
import zlib
from time import time as stime
from json import JSONEncoder
from collections import namedtuple

try:
    import http.client as httpclient
except ImportError:
    import httplib as httpclient

import linkhub
from linkhub import LinkhubException

ServiceID_REAL = 'POPBILL'
ServiceID_TEST = 'POPBILL_TEST'
ServiceURL_REAL = 'popbill.linkhub.co.kr'
ServiceURL_TEST = 'popbill-test.linkhub.co.kr'
APIVersion = '1.0'


def __with_metaclass(meta, *bases):
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PopbillBase(__with_metaclass(Singleton, object)):
    IsTest = False
    IPRestrictOnOff = True

    def __init__(self, LinkID, SecretKey, timeOut=15):
        """ 생성자.
            args
                LinkID : 링크허브에서 발급받은 LinkID
                SecretKey : 링크허브에서 발급받은 SecretKey
        """
        self.__linkID = LinkID
        self.__secretKey = SecretKey
        self.__scopes = ["member"]
        self.__tokenCache = {}
        self.__conn = None
        self.__connectedAt = stime()
        self.__timeOut = timeOut

    def _getConn(self):
        if stime() - self.__connectedAt >= self.__timeOut or self.__conn == None:
            self.__conn = httpclient.HTTPSConnection(ServiceURL_TEST if self.IsTest else ServiceURL_REAL)
            self.__connectedAt = stime()
            return self.__conn
        else:
            return self.__conn

    def _addScope(self, newScope):
        self.__scopes.append(newScope)

    # 파트너 포인트 충전 팝업 URL 추가 - 2017/08/29
    def getPartnerURL(self, CorpNum, TOGO):
        """ 팝빌 회원 잔여포인트 확인
            args
                CorpNum : 팝빌회원 사업자번호
                TOGO : "CHRG"
            return
                URL
            raise
                PopbillException
        """
        try:
            return linkhub.getPartnerURL(self._getToken(CorpNum), TOGO)
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getBalance(self, CorpNum):
        """ 팝빌 회원 잔여포인트 확인
            args
                CorpNum : 확인하고자 하는 회원 사업자번호
            return
                잔여포인트 by float
            raise
                PopbillException
        """
        try:
            return linkhub.getBalance(self._getToken(CorpNum))
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getPartnerBalance(self, CorpNum):
        """ 팝빌 파트너 잔여포인트 확인
            args
                CorpNum : 확인하고자 하는 회원 사업자번호
            return
                잔여포인트 by float
            raise
                PopbillException
        """
        try:
            return linkhub.getPartnerBalance(self._getToken(CorpNum))
        except LinkhubException as LE:
            raise PopbillException(LE.code, LE.message)

    def getPopbillURL(self, CorpNum, UserID, ToGo):
        """ 팝빌 관련 URL을 확인.
            args
                CorpNum : 회원 사업자번호
                UserID  : 회원 팝빌아이디
                ToGo    : 관련 기능 지정 문자. ('CHRG' : 포인트 충전,'CERT' : 공인인증서등록 ,'LOGIN' : 팝빌메인)
            return
                30초 보안 토큰을 포함한 url
            raise
                PopbillException
        """
        if ToGo == None or ToGo == '':
            raise PopbillException(-99999999, "TOGO값이 입력되지 않았습니다.")

        result = self._httpget('/?TG=' + ToGo, CorpNum, UserID)
        return result.url

    def getAccessURL(self, CorpNum, UserID):
        """ 팝빌 로그인 URL
            args
                CorpNum : 회원 사업자번호
                UserID  : 회원 팝빌아이디
            return
                30초 보안 토큰을 포함한 url
            raise
                PopbillException
        """
        result = self._httpget('/?TG=LOGIN', CorpNum, UserID)
        return result.url

    def getChargeURL(self, CorpNum, UserID):
        """ 팝빌 연동회원 포인트 충전 URL
            args
                CorpNum : 회원 사업자번호
                UserID  : 회원 팝빌아이디
            return
                30초 보안 토큰을 포함한 url
            raise
                PopbillException
        """
        result = self._httpget('/?TG=CHRG', CorpNum, UserID)
        return result.url

    def checkIsMember(self, CorpNum):
        """ 회원가입여부 확인
            args
                CorpNum : 회원 사업자번호
            return
                회원가입여부 True/False
            raise
                PopbillException
        """
        if CorpNum == None or CorpNum == '':
            raise PopbillException(-99999999, "사업자번호가 입력되지 않았습니다.")

        return self._httpget('/Join?CorpNum=' + CorpNum + '&LID=' + self.__linkID, None, None)

    def joinMember(self, JoinInfo):
        """ 팝빌 회원가입
            args
                JoinInfo : 회원가입정보. Reference JoinForm class
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        JoinInfo.LinkID = self.__linkID
        postData = self._stringtify(JoinInfo)
        return self._httppost('/Join', postData)

    def checkID(self, checkID):
        """ 아이디 중복확인
            args
                checkID : 중복확인할 아이디
            return
                중복여부, consist of code and message
            raise
                PopbillException
        """
        if checkID == None or checkID == '':
            raise PopbillException(-99999999, "아이디가 입력되지 않았습니다.")

        return self._httpget('/IDCheck?ID=' + checkID)

    def listContact(self, CorpNum, UserID=None):
        """ 담당자 목록 확인
            args
                CorpNum : 회원 사업자번호
                UserID : 회원 아이디
            return
                담당자 목록 as list
            raise
                PopbillException
        """
        return self._httpget('/IDs', CorpNum, UserID)

    def updateContact(self, CorpNum, ContactInfo, UserID=None):
        """ 담당자 정보 수정
            args
                CorpNum : 회원 사업자번호
                ContactInfo : 담당자 정보, Reference ContactInfo class
                UserID :  회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        postData = self._stringtify(ContactInfo)
        return self._httppost('/IDs', postData, CorpNum, UserID)

    def getCorpInfo(self, CorpNum, UserID=None):
        """ 회사정보 확인
            args
                CorpNum : 회원 사업자번호
                UserID : 회원 아이디
            return
                회사정보
            raise
                PopbillException
        """
        return self._httpget('/CorpInfo', CorpNum, UserID)

    def updateCorpInfo(self, CorpNum, CorpInfo, UserID=None):
        """ 담당자 정보 수정
            args
                CorpNum : 회원 사업자번호
                CorpInfo : 회사 정보, Reference CorpInfo class
                UserID :  회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        postData = self._stringtify(CorpInfo)
        return self._httppost('/CorpInfo', postData, CorpNum, UserID)

    def registContact(self, CorpNum, ContactInfo, UserID=None):
        """ 담당자 추가
            args
                CorpNum : 회원 사업자번호
                ContactInfo : 담당자 정보, Reference ContactInfo class
                UserID :  회원 아이디
            return
                처리결과. consist of code and message
            raise
                PopbillException
        """
        postData = self._stringtify(ContactInfo)
        return self._httppost('/IDs/New', postData, CorpNum, UserID)

    def _getToken(self, CorpNum):

        try:
            token = self.__tokenCache[CorpNum]
        except KeyError:
            token = None

        refreshToken = True

        if token != None:
            refreshToken = token.expiration[:-5] < linkhub.getTime()

        if refreshToken:
            try:
                token = linkhub.generateToken(self.__linkID, self.__secretKey,
                                              ServiceID_TEST if self.IsTest else ServiceID_REAL, CorpNum, self.__scopes, None if self.IPRestrictOnOff else "*")

                try:
                    del self.__tokenCache[CorpNum]
                except KeyError:
                    pass

                self.__tokenCache[CorpNum] = token

            except LinkhubException as LE:
                raise PopbillException(LE.code, LE.message)

        return token

    def _httpget(self, url, CorpNum=None, UserID=None):

        conn = self._getConn()

        headers = {"x-pb-version": APIVersion}

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token

        if UserID != None:
            headers["x-pb-userid"] = UserID

        headers["Accept-Encoding"] = "gzip,deflate"

        conn.request('GET', url, '', headers)

        response = conn.getresponse()
        responseString = response.read()

        if Utils.isGzip(response, responseString):
            responseString = Utils.gzipDecomp(responseString)

        if response.status != 200:
            err = Utils.json2obj(responseString)
            raise PopbillException(int(err.code), err.message)
        else:
            return Utils.json2obj(responseString)

    def _httppost(self, url, postData, CorpNum=None, UserID=None, ActionOverride=None, contentsType=None):

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

        conn.request('POST', url, postData, headers)

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

        headers = {"x-pb-version": APIVersion, "Content-Type": "multipart/form-data; boundary=%s" % boundary}

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token

        if UserID != None:
            headers["x-pb-userid"] = UserID

        headers["Accept-Encoding"] = "gzip,deflate"

        # oraganize postData
        CRLF = '\r\n'

        buff = BytesIO()

        if postData != None and postData != '':
            buff.write((CRLF + '--' + boundary + CRLF).encode('utf-8'))
            buff.write(('Content-Disposition: form-data; name="form"' + CRLF).encode('utf-8'))
            buff.write(CRLF.encode('utf-8'))
            buff.write(postData.encode('utf-8'))

        for f in Files:
            buff.write((CRLF + '--' + boundary + CRLF).encode('utf-8'))
            buff.write(
                ('Content-Disposition: form-data; name="%s"; filename="%s"' % (f.fieldName, f.fileName) + CRLF).encode(
                    'utf-8'))
            buff.write(('Content-Type: Application/octet-stream' + CRLF).encode('utf-8'))
            buff.write(CRLF.encode('utf-8'))
            buff.write(f.fileData)

        buff.write((CRLF + '--' + boundary + '--' + CRLF + CRLF).encode('utf-8'))

        multiparted = buff.getvalue()

        conn.request('POST', url, multiparted, headers)

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


class PopbillEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Utils:
    @staticmethod
    def _json_object_hook(d):
        return JsonObject(namedtuple('JsonObject', d.keys())(*d.values()))

    @staticmethod
    def json2obj(data):
        if (type(data) is bytes): data = data.decode()
        return json.loads(data, object_hook=Utils._json_object_hook)

    @staticmethod
    def isGzip(response, data):
        if (response.getheader('Content-Encoding') != None and
                'gzip' in response.getheader('Content-Encoding')):
            return True
        else:
            return False

    @staticmethod
    def gzipDecomp(data):
        return zlib.decompress(data, 16 + zlib.MAX_WBITS)
