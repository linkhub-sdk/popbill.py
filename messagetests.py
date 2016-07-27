# -*- coding: utf-8 -*-
# code for console Encoding difference. Dont' mind on it
import sys
import imp
import random
imp.reload(sys)
try: sys.setdefaultencoding('UTF8')
except Exception as E: pass

try:
    import unittest2 as unittest
except ImportError:
    import unittest
from datetime import datetime
from popbill import *

class MessageServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.messageService = MessageService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.messageService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_getChargeInfo(self):
        chrgInfo = self.messageService.getChargeInfo(self.testCorpNum, "MMS", self.testUserID)
        print(chrgInfo.unitCost)
        print(chrgInfo.chargeMethod)
        print(chrgInfo.rateSystem)

    def test_getAutoDenyList(self):
        autoDenyList = self.messageService.getAutoDenyList(self.testCorpNum, self.testUserID)
        print(autoDenyList[5].number)

    def test_getMessage(self):
        SDate = "20160601"
        EDate = "20160831"
        State = ['1','2','3','4']
        Item = ['SMS', 'LMS', 'MMS']
        ReserveYN = '0'
        SenderYN = '0'
        Page = 1
        PerPage = 10
        Order = "D"

        info = self.messageService.search(self.testCorpNum, SDate, EDate, State, Item, ReserveYN, SenderYN, Page, PerPage, Order, self.testUserID)
        for i in range(1, 10):
            print(info.list[i].receiveNum +' '+info.list[i].tranNet)

    def test_01_getBalance(self):
        balance = self.messageService.getBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')


    def test_02_getPartnerBalance(self):
        balance = self.messageService.getPartnerBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_03_checkIsMember(self):
        result = self.messageService.checkIsMember(self.testCorpNum)
        self.assertEqual(result.code,1,result.message + ", 가입시 코드 1")

        result = self.messageService.checkIsMember("1234568790")
        self.assertEqual(result.code,0,result.message + ", 미가입시 코드 0")


    def test_04_getPopbillURL(self):

        url = self.messageService.getPopbillURL(self.testCorpNum,self.testUserID,"CHRG")
        self.assertEqual(url[:5], "https","https로 시작")

    def test_05_getUnitCost(self):
        unitCost = self.messageService.getUnitCost(self.testCorpNum, "SMS")
        print(unitCost)
        self.assertGreaterEqual(unitCost,0,"단가는 0 이상.")

    def test_06_sendSMS_one(self):
        try:
            receiptNum = self.messageService.sendSMS(self.testCorpNum, "07075103710", "010000000", "수신자명","단건전송 내용", "", True)
            print("sendSMS_one : " +receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_07_sendSMS(self):
        reserveDT = ''
        messages = []
        messages.append(
                        MessageReceiver(
                                        snd='07075103710',
                                        rcv='010000000',
                                        rcvnm='수신자명',
                                        msg='문자 API TEST'
                                       )
                        )


        receiptNum = self.messageService.sendSMS_multi(self.testCorpNum, "07075103710", "동보전송 메시지 내용", messages, reserveDT)
        print(receiptNum)

    def test_08_sendSMS_Multi(self):
        reserveDT = ''
        messages = []

        for x in range(0, 5):
            messages.append(
                        MessageReceiver(
                                        snd='07075103710',
                                        rcv='010000000',
                                        rcvnm='수신자명',
                                        msg='문자 API TEST'
                                       )
                        )




        receiptNum = self.messageService.sendSMS_multi(self.testCorpNum, "07075103710", "동보전송 메시지 내용", messages, reserveDT)
        print(receiptNum)



    def test_09__sendLMS_one(self):
        reserveDT = ''
        try:
                receiptNum = self.messageService.sendLMS(self.testCorpNum, "07075103710", "010000000", "수신자명", "장문메시지 제목", "장문 메시지 내용", reserveDT, False)
                print("sendLMS_one : "+ receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_10_sendLMS(self):
        Subject = '동보전송 제목'
        reserveDT = ''
        messages = []
        messages.append(
                        MessageReceiver(
                                        snd='07075103710',
                                        rcv='010000000',
                                        rcvnm='수신자명',
                                        msg='장문 문자 API TEST',
                                        sjt='장문 문자 제목'
                                       )
                        )
        receiptNum = self.messageService.sendLMS_multi(self.testCorpNum, "07075103710", "Subject", "동보전송 메시지 내용", messages, reserveDT)
        print(receiptNum)

    def test_11__sendXMS_one(self):

        reserveDT = ''

        try:
                receiptNum = self.messageService.sendXMS(self.testCorpNum, "07075103710", "010000000", "수신자명", "메시지 제목",
                 "메시지 내용90Byte초과시 장문전송 메시지 내용90Byte초과시 장문전송 메시지 내용90Byte초과시 장문전송 메시지 내용90Byte초과시 장문전송", reserveDT, True)
                print("sendXMS_one : "+ receiptNum)
        except PopbillException as PE:
            print(PE.message)


    def test_12_sendXMSnResult(self):
        Subject = '동보전송 제목'
        reserveDT = ''
        messages = []
        messages.append(
                        MessageReceiver(
                                        snd='07075103710',
                                        rcv='010000000',
                                        rcvnm='수신자명',
                                        msg='장문 문자 API TEST'
                                        #sjt='장문 문자 제목'
                                       )
                        )

        receiptNum = self.messageService.sendXMS_multi(self.testCorpNum, "07075103710", Subject, "동보전송 메시지 내용", messages, reserveDT)
        print(receiptNum)

        result = self.messageService.getMessages(self.testCorpNum, receiptNum)
        print(result[0].receiveName)
        print(result[0].content)

    def test_13_reserveSendnCancel(self):

        Subject = '동보전송 제목'
        reserveDT = '20150325200000'

        messages = []

        messages.append(
                        MessageReceiver(
                                        snd='07075103710',
                                        rcv='010000000',
                                        rcvnm='수신자명',
                                        msg='장문 문자 API TEST',
                                        sjt='장문 문자 제목'
                                       )
                        )

        try:
            receiptNum = self.messageService.sendXMS_multi(self.testCorpNum, "07075103710", Subject, "동보전송 메시지 내용", messages, reserveDT)

            result = self.messageService.cancelReserve(self.testCorpNum, receiptNum)
            self.assertEqual(result.code,1,result.message + ", 예약취소 실패")
        except PopbillException as PE:
            print(PE.message)




    def test_14_getURL(self):

        url = self.messageService.getURL(self.testCorpNum, self.testUserID, 'BOX')
        self.assertEqual(url[:5], "https","https로 시작")
        print("BOX URL : " +url)

    def test_15_sendMMS(self):
        Subject = "동보전송 제목"
        reserveDT = ''
        filepath = 'test2.jpeg'

        try:
            receiptNum = self.messageService.sendMMS(self.testCorpNum, "07075103710","010000000","수신자명", Subject, "동보전송 메시지 내용", filepath, reserveDT, True)
            print(receiptNum)

        except PopbillException as PE:
            print(PE.message)

    def test_16_sendMMS(self):

        filepath = 'test2.jpeg'

        messages = []
        reserveDT = ''

        messages.append(
                        MessageReceiver(
                                        snd='07075103710',
                                        rcv='010000000',
                                        rcvnm='수신자명',
                                        msg='멀티 문자 API TEST',
                                        sjt='멀티 문자 제목'
                                       )
                        )
        try:
            receiptNum = self.messageService.sendMMS_Multi(self.testCorpNum, "07075103710",'', '', messages, filepath, reserveDT, True)
            print(receiptNum)

        except PopbillException as PE:
            print(PE.message)

if __name__ == '__main__':
    unittest.main()
