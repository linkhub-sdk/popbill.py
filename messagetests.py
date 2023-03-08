# -*- coding: utf-8 -*-
# code for console Encoding difference. Dont' mind on it
import sys
import imp
import random

imp.reload(sys)
try:
    sys.setdefaultencoding('UTF8')
except Exception as E:
    pass

try:
    import unittest2 as unittest
except ImportError:
    import unittest
from datetime import datetime
from popbill import *


class MessageServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.messageService = MessageService('TESTER', 'SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
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

    def test_checkSenderNumber(self):
        try:
            SenderNumber = ""
            response = self.messageService.checkSenderNumber(self.testCorpNum, SenderNumber)
            print(response)
        except PopbillException as PE:
            print(PE.message)

    def test_getMessage(self):
        SDate = "20180901"
        EDate = "20181008"
        State = ['1', '2', '3', '4']
        Item = ['SMS', 'LMS', 'MMS']
        ReserveYN = '0'
        SenderYN = '0'
        Page = 1
        PerPage = 10
        Order = "D"
        QString = ""

        info = self.messageService.search(self.testCorpNum, SDate, EDate, State, Item, ReserveYN, SenderYN, Page,
                                          PerPage, Order, self.testUserID, QString)
        i = 1
        for info in info.list:
            print("====== 문자전송 정보 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

    def test_01_getBalance(self):
        balance = self.messageService.getBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance, 0, '잔액 0 이상.')

    def test_02_getPartnerBalance(self):
        balance = self.messageService.getPartnerBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance, 0, '잔액 0 이상.')

    def test_03_checkIsMember(self):
        result = self.messageService.checkIsMember(self.testCorpNum)
        self.assertEqual(result.code, 1, result.message + ", 가입시 코드 1")

        result = self.messageService.checkIsMember("1234568790")
        self.assertEqual(result.code, 0, result.message + ", 미가입시 코드 0")

    def test_04_getPopbillURL(self):

        url = self.messageService.getPopbillURL(self.testCorpNum, self.testUserID, "CHRG")
        self.assertEqual(url[:5], "https", "https로 시작")

    def test_05_getUnitCost(self):
        unitCost = self.messageService.getUnitCost(self.testCorpNum, "SMS")
        print(unitCost)
        self.assertGreaterEqual(unitCost, 0, "단가는 0 이상.")

    def test_06_sendSMS_one(self):
        try:
            receiptNum = self.messageService.sendSMS(self.testCorpNum, "", "", "수신자명", "단건전송 내용",
                                                     "20180912102154", "", "testkorea", "수신받는자명", "20180911102147")
            print("sendSMS_one : " + receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_07_sendSMS(self):
        reserveDT = ''
        messages = []
        messages.append(
            MessageReceiver(
                snd='',
                rcv='',
                rcvnm='수신자명',
                msg='문자 API TEST',
                interOPRefKey='20220729'+str(x)
            )
        )

        receiptNum = self.messageService.sendSMS_multi(self.testCorpNum, "", "동보전송 메시지 내용", messages,
                                                       reserveDT, "", "testkorea", "20180809140550")
        print(receiptNum)

    def test_08_sendSMS_Multi(self):
        reserveDT = ''
        messages = []

        for x in range(0, 5):
            messages.append(
                MessageReceiver(
                    snd='',
                    rcv='',
                    rcvnm='수신자명',
                    msg='문자 API TEST',
                    interOPRefKey='20220729'+str(x)
                )
            )

        receiptNum = self.messageService.sendSMS_multi(self.testCorpNum, "", "동보전송 메시지 내용", messages,
                                                       reserveDT, "", "testkorea", "20180809140617")
        print(receiptNum)

    def test_09__sendLMS_one(self):
        reserveDT = ''
        try:
            receiptNum = self.messageService.sendLMS(self.testCorpNum, "", "", "수신자명", "장문메시지 제목",
                                                     "장문 메시지 내용", reserveDT, False, "testkorea", "", "20180809140643")
            print("sendLMS_one : " + receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_10_sendLMS(self):
        Subject = '동보전송 제목'
        reserveDT = ''
        messages = []
        messages.append(
            MessageReceiver(
                snd='',
                rcv='',
                rcvnm='수신자명',
                msg='장문 문자 API TEST',
                sjt='장문 문자 제목',
                interOPRefKey='20220729'+str(x)
            )
        )
        receiptNum = self.messageService.sendLMS_multi(self.testCorpNum, "", "Subject", "동보전송 메시지 내용",
                                                       messages, reserveDT, "", "", "20180809140900")
        print(receiptNum)

    def test_11__sendXMS_one(self):

        reserveDT = ''

        try:
            receiptNum = self.messageService.sendXMS(self.testCorpNum, "", "", "수신자명", "메시지 제목",
                                                     "메시지 내용90Byte초과시 장문전송 메시지 내용90Byte초과시 장문전송 메시지 내용90Byte초과시 장문전송 메시지 내용90Byte초과시 장문전송",
                                                     reserveDT, True, "testkorea", "발신자명", "20180910103454")
            print("sendXMS_one : " + receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_12_sendXMSnResult(self):
        Subject = '동보전송 제목'
        reserveDT = ''
        messages = []
        messages.append(
            MessageReceiver(
                snd='',
                rcv='',
                rcvnm='수신자명',
                msg='장문 문자 API TEST',
                # sjt='장문 문자 제목',
                interOPRefKey='20220729'+str(x)
            )
        )

        receiptNum = self.messageService.sendXMS_multi(self.testCorpNum, "", Subject, "동보전송 메시지 내용",
                                                       messages, reserveDT, "", "testkorea", "20180809141010")
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
                snd='',
                rcv='',
                rcvnm='수신자명',
                msg='장문 문자 API TEST',
                sjt='장문 문자 제목',
                interOPRefKey='20220729'+str(x)
            )
        )

        try:
            receiptNum = self.messageService.sendXMS_multi(self.testCorpNum, "", Subject, "동보전송 메시지 내용",
                                                           messages, reserveDT)

            result = self.messageService.cancelReserve(self.testCorpNum, receiptNum)
            self.assertEqual(result.code, 1, result.message + ", 예약취소 실패")
        except PopbillException as PE:
            print(PE.message)

    def test_14_getURL(self):

        url = self.messageService.getURL(self.testCorpNum, self.testUserID, 'SENDER')
        self.assertEqual(url[:5], "https", "https로 시작")
        print("BOX URL : " + url)

    def test_15_sendMMS(self):
        Subject = "동보전송 제목"
        reserveDT = ''
        filepath = 'test2.jpeg'

        try:
            receiptNum = self.messageService.sendMMS(self.testCorpNum, "", "", "수신자명", Subject,
                                                     "동보전송 메시지 내용", filepath, reserveDT, True,
                                                     "testkorea", "수신받는자명", "20180809141117")
            print(receiptNum)

        except PopbillException as PE:
            print(PE.message)

    def test_16_sendMMS(self):

        filepath = 'test2.jpeg'

        messages = []
        reserveDT = ''

        messages.append(
            MessageReceiver(
                snd='',
                rcv='',
                rcvnm='수신자명',
                msg='멀티 문자 API TEST',
                sjt='멀티 문자 제목',
                interOPRefKey='20220729'+str(x)
            )
        )
        try:
            receiptNum = self.messageService.sendMMS_Multi(self.testCorpNum, "", '', '', messages, filepath,
                                                           reserveDT, True, "", "20180809141920")
            print(receiptNum)

        except PopbillException as PE:
            print(PE.message)

    def test_getSenderNumberList(self):
        numberList = self.messageService.getSenderNumberList(self.testCorpNum, self.testUserID)
        for senderObj in numberList:
            print(senderObj.number)
            print(senderObj.representYN)
            print(senderObj.state)

    def test_getStates(self):
        receiptNumList = []
        receiptNumList.append("018041717000000018")
        receiptNumList.append("018041717000000019")
        response = self.messageService.getStates(self.testCorpNum, receiptNumList, 'testkorea')
        print(len(response))

    def test_getMessagesRN(self):
        requestNum = "20180809141920"
        response = self.messageService.getMessagesRN(self.testCorpNum, requestNum)
        print(response[0].state)

    def test_cancelReserve(self):
        try:
            receiptNum = "0180910150000000"
            respone = self.messageService.cancelReserve(self.testCorpNum, receiptNum)
            print(respone)
        except PopbillException as PE:
            print(PE.message)


    def test_cancelReserveRN(self):
        try:
            requestNum = "20180809144427"
            respone = self.messageService.cancelReserveRN(self.testCorpNum, requestNum)
            print(respone)
        except PopbillException as PE:
            print(PE.message)

    def test_cancelReservebyRCV(self):
        try:
            receiptNum = "0180910150000000"
            receiveNum = "0102223333"
            respone = self.messageService.cancelReservebyRCV(self.testCorpNum, receiptNum, receiveNum)
            print(respone.code)
            print(respone.message)
        except PopbillException as PE:
            print(PE.code)
            print(PE.message)


    def test_cancelReserveRNbyRCV(self):
        try:
            requestNum = "20180809144427"
            receiveNum = "0102223333"
            respone = self.messageService.cancelReserveRNbyRCV(self.testCorpNum, requestNum, receiveNum)
            print(respone.code)
            print(respone.message)
        except PopbillException as PE:
            print(PE.code)
            print(PE.message)

    def test_getSenderNumberMgtURL(self):
        try:
            response = self.messageService.getSenderNumberMgtURL(self.testCorpNum, self.testUserID)
            print(response)
        except PopbillException as PE:
            print(PE.message)

    def test_getSentListURL(self):
        try:
            response = self.messageService.getSentListURL(self.testCorpNum, self.testUserID)
            print(response)
        except PopbillException as PE:
            print(PE.message)

    def test_checkAutoDenyNumberWithUserID(self):
        CorpNum = self.testCorpNum
        UserID = self.testUserID
        response = self.messageService.checkAutoDenyNumber(CorpNum, UserID)
        print(response)
        self.assertTrue(response != None)

    def test_checkAutoDenyNumber(self):
        CorpNum = self.testCorpNum
        response = self.messageService.checkAutoDenyNumber(CorpNum)
        print(response)
        self.assertTrue(response != None)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MessageServiceTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
