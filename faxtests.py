# -*- coding: utf-8 -*-
# code for console Encoding difference. Dont' mind on it 
import sys
import imp
imp.reload(sys)
try: sys.setdefaultencoding('UTF8')
except Exception as E: pass

import unittest
from datetime import datetime
from popbill import *

class FaxServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.faxService =  FaxService('TESTER','yj1oEHdWJI0fMMsagD0JxBnYnbNRQuTD3MwxNwty2Tg=')
        self.faxService.IsTest = True
        self.testCorpNum = "1231212312"
        self.testUserID = "userid"

    def test_getURL(self):
        url = self.faxService.getURL(self.testCorpNum,self.testUserID,"SBOX")
        self.assertEqual(url[:5],"https","https로시작")

    def test_getUnitCost(self):
        unitCost = self.faxService.getUnitCost(self.testCorpNum)
        self.assertGreaterEqual(unitCost,0,"단가는 0 이상.")


    def test_sendFax(self):
        receivers = FaxReceiver(receiveNum="00011112222",receiveName="수신자명칭")
        filepath = "test.jpeg"

        receiptNum = self.faxService.sendFax(   
                                                self.testCorpNum,
                                                "070-7510-6766",
                                                receivers,
                                                filepath
                                            )

        self.assertIsNotNone(receiptNum,"접수번호 확인")

if __name__ == '__main__':
    unittest.main()