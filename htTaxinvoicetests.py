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

class HTTaxinvoiceServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.htTaxinvoiceService =  HTTaxinvoiceService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.htTaxinvoiceService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_getChrgInfo(self):
        chrgInfo = self.htTaxinvoiceService.getChargeInfo(self.testCorpNum, self.testUserID)
        print(chrgInfo.rateSystem)
        print(chrgInfo.chargeMethod)
        print(chrgInfo.unitCost)

    def test_requestJob(self):
        Type = "SELL"
        DType = "W"
        SDate = "20160601"
        EDate = "20160831"
        jobID = self.htTaxinvoiceService.requestJob(self.testCorpNum, Type, DType, SDate, EDate, self.testUserID)
        print (jobID)

    def test_getJobState(self):
        JobID = "016072714000000003"

        state = self.htTaxinvoiceService.getJobState(self.testCorpNum, JobID, self.testUserID)

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
        jobInfos = self.htTaxinvoiceService.listActiveJob(self.testCorpNum, self.testUserID)

        state = jobInfos[1]

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
        JobID = "016072714000000003"
        Type = ["N", "M"]
        TaxType = ["T", "N", "Z"]
        PurposeType = ["R", "C", "N"]
        TaxRegIDType = "S"
        TaxRegIDYN = ""
        TaxRegID = ""
        Page = 1
        PerPage = 10
        Order = "D"

        searchInfo = self.htTaxinvoiceService.search(self.testCorpNum, JobID, Type, TaxType, PurposeType, TaxRegIDType, TaxRegIDYN, TaxRegID, Page, PerPage, Order, self.testUserID)

        print(searchInfo.total)
        print(searchInfo.list[0].ntsconfirmNum)

    def test_summary(self):
        JobID = "016072714000000003"
        Type = ["N", "M"]
        TaxType = ["T", "N", "Z"]
        PurposeType = ["R", "C", "N"]
        TaxRegIDType = "S"
        TaxRegIDYN = ""
        TaxRegID = ""

        summaryInfo = self.htTaxinvoiceService.summary(self.testCorpNum, JobID, Type, TaxType, PurposeType, TaxRegIDType, TaxRegIDYN, TaxRegID, self.testUserID)

        print(summaryInfo.count)

    def test_getTaxinvoice(self):
        NTSConfirmNum = "201607274100002900000209"

        taxinvoiceInfo = self.htTaxinvoiceService.getTaxinvoice(self.testCorpNum, NTSConfirmNum, self.testUserID)

        print(taxinvoiceInfo.ntsconfirmNum)

    def test_getXML(self):
        NTSConfirmNum = "201607274100002900000209"

        taxinvoiceInfo = self.htTaxinvoiceService.getXML(self.testCorpNum, NTSConfirmNum, self.testUserID)

        print(taxinvoiceInfo.retObject)

    def test_getFlatRatePopUpURL(self):

        url = self.htTaxinvoiceService.getCertificatePopUpURL(self.testCorpNum, self.testUserID)

        print(url)

    def test_getFlatRateState(self):

        flatRateInfo = self.htTaxinvoiceService.getFlatRateState(self.testCorpNum, self.testUserID)

        print(flatRateInfo.unPaidYN)

    def test_getCertificateExpireDate(self):

        expireDate = self.htTaxinvoiceService.getCertificateExpireDate(self.testCorpNum, self.testUserID)

        print(expireDate)


if __name__ == '__main__':
    unittest.main()
