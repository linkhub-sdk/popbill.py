# -*- coding: utf-8 -*-
# code for console Encoding difference. Dont' mind on it
import imp
import random
import sys

imp.reload(sys)
try:
    sys.setdefaultencoding("UTF8")
except Exception as E:
    pass

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from popbill import *


class HTCashbillServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.htCashbillService = HTCashbillService(
            "TESTER", "SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I="
        )
        self.htCashbillService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_checkID(self):
        response = self.htCashbillService.checkID("testkorea")
        self.assertEqual(response.code, 1, "해당 아이디 사용중")

    def test_registContact(self):
        contactInfo = ContactInfo(
            id="testkorea_0726",
            pwd="popbill",
            personName="정씨네",
            tel="",
            email="",
            searchAllAllowYN=True,
            mgrYN=False,
        )
        response = self.htCashbillService.registContact(
            self.testCorpNum, contactInfo, self.testUserID
        )
        self.assertEqual(response.code, 1, "담당자 추가 성공")

    def test_listContact(self):
        contactList = self.htCashbillService.listContact(
            self.testCorpNum, self.testUserID
        )
        self.assertGreater(len(contactList), 0, "담당자 목록 조회")

    def test_updateContact(self):
        contactInfo = ContactInfo(
            personName="담당자 성명_0728",
            tel="",
            email="",
            searchAllAllowYN=True,
            mgtYN=False,
        )
        response = self.htCashbillService.updateContact(
            self.testCorpNum, contactInfo, self.testUserID
        )
        self.assertEqual(response.code, 1, "담당자 정보 수정성공.")

    def test_getCorpInfo(self):
        corpInfo = self.htCashbillService.getCorpInfo(self.testCorpNum, self.testUserID)
        self.assertIsNotNone(corpInfo)

    def test_updateCorpInfo(self):
        corpInfo = CorpInfo(
            ceoname="대표자성명_0728",
            corpName="상호_0728",
            addr="주소_0728",
            bizType="업태_0728",
            bizClass="종목_0728",
        )
        response = self.htCashbillService.updateCorpInfo(
            self.testCorpNum, corpInfo, self.testUserID
        )
        self.assertEqual(response.code, 1, "회사정보 수정성공")

    def test_getChrgInfo(self):
        chrgInfo = self.htCashbillService.getChargeInfo(
            self.testCorpNum, self.testUserID
        )
        self.assertIsNotNone(chrgInfo)

        print("단가 : " + chrgInfo.unitCost)

    def test_requestJob(self):
        Type = "SELL"
        SDate = "20160601"
        EDate = "20160831"

        jobID = self.htCashbillService.requestJob(
            self.testCorpNum, Type, SDate, EDate, self.testUserID
        )
        self.assertIsNotNone(jobID, "수집 요청")

        print("작업아이디(jobID) : " + jobID)

    def test_getJobState(self):
        JobID = "016072811000000010"

        state = self.htCashbillService.getJobState(
            self.testCorpNum, JobID, self.testUserID
        )
        self.assertIsNotNone(state, "수집 상태 조회")

        tmp = "\n\t======== getJobState Response ========\n"
        tmp += "\tjobID : " + state.jobID + "\n"
        tmp += "\tjobState : " + str(state.jobState) + "\n"
        tmp += "\tqueryType : " + state.queryType + "\n"
        tmp += "\tqueryDateType : " + state.queryDateType + "\n"
        tmp += "\tqueryStDate : " + state.queryStDate + "\n"
        tmp += "\tqueryEnDate : " + state.queryEnDate + "\n"
        tmp += "\terrorCode : " + str(state.errorCode) + "\n"
        tmp += "\terrorReason : " + state.errorReason + "\n"
        tmp += "\tjobStartDT : " + state.jobStartDT + "\n"
        tmp += "\tjobEndDT : " + state.jobEndDT + "\n"
        tmp += "\tcollectCount : " + str(state.collectCount) + "\n"
        tmp += "\tregDT : " + state.regDT
        print(tmp)

    def test_listACtiveJob(self):
        jobInfos = self.htCashbillService.listActiveJob(
            self.testCorpNum, self.testUserID
        )
        self.assertIsNotNone(jobInfos, "수집 상태 목록 조회")

        state = jobInfos[0]

        tmp = "\n======== listACtiveJob Response ========\n"
        tmp += "\tjobID : " + state.jobID + "\n"
        tmp += "\tjobState : " + str(state.jobState) + "\n"
        tmp += "\tqueryType : " + state.queryType + "\n"
        tmp += "\tqueryDateType : " + state.queryDateType + "\n"
        tmp += "\tqueryStDate : " + state.queryStDate + "\n"
        tmp += "\tqueryEnDate : " + state.queryEnDate + "\n"
        tmp += "\terrorCode : " + str(state.errorCode) + "\n"
        tmp += "\terrorReason : " + state.errorReason + "\n"
        tmp += "\tjobStartDT : " + state.jobStartDT + "\n"
        tmp += "\tjobEndDT : " + state.jobEndDT + "\n"
        tmp += "\tcollectCount : " + str(state.collectCount) + "\n"
        tmp += "\tregDT : " + state.regDT + "\n"
        print(tmp)

    def test_search(self):
        JobID = "016072811000000010"
        TradeType = ["N", "C"]
        TradeUsage = ["P", "C"]
        Page = 1
        PerPage = 10
        Order = "D"

        searchInfo = self.htCashbillService.search(
            self.testCorpNum,
            JobID,
            TradeType,
            TradeUsage,
            Page,
            PerPage,
            Order,
            self.testUserID,
        )
        self.assertIsNotNone(searchInfo, "수집 결과 조회")

        tmp = "\n ======== search Response ========\n"
        tmp += "\t code : " + str(searchInfo.code) + "\n"
        tmp += "\t message : " + searchInfo.message + "\n"
        tmp += "\t total : " + str(searchInfo.total) + "\n"
        tmp += "\t perPage : " + str(searchInfo.perPage) + "\n"
        tmp += "\t pageNum : " + str(searchInfo.pageNum) + "\n"
        tmp += "\t pageCount : " + str(searchInfo.pageCount) + "\n"
        print(tmp)

    def test_summary(self):
        JobID = "016072811000000010"
        TradeType = ["N", "C"]
        TradeUsage = ["P", "C"]
        Page = 1
        PerPage = 10
        Order = "D"

        summaryInfo = self.htCashbillService.summary(
            self.testCorpNum, JobID, TradeType, TradeUsage, self.testUserID
        )
        self.assertIsNotNone(summaryInfo, "수집 결과 요약정보 조회")

        tmp = "\n ======== summary Response ========\n"
        tmp += "\t count : " + str(summaryInfo.count) + "\n"
        tmp += "\t supplyCostTotal : " + str(summaryInfo.supplyCostTotal) + "\n"
        tmp += "\t taxTotal : " + str(summaryInfo.taxTotal) + "\n"
        tmp += "\t serviceFeeTotal : " + str(summaryInfo.serviceFeeTotal) + "\n"
        tmp += "\t amountTotal : " + str(summaryInfo.amountTotal) + "\n"
        print(tmp)

    def test_getFlatRatePopUpURL(self):
        url = self.htCashbillService.getFlatRatePopUpURL(
            self.testCorpNum, self.testUserID
        )
        self.assertIsNotNone(url)

    def test_getCertificatePopUpURL(self):
        url = self.htCashbillService.getCertificatePopUpURL(
            self.testCorpNum, self.testUserID
        )
        self.assertIsNotNone(url)

    def test_getFlatRateState(self):

        flatRateInfo = self.htCashbillService.getFlatRateState(
            self.testCorpNum, self.testUserID
        )
        self.assertEqual(flatRateInfo.referenceID, self.testCorpNum, "정액제 서비스 상태 확인")

        tmp = "\n ======== FlatRateState Response ========\n"
        tmp += "\t referenceID : " + flatRateInfo.referenceID + "\n"
        tmp += "\t contractDT : " + flatRateInfo.contractDT + "\n"
        tmp += "\t useEndDate : " + flatRateInfo.useEndDate + "\n"
        tmp += "\t baseDate : " + str(flatRateInfo.baseDate) + "\n"
        tmp += "\t state : " + str(flatRateInfo.state) + "\n"
        tmp += "\t closeRequestYN : " + str(flatRateInfo.closeRequestYN) + "\n"
        tmp += "\t useRestrictYN : " + str(flatRateInfo.useRestrictYN) + "\n"
        tmp += "\t closeOnExpired : " + str(flatRateInfo.closeOnExpired) + "\n"
        tmp += "\t unPaidYN : " + str(flatRateInfo.unPaidYN) + "\n"

        print(tmp)

    def test_getCertificateExpireDate(self):
        expireDate = self.htCashbillService.getCertificateExpireDate(
            self.testCorpNum, self.testUserID
        )
        self.assertIsNotNone(expireDate)
        print("CertificateExpireDate : " + expireDate)

    def test_checkCertValidation(self):
        try:
            response = self.htCashbillService.checkCertValidation(self.testCorpNum)
            print(response.code)
            print(response.message)
        except PopbillException as PE:
            print(PE.message)

    def test_registDeptUser(self):
        try:
            response = self.htCashbillService.registDeptUser(
                self.testCorpNum, "cash_testpy", "123123"
            )
            print(response.code)
            print(response.message)
        except PopbillException as PE:
            print(PE.message)

    def test_checkDeptUser(self):
        try:
            response = self.htCashbillService.checkDeptUser(self.testCorpNum)
            print(response.code)
            print(response.message)
        except PopbillException as PE:
            print(PE.message)

    def test_checkLoginDeptUser(self):
        try:
            response = self.htCashbillService.checkLoginDeptUser(self.testCorpNum)
            print(response.code)
            print(response.message)
        except PopbillException as PE:
            print(PE.message)

    def test_deleteDeptUser(self):
        try:
            response = self.htCashbillService.deleteDeptUser(self.testCorpNum)
            print(response.code)
            print(response.message)
        except PopbillException as PE:
            print(PE.message)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(HTCashbillServiceTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
