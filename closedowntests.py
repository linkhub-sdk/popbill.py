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

class ClosedownServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.closedownService =  ClosedownService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.closedownService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"
        self.testMgtKey = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',10))

    def test_getChrgInfo(self):
        chrgInfo = self.closedownService.getChargeInfo(self.testCorpNum, self.testUserID)
        print(chrgInfo.rateSystem)
        print(chrgInfo.chargeMethod)
        print(chrgInfo.unitCost)

    def test_getUnitCost(self):
        unitCost = self.closedownService.getUnitCost(self.testCorpNum)
        print(unitCost)
        self.assertGreaterEqual(unitCost,0,"단가는 0 이상.")

    def test_getBalance(self):
        balance = self.closedownService.getBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_getPartnerBalance(self):
        balance = self.closedownService.getPartnerBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_checkIsMember(self):
        result = self.closedownService.checkIsMember(self.testCorpNum)
        self.assertEqual(result.code,1,result.message + ", 가입시 코드는 1")

        result = self.closedownService.checkIsMember("1234568790")
        self.assertEqual(result.code,0,result.message + ", 미가입시 코드는 0")

    def test_getPopbillURL(self):
        url = self.closedownService.getPopbillURL(self.testCorpNum,self.testUserID,"LOGIN")
        print(url)
        self.assertEqual(url[:5], "https", "https로 시작")

    def test_checkCorpNum(self):
        result = self.closedownService.checkCorpNum(self.testCorpNum, "401-03-94930")

        # state (휴폐업상태) : None-알수없음, 0-등록되지 않은 사업자번호, 1-사업중, 2-폐업, 3-휴업
        # type (사업 유형) : None-알수없음, 1-일반과세자, 2-면세과세자, 3-간이과세자, 4-비영리법인, 국가기관

        tmp = "corpNum : " + result.corpNum +"\n"
        tmp += "state : " + str(result.state)+ "\n"
        tmp += "type : " + str(result.type) + "\n"
        tmp += "stateDate(휴폐업일자) : " + str(result.stateDate) + "\n"
        tmp += "typeDate(전환일자) : " + str(result.typeDate) + "\n"
        tmp += "checkDate(국세청 확인일자) : " + str(result.checkDate) + "\n"

        print(tmp)

        self.assertEqual(result.corpNum, "4010394930","checkCorpNum 오류 :" + str(result.message))

    def test_checkCorpNums(self):
        resultList = self.closedownService.checkCorpNums(self.testCorpNum,["1234567890","4108600477","410-86-21884"])

        # state (휴폐업상태) : None-알수없음, 0-등록되지 않은 사업자번호, 1-사업중, 2-폐업, 3-휴업
        # type (사업 유형) : None-알수없음, 1-일반과세자, 2-면세과세자, 3-간이과세자, 4-비영리법인, 국가기관

        for info in resultList:
            print("corpNum : %s" % info.corpNum)
            for key, value in info.__dict__.items():
                if not key.startswith("__"):
                    print("     %s : %s" % (key,value))

        self.assertGreater(len(resultList),0,"갯수 확인")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ClosedownServiceTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
