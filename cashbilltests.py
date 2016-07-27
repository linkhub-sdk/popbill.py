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
from popbill import *

class CashbillServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cashbillService =  CashbillService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.cashbillService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"
        self.testMgtKey = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',10))

    def test_getChargeInfo(self):
        chrgInfo = self.cashbillService.getChargeInfo(self.testCorpNum, self.testUserID)
        print(chrgInfo.unitCost)
        print(chrgInfo.rateSystem)
        print(chrgInfo.chargeMethod)

    def test_search(self):
        DType = "R"
        SDate = "20160601"
        EDate = "20160831"
        State = ["3**"]
        TradeType = ["N", "C"]
        TradeUsage = ["P", "C"]
        TaxationType = ["T", "N"]
        Page = 1
        PerPage = 10
        Order = "D"

        try:
            result = self.cashbillService.search(self.testCorpNum,DType,SDate,EDate,State,TradeType,TradeUsage,TaxationType,Page,PerPage,Order,self.testUserID)
            print(result.total)
            self.assertEqual(result.code, 1, "등록 오류 : " + result.message)
        except PopbillException as PE:
            print(PE.message)
    def test_registIssue(self):

        cashbill = Cashbill(mgtKey = "20160726-02",
                            tradeType = "승인거래",
                            tradeUsage = "소득공제용",
                            taxationType = "과세",
                            identityNum = "01012341234",
                            franchiseCorpNum = "1234567890",
                            franchiseCorpName = "발행자 상호",
                            franchiseCEOName = "발행 대표자 성명",
                            franchiseAddr = "발행자 주소",
                            franchiseTEL = "07075103710",
                            smssendYN = False,
                            customerName = "고객명",
                            itemName = "상품명",
                            orderNumber = "주문번호",
                            email = "test@test.com",
                            hp = "010000000",
                            fax = "07075103710",
                            supplyCost = "15000",
                            tax = "5000",
                            serviceFee = "0",
                            totalAmount = "20000"
                            )
        try:
            result = self.cashbillService.registIssue(self.testCorpNum,cashbill,"발행메모")
            self.assertEqual(result.code, 1, "등록 오류 : " + result.message)
        except PopbillException as PE:
            print(PE.message)

    def test_getInfos(self):
        infos = self.cashbillService.getInfos(self.testCorpNum,["20150707-01","20150706-01"])
        for info in infos:
            print("info : %s" % info.mgtKey)
            for key, value in info.__dict__.items():
                if not key.startswith("__"):
                    print("     %s : %s" % (key,value))
        self.assertGreater(len(infos),0,"갯수 확인")

    def test_getBalance(self):
        balance = self.cashbillService.getBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_getPartnerBalance(self):
        balance = self.cashbillService.getPartnerBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_checkIsMember(self):
        result = self.cashbillService.checkIsMember(self.testCorpNum)
        self.assertEqual(result.code,1,result.message + ", 가입시 코드는 1")

        result = self.cashbillService.checkIsMember("1234568790")
        self.assertEqual(result.code,0,result.message + ", 미가입시 코드는 0")

    def test_getURL(self):
        url = self.cashbillService.getURL(self.testCorpNum,self.testUserID,"PBOX")
        self.assertEqual(url[:5], "https","https로 시작")
        print("PBOX url : " + url)

    def test_getUnitCost(self):
        unitCost = self.cashbillService.getUnitCost(self.testCorpNum)
        self.assertGreaterEqual(unitCost,0,"단가는 0 이상.")

    def test_02_checkMgtKeyInUse(self):
        bIsInUse = self.cashbillService.checkMgtKeyInUse(self.testCorpNum,"20150325-01")
        self.assertEqual(bIsInUse,True, "등록으로 확인")

        bIsInUse = self.cashbillService.checkMgtKeyInUse(self.testCorpNum,"20150325-535")
        self.assertEqual(bIsInUse,False, "미등록으로 확인")

    def test_getPopbillURL(self):
        url = self.cashbillService.getPopbillURL(self.testCorpNum,self.testUserID,"LOGIN")
        self.assertEqual(url[:5], "https", "https로 시작")

    def test_01_register(self):

        cashbill = Cashbill(mgtKey = "20150325-01",
                            tradeType = "승인거래",
                            tradeUsage = "소득공제용",
                            taxationType = "과세",
                            identityNum = "010000000",
                            franchiseCorpNum = "1234567890",
                            franchiseCorpName = "발행자 상호",
                            franchiseCEOName = "발행 대표자 성명",
                            franchiseAddr = "발행자 주소",
                            franchiseTEL = "07075103710",
                            smssendYN = False,
                            customerName = "고객명",
                            itemName = "상품명",
                            orderNumber = "주문번호",
                            email = "test@test.com",
                            hp = "010000000",
                            fax = "07075103710",
                            supplyCost = "15000",
                            tax = "5000",
                            serviceFee = "0",
                            totalAmount = "20000"
                            )
        try:
            result = self.cashbillService.register(self.testCorpNum,cashbill)
            self.assertEqual(result.code, 1, "등록 오류 : " + result.message)
        except PopbillException as PE:
            print(PE.message)

    def test_02_update(self):
        cashbill = Cashbill(mgtKey = "20150325-01",
                            tradeType = "승인거래",
                            tradeUsage = "소득공제용",
                            taxationType = "과세",
                            identityNum = "01012341234",
                            franchiseCorpNum = "1234567890",
                            franchiseCorpName = "발행자 상호",
                            franchiseCEOName = "발행 대표자 성명",
                            franchiseAddr = "발행자 주소",
                            franchiseTEL = "07075103710",
                            smssendYN = False,
                            customerName = "고객명",
                            itemName = "상품명",
                            orderNumber = "주문번호",
                            email = "test@test.com",
                            hp = "010000000",
                            fax = "07075103710",
                            supplyCost = "15000",
                            tax = "5000",
                            serviceFee = "0",
                            totalAmount = "20000"
                            )

        try:
            result = self.cashbillService.update(self.testCorpNum, '20150325-01', cashbill)
            self.assertEqual(result.code, 1, "수정 오류 : " + result.message)
            print(result.message)
        except PopbillException as PE:
            print(PE.message)

    def test_03_issue(self):
        try:
            result = self.cashbillService.issue(self.testCorpNum, '20150325-01', "발행메모")
            self.assertEqual(result.code, 1, "발행 오류 : " + result.message)
            print(result.message)
        except PopbillException as PE:
            print(PE.message)

    def test_04_cancelIssue(self):
        result = self.cashbillService.cancelIssue(self.testCorpNum, "20150325-01", "발행취소 메모1")
        self.assertEqual(result.code, 1, "발행취소 오류 : "+result.message)

    def test_05_getInfo(self):
            result = self.cashbillService.getInfo(self.testCorpNum, "20150325-01")
            print(result.itemKey)
            self.assertEqual(result.mgtKey, "20150325-01","getInfo 오류 :" + str(result.message))

    def test_06_getDetailInfo(self):
            result = self.cashbillService.getDetailInfo(self.testCorpNum, "20150325-01")
            print(result.smssendYN)
            self.assertEqual(result.mgtKey, "20150325-01", "getDetail오류 :" + str(result.message))

    def test_07_sendEmail(self):

            result = self.cashbillService.sendEmail(self.testCorpNum, "20150325-01", "test@test.com")
            self.assertEqual(result.code,1, "이메일 재전송 오류 : "+result.message)


    def test_08_sendSMS(self):

        result = self.cashbillService.sendSMS(self.testCorpNum, "20150325-01", "07075103710","010111222","문자메시지 테스트")
        self.assertEqual(result.code,1, "알림문자 전송 오류 : "+result.message)


    def test_09_sendFax(self):
        result = self.cashbillService.sendFAX(self.testCorpNum, "20150325-01", "07075103710","010111222")
        self.assertEqual(result.code,1, "알림문자 전송 오류 : "+result.message)

    def test_10_getLogs(self):
        result = self.cashbillService.getLogs(self.testCorpNum, "20150325-01")
        print(result[0].log)

    def test_12_getPopUpURL(self):
        url = self.cashbillService.getPopUpURL(self.testCorpNum, "20150325-01", self.testUserID)
        self.assertEqual(url[:5], "https", "https로 시작 ")
        print("PopupURL : " + url)

    def test_13_getPrintURL(self):
        url = self.cashbillService.getPrintURL(self.testCorpNum, "20150325-01", self.testUserID)
        self.assertEqual(url[:5], "https", "https로 시작 ")
        print("Print URL : " + url)

    def test_14_getEPrintURL(self):
        url = self.cashbillService.getEPrintURL(self.testCorpNum, "20150325-01", self.testUserID)
        self.assertEqual(url[:5], "https", "https로 시작 ")
        print("EPRINT url : " + url)

    def test_15_getMailURL(self):
        url = self.cashbillService.getMailURL(self.testCorpNum, "20150325-01", self.testUserID)
        self.assertEqual(url[:5], "https", "https로 시작 ")
        print("mailURL : " + url)

    def test_16_getMassPrintURL(self):
        MgtKeyList = ["20150225-02", "20150320-01", "20150320-03"]
        url = self.cashbillService.getMassPrintURL(self.testCorpNum, MgtKeyList, self.testUserID)
        self.assertEqual(url[:5], "https", "https로 시작 ")
        print("PopupURL : " + url)

    def test_99_delete(self):
        result = self.cashbillService.delete(self.testCorpNum, "20150325-01")
        self.assertEqual(result.code,1, "삭제 오류 : "+result.message)


if __name__ == '__main__':
    unittest.main()
