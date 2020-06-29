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

class AccountCheckServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.accountCheckService =  AccountCheckService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.accountCheckService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_getChrgInfo(self):
        try:
            chrgInfo = self.accountCheckService.getChargeInfo(self.testCorpNum, self.testUserID)
            print(chrgInfo.rateSystem)
            print(chrgInfo.chargeMethod)
            print(chrgInfo.unitCost)
        except Exception as e:
            print(e.code)
            print(e.message)

    def test_getUnitCost(self):
        try:
            unitCost = self.accountCheckService.getUnitCost(self.testCorpNum)
            print(unitCost)
        except Exception as e:
            print(e.code)
            print(e.message)

    def test_checkAccount(self):
        try:
            accountInfo = self.accountCheckService.checkAccountInfo(self.testCorpNum, "0081", "620199909856")
            print(accountInfo.resultCode)
            print(accountInfo.resultMessage)
            print(accountInfo.bankCode)
            print(accountInfo.accountNumber)
            print(accountInfo.accountName)
            print(accountInfo.checkDate)
        except Exception as e:
            print(e.code)
            print(e.message)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AccountCheckServiceTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
