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

class FaxServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.faxService =  FaxService('TESTER','r1bp+HzSDrMkSS8921B8Dyrn83Y/yDcOnru2OBTT2Z8=')
        self.faxService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_01_getURL(self):
        url = self.faxService.getURL(self.testCorpNum,self.testUserID,"BOX")
        print(url)
        self.assertEqual(url[:5],"https","https로시작")

    def test_02_getUnitCost(self):
        unitCost = self.faxService.getUnitCost(self.testCorpNum)
        self.assertGreaterEqual(unitCost,0,"단가는 0 이상.")

    def test_03_sendFaxMulti(self):
        receivers = []

        filepath = ["test.jpeg", "test2.jpeg"]

        for x in range(0, 5):
            receivers.append(FaxReceiver(receiveNum="00011112222",receiveName="수신자명칭"))

        receiptNum = self.faxService.sendFax_multi(   
                                                self.testCorpNum,
                                                "070-7510-3710",
                                                receivers,
                                                filepath
                                            )
        self.assertIsNotNone(receiptNum,"접수번호 확인완료")

        result = self.faxService.getFaxResult(self.testCorpNum, receiptNum, self.testUserID)

        print(result[0].sendState)
        print(result[0].convState)
        print(result[0].sendResult)

    def test_04_reserveCancel(self):

        receivers = FaxReceiver(receiveNum="000111222",receiveName="수신자명")
        filepath = "test2.jpeg"

        reserveDT = '20150325200000'
        receiptNum = self.faxService.sendFax_multi(   
                                                self.testCorpNum,
                                                "070-7510-3711",
                                                receivers,
                                                filepath,
                                                reserveDT
                                            )
        self.assertIsNotNone(receiptNum,"접수번호 확인완료")
        print(receiptNum)

        try:
            result = self.faxService.cancelReserve(self.testCorpNum, "015032513303900002")
        except PopbillException as PE:
            print(PE.message)


    def test_05_sendFax(self):

        receiptNum = self.faxService.sendFax(self.testCorpNum, '07075103710', '070123','수신자명', 'test2.jpeg')

        self.assertIsNotNone(receiptNum," 접수번호 확인완료")
        
if __name__ == '__main__':
    unittest.main()