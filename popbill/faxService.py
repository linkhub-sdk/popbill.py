# -*- coding: utf-8 -*-
# Module for Popbill FAX API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Kim Seongjun (pallet027@gmail.com)
# Written : 2015-01-21
# Thanks for your interest. 
from datetime import datetime
from .base import PopbillBase,PopbillException,File


class FaxService(PopbillBase):
    def __init__(self,LinkID,SecretKey):
        super(self.__class__,self).__init__(LinkID,SecretKey)
        self._addScope("160")
        
    def getURL(self,CorpNum,UserID , ToGo):
        result = self._httpget('/FAX/?TG=' + ToGo , CorpNum,UserID)
        return result.url

    def getUnitCost(self,CorpNum):
        result = self._httpget('/FAX/UnitCost' , CorpNum)
        return int(result.unitCost)

    def sendFax(self,CorpNum,SenderNum, Receiver, FilePath, ReserveDT = None , UserID = None):
        if SenderNum == None or SenderNum == "" :
            raise PopbillException(-99999999,"발신자 번호가 입력되지 않았습니다.")
        if Receiver == None:
            raise PopbillException(-99999999,"수신자 정보가 입력되지 않았습니다.")
        if not (type(Receiver) is str or type(Receiver) is FaxReceiver or type(Receiver) is list) :
            raise PopbillException(-99999999,"'Receiver' argument type error. 'FaxReceiver' or List of 'FaxReceiver'.")
        if FilePath == None :
            raise PopbillException(-99999999,"발신 파일경로가 입력되지 않았습니다.")
        if not (type(FilePath) is str or type(FilePath) is list) :
            raise PopbillException(-99999999,"발신 파일은 파일경로 또는 경로목록만 입력 가능합니다.")
        if type(FilePath) is list and (len(FilePath) < 1 or len(FilePath) > 5) :
            raise PopbillException(-99999999,"파일은 1개 이상, 5개 까지 전송 가능합니다.")

        req = {"snd" : SenderNum , "fCnt": 1 if type(FilePath) is str else len(FilePath) , "rcvs" : [] , "sndDT" : None}

        if(type(Receiver) is str):        
            Receiver = FaxReceiver(receiveNum=Receiver)
            
        if(type(Receiver) is FaxReceiver):
            Receiver = [Receiver]

        for r in Receiver:
            req['rcvs'].append({"rcv" : r.receiveNum, "rcvnm" : r.receiveName})

        if ReserveDT != None :
            req['sndDT'] = ReserveDT

        postData = self._stringtify(req)

        if(type(FilePath) is str):
            FilePath = [FilePath]
        
        files = []

        for filePath in FilePath:
            with open(filePath,"rb") as f:
                files.append(File(fieldName='file',
                              fileName=f.name,
                              fileData=f.read())
                            )
                
        result = self._httppost_files('/FAX',postData,files,CorpNum,UserID)

        return result.receiptNum


class FaxReceiver(object):
    def __init__(self,**kwargs):
        self.__dict__ = dict.fromkeys(['receiveNum','receiveName'])
        self.__dict__.update(kwargs)