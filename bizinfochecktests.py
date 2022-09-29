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

class BizInfoCheckServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.BizInfoCheckService =  BizInfoCheckService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.BizInfoCheckService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"
        self.testMgtKey = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',10))

    def test_getChrgInfo(self):
        chrgInfo = self.BizInfoCheckService.getChargeInfo(self.testCorpNum, self.testUserID)
        print(chrgInfo.rateSystem)
        print(chrgInfo.chargeMethod)
        print(chrgInfo.unitCost)

    def test_getUnitCost(self):
        unitCost = self.BizInfoCheckService.getUnitCost(self.testCorpNum)
        print(unitCost)
        self.assertGreaterEqual(unitCost,0,"단가는 0 이상.")

    def test_getBalance(self):
        balance = self.BizInfoCheckService.getBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_getPartnerBalance(self):
        balance = self.BizInfoCheckService.getPartnerBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_checkIsMember(self):
        result = self.BizInfoCheckService.checkIsMember(self.testCorpNum)
        self.assertEqual(result.code,1,result.message + ", 가입시 코드는 1")

        result = self.BizInfoCheckService.checkIsMember("1234568790")
        self.assertEqual(result.code,0,result.message + ", 미가입시 코드는 0")

    def test_getPopbillURL(self):
        url = self.BizInfoCheckService.getPopbillURL(self.testCorpNum,self.testUserID,"LOGIN")
        print(url)
        self.assertEqual(url[:5], "https", "https로 시작")

    def test_checkBizInfo(self):
        result = self.BizInfoCheckService.checkBizInfo(self.testCorpNum, "6798700151","")

        tmp = "corpNum (사업자번호) : " + str(result.corpNum) + "\n"
        tmp += "companyRegNum (법인번호): " + str(result.companyRegNum) + "\n"
        tmp += "checkDT (확인일시) : " + result.checkDT + "\n"
        tmp += "corpName (상호): " + str(result.corpName) + "\n"
        tmp += "corpCode (기업형태코드): " + str(result.corpCode) + "\n"
        tmp += "corpScaleCode (기업규모코드): " + str(result.corpScaleCode) + "\n"
        tmp += "personCorpCode (개인법인코드): " + str(result.personCorpCode) + "\n"
        tmp += "headOfficeCode (본점지점코드) : " + str(result.headOfficeCode) + "\n"
        tmp += "industryCode (산업코드) : " + str(result.industryCode) + "\n"
        tmp += "establishCode (설립구분코드) : " + str(result.establishCode) + "\n"
        tmp += "establishDate (설립일자) : " + str(result.establishDate) + "\n"
        tmp += "CEOName (대표자명) : " + str(result.ceoname) + "\n"
        tmp += "workPlaceCode (사업장구분코드): " + str(result.workPlaceCode) + "\n"
        tmp += "addrCode (주소구분코드) : " + str(result.addrCode) + "\n"
        tmp += "zipCode (우편번호) : " + str(result.zipCode) + "\n"
        tmp += "addr (주소) : " + str(result.addr) + "\n"
        tmp += "addrDetail (상세주소) : " + str(result.addrDetail) + "\n"
        tmp += "enAddr (영문주소) : " + str(result.enAddr) + "\n"
        tmp += "bizClass (업종) : " + str(result.bizClass) + "\n"
        tmp += "bizType (업태) : " + str(result.bizType) + "\n"
        tmp += "result (결과코드) : " + str(result.result) + "\n"
        tmp += "resultMessage (결과메시지) : " + str(result.resultMessage) + "\n"
        tmp += "closeDownTaxType (사업자과세유형) : " + str(result.closeDownTaxType) + "\n"
        tmp += "closeDownTaxTypeDate (과세유형전환일자):" + str(result.closeDownTaxTypeDate) + "\n"
        tmp += "closeDownState (휴폐업상태) : " + str(result.closeDownState) + "\n"
        tmp += "closeDownStateDate (휴폐업일자) : " + str(result.closeDownStateDate) + "\n"

        print(tmp)

        self.assertEqual(result.corpNum, "6798700151","checkBizInfo 오류 :" + str(result.message))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BizInfoCheckServiceTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
