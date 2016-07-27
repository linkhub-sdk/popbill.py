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

class HTCashbillServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.htCashbillService =  HTCashbillService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.htCashbillService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_getChrgInfo(self):
        chrgInfo = self.htCashbillService.getChargeInfo(self.testCorpNum, self.testUserID)
        print(chrgInfo.rateSystem)
        print(chrgInfo.chargeMethod)
        print(chrgInfo.unitCost)

    def test_requestJob(self):
        Type = "SELL"
        SDate = "20160601"
        EDate = "20160831"
        jobID = self.htCashbillService.requestJob(self.testCorpNum, Type, SDate, EDate, self.testUserID)
        print (jobID)

    def test_getJobState(self):
        JobID = "016072716000000002"

        state = self.htCashbillService.getJobState(self.testCorpNum, JobID, self.testUserID)

        tmp = '======== getJobState Response ========\n'
        tmp += 'jobID : ' + state.jobID + '\n'
        tmp += 'jobState : ' + str(state.jobState) + '\n'
        tmp += 'queryType : ' + state.queryType + '\n'
        tmp += 'queryDateType : ' + state.queryDateType + '\n'
        tmp += 'queryStDate : ' + state.queryStDate + '\n'
        tmp += 'queryEnDate : ' + state.queryEnDate + '\n'
        tmp += 'errorCode : ' + str(state.errorCode) + '\n'
        tmp += 'errorReason : ' + state.errorReason + '\n'
        tmp += 'jobStartDT : ' + state.jobStartDT + '\n'
        tmp += 'jobEndDT : ' + state.jobEndDT + '\n'
        tmp += 'collectCount : ' + str(state.collectCount) + '\n'
        tmp += 'regDT : ' + state.regDT + '\n'
        print(tmp)

    def test_listACtiveJob(self):
        jobInfos = self.htCashbillService.listActiveJob(self.testCorpNum, self.testUserID)

        state = jobInfos[0]

        tmp = '======== listACtiveJob Response ========\n'
        tmp += 'jobID : ' + state.jobID + '\n'
        tmp += 'jobState : ' + str(state.jobState) + '\n'
        tmp += 'queryType : ' + state.queryType + '\n'
        tmp += 'queryDateType : ' + state.queryDateType + '\n'
        tmp += 'queryStDate : ' + state.queryStDate + '\n'
        tmp += 'queryEnDate : ' + state.queryEnDate + '\n'
        tmp += 'errorCode : ' + str(state.errorCode) + '\n'
        tmp += 'errorReason : ' + state.errorReason + '\n'
        tmp += 'jobStartDT : ' + state.jobStartDT + '\n'
        tmp += 'jobEndDT : ' + state.jobEndDT + '\n'
        tmp += 'collectCount : ' + str(state.collectCount) + '\n'
        tmp += 'regDT : ' + state.regDT + '\n'
        print(tmp)

    def test_search(self):
        JobID = "016072716000000002"
        TradeType = ["N", "C"]
        TradeUsage = ["P", "C"]
        Page = 1
        PerPage = 10
        Order = "D"

        searchInfo = self.htCashbillService.search(self.testCorpNum, JobID, TradeType, TradeUsage, Page, PerPage, Order, self.testUserID)

        print(searchInfo.total)
        print(searchInfo.list[0].ntsconfirmNum)

    def test_summary(self):
        JobID = "016072716000000002"
        TradeType = ["N", "C"]
        TradeUsage = ["P", "C"]
        Page = 1
        PerPage = 10
        Order = "D"

        summaryInfo = self.htCashbillService.summary(self.testCorpNum, JobID, TradeType, TradeUsage, self.testUserID)

        print(summaryInfo.taxTotal)

    def test_getFlatRatePopUpURL(self):

        url = self.htCashbillService.getFlatRatePopUpURL(self.testCorpNum, self.testUserID)

        print(url)

    def test_getCertificatePopUpURL(self):

        url = self.htCashbillService.getCertificatePopUpURL(self.testCorpNum, self.testUserID)

        print(url)

    def test_getFlatRateState(self):

        flatRateInfo = self.htCashbillService.getFlatRateState(self.testCorpNum, self.testUserID)

        tmp = flatRateInfo.referenceID + '\n'
        tmp += flatRateInfo.contractDT + '\n'
        tmp += flatRateInfo.useEndDate + '\n'
        tmp += str(flatRateInfo.baseDate) + '\n'
        tmp += str(flatRateInfo.state) + '\n'
        tmp += str(flatRateInfo.closeRequestYN) + '\n'
        tmp += str(flatRateInfo.useRestrictYN) + '\n'
        tmp += str(flatRateInfo.closeOnExpired) + '\n'
        tmp += str(flatRateInfo.unPaidYN) + '\n'

        print(tmp)

    def test_getCertificateExpireDate(self):

        expireDate = self.htCashbillService.getCertificateExpireDate(self.testCorpNum, self.testUserID)

        print(expireDate)


if __name__ == '__main__':
    unittest.main()
