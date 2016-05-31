# -*- coding: utf-8 -*-
# Module for Popbill Base API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Kim Seongjun (pallet027@gmail.com)
# Written : 2015-01-21
# Updated : 2016-05-31
# Thanks for your interest.
from io import BytesIO
import datetime
import json
from time import time as stime
from json import JSONEncoder
from collections import namedtuple
try:
    import http.client as httpclient
except ImportError:
    import httplib as httpclient
import mimetypes

import linkhub
from linkhub import LinkhubException

ServiceID_REAL = 'POPBILL';
ServiceID_TEST = 'POPBILL_TEST';
ServiceURL_REAL = 'popbill.linkhub.co.kr';
ServiceURL_TEST = 'popbill_test.linkhub.co.kr';
APIVersion = '1.0';

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

class PopbillBase(__with_metaclass(Singleton,object)):
    IsTest = False

    def __init__(self,LinkID,SecretKey,timeOut = 60):
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


    def _getConn(self,ForceReconnect=False):
        if ForceReconnect or self.__conn == None or stime() - self.__connectedAt >= self.__timeOut:
            self.__conn = httpclient.HTTPSConnection(ServiceURL_TEST if self.IsTest else ServiceURL_REAL);
            self.__connectedAt = stime()
            return self.__conn
        else:
            return self.__conn

    def _addScope(self,newScope):
        self.__scopes.append(newScope)

    def getBalance(self,CorpNum):
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
                raise PopbillException(LE.code,LE.message)

    def getPartnerBalance(self,CorpNum):
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
                raise PopbillException(LE.code,LE.message)

    def getPopbillURL(self,CorpNum,UserID,ToGo):
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
        result = self._httpget('/?TG=' + ToGo , CorpNum,UserID)
        return result.url

    def checkIsMember(self,CorpNum):
        """ 회원가입여부 확인
            args
                CorpNum : 회원 사업자번호
            return
                회원가입여부 True/False
            raise
                PopbillException
        """
        return self._httpget('/Join?CorpNum=' + CorpNum + '&LID=' + self.__linkID,None,None)

    def joinMember(self,JoinInfo):
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
        return self._httppost('/Join',postData)

    def _getToken(self,CorpNum):

        try:
            token = self.__tokenCache[CorpNum]
        except KeyError :
            token = None

        refreshToken = True

        if token != None :
            refreshToken = token.expiration[:-5] < linkhub.getTime()

        if refreshToken :
            try:
                token = linkhub.generateToken(self.__linkID,self.__secretKey,ServiceID_TEST if self.IsTest else ServiceID_REAL ,CorpNum,self.__scopes)

                try:
                    del self.__tokenCache[CorpNum]
                except KeyError:
                    pass

                self.__tokenCache[CorpNum] = token

            except LinkhubException as LE:
                raise PopbillException(LE.code,LE.message)

        return token

    def _httpget(self,url,CorpNum = None,UserID = None):

        headers = {"x-pb-version" : APIVersion}

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token

        if UserID != None:
            headers["x-pb-userid"] = UserID

        # SEH 의 EXCEPTION_EXECUTE_HANDLER 를 모방해서, 한번의 실패에 한해 강제 재연결을 수행한다.
        # 그 후에 발생하는 에러에 대해서는 그냥 예외처리한다.
        for i in range(2):
            try:
                conn = self._getConn()
                conn.request('GET', url, '', headers)

                response = conn.getresponse()
                responseString = response.read()
                break
            except httpclient.HTTPException:
                if i == 0:
                    # 처음 예외가 발생했을 경우는 재연결을 시도한다.
                    try:
                        self._getConn(ForceReconnect=True)
                        continue
                    except Exception:
                        # 재연결에서 어떤 에러가 발생한다면?
                        # 처리할 수 없는 상황, 아마도 서버에의 초기 연결이 실패한경우
                        raise PopbillException(int(-99999999), 'UNEXPECTED EXCEPTION')
                else:
                    # 이미 한번 예외 처리를 했음에도 불구하고 에러가 난 경우.
                    raise PopbillException(int(-99999999), 'UNEXPECTED EXCEPTION')

        if response.status != 200 :
            err = Utils.json2obj(responseString)
            raise PopbillException(int(err.code),err.message)
        else:
            return Utils.json2obj(responseString)

    def _httppost(self,url,postData, CorpNum = None,UserID = None,ActionOverride = None ):

        headers = {"x-pb-version" : APIVersion, "Content-Type" : "Application/json"}

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token

        if UserID != None:
            headers["x-pb-userid"] = UserID

        if ActionOverride != None:
            headers["X-HTTP-Method-Override"] = ActionOverride

        # SEH 의 EXCEPTION_EXECUTE_HANDLER 를 모방해서, 한번의 실패에 한해 강제 재연결을 수행한다.
        # 그 후에 발생하는 에러에 대해서는 그냥 예외처리한다.
        for i in range(2):
            try:
                conn = self._getConn()
                conn.request('POST', url, postData, headers)

                response = conn.getresponse()
                responseString = response.read()
                break
            except httpclient.HTTPException:
                if i == 0:
                    # 처음 예외가 발생했을 경우는 재연결을 시도한다.
                    try:
                        self._getConn(ForceReconnect=True)
                        continue
                    except Exception:
                        # 재연결에서 어떤 에러가 발생한다면?
                        # 처리할 수 없는 상황, 아마도 서버에의 초기 연결이 실패한경우
                        raise PopbillException(int(-99999999), 'UNEXPECTED EXCEPTION')
                else:
                    # 이미 한번 예외 처리를 했음에도 불구하고 에러가 난 경우.
                    raise PopbillException(int(-99999999), 'UNEXPECTED EXCEPTION')

        if response.status != 200 :
            err = Utils.json2obj(responseString)
            raise PopbillException(int(err.code),err.message)
        else:
            return Utils.json2obj(responseString)

    def _httppost_files(self,url,postData,Files,CorpNum,UserID = None):

        boundary = "--POPBILL_PYTHON--"

        headers = {"x-pb-version" : APIVersion, "Content-Type" : "multipart/form-data; boundary=%s" % boundary}

        if CorpNum != None:
            headers["Authorization"] = "Bearer " + self._getToken(CorpNum).session_token

        if UserID != None:
            headers["x-pb-userid"] = UserID


        #oraganize postData
        CRLF = '\r\n'

        buff = BytesIO()

        if postData != None and postData != '':
            buff.write((CRLF + '--' + boundary + CRLF).encode('utf-8'))
            buff.write(('Content-Disposition: form-data; name="form"' + CRLF).encode('utf-8'))
            buff.write(CRLF.encode('utf-8'))
            buff.write(postData.encode('utf-8'))

        for f in Files:
            buff.write(( CRLF + '--' + boundary + CRLF).encode('utf-8'))
            buff.write(('Content-Disposition: form-data; name="%s"; filename="%s"' % (f.fieldName, f.fileName) + CRLF).encode('utf-8'))
            buff.write(('Content-Type: Application/octet-stream' + CRLF).encode('utf-8'))
            buff.write(CRLF.encode('utf-8'))
            buff.write(f.fileData)

        buff.write(( CRLF + '--' + boundary + '--' + CRLF + CRLF).encode('utf-8'))

        multiparted = buff.getvalue()

        # SEH 의 EXCEPTION_EXECUTE_HANDLER 를 모방해서, 한번의 실패에 한해 강제 재연결을 수행한다.
        # 그 후에 발생하는 에러에 대해서는 그냥 예외처리한다.
        for i in range(2):
            try:
                conn = self._getConn()
                conn.request('POST', url, multiparted, headers)

                response = conn.getresponse()
                responseString = response.read()
                break
            except httpclient.HTTPException:
                if i == 0:
                    # 처음 예외가 발생했을 경우는 재연결을 시도한다.
                    try:
                        self._getConn(ForceReconnect=True)
                        continue
                    except Exception:
                        # 재연결에서 어떤 에러가 발생한다면?
                        # 처리할 수 없는 상황, 아마도 서버에의 초기 연결이 실패한경우
                        raise PopbillException(int(-99999999), 'UNEXPECTED EXCEPTION')
                else:
                    # 이미 한번 예외 처리를 했음에도 불구하고 에러가 난 경우.
                    raise PopbillException(int(-99999999), 'UNEXPECTED EXCEPTION')

        if response.status != 200 :
            err = Utils.json2obj(responseString)
            raise PopbillException(int(err.code),err.message)
        else:
            return Utils.json2obj(responseString)

    def _parse(self,jsonString):
        return Utils.json2obj(jsonString);

    def _stringtify(self,obj):
        return json.dumps(obj,cls=PopbillEncoder)


class JoinForm(object):
    def __init__(self,**kwargs):
        self.__dict__ = kwargs

class File(object):
    def __init__(self,**kwargs):
        self.__dict__ = kwargs


class PopbillException(Exception):
    def __init__(self,code,message):
        self.code = code
        self.message = message

class JsonObject(object):
    def __init__(self,dic):
        try:
            d = dic.__dict__
        except AttributeError :
            d = dic._asdict()

        self.__dict__.update(d)

    def __getattr__(self,name):
        return None


class PopbillEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Utils:
    @staticmethod
    def _json_object_hook(d): return JsonObject(namedtuple('JsonObject', d.keys())(*d.values()))

    @staticmethod
    def json2obj(data):
        if(type(data) is bytes): data = data.decode()
        return json.loads(data, object_hook=Utils._json_object_hook)
