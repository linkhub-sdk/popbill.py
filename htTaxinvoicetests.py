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
from popbill import *


class HTTaxinvoiceServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.htTaxinvoiceService = HTTaxinvoiceService('TESTER', 'SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.htTaxinvoiceService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_getPartnerURL(self):
        url = self.htTaxinvoiceService.getPartnerURL(self.testCorpNum, "CHRG")
        self.assertIsNotNone(url, "파트너 포인트 충전 URL")
        print url

    def test_checkID(self):
        response = self.htTaxinvoiceService.checkID("testkorea")
        self.assertEqual(response.code, 1, "해당 아이디 사용중")

    def test_registContact(self):
        contactInfo = ContactInfo(
            id="testkorea_0726",
            pwd="popbill",
            personName="정씨네",
            tel="010-1234-1234",
            hp="010-4324-5117",
            fax="070-7510-3710",
            email="code@linkhub.co.kr",
            searchAllAllowYN=True,
            mgrYN=False
        )
        response = self.htTaxinvoiceService.registContact(self.testCorpNum, contactInfo, self.testUserID)
        self.assertEqual(response.code, 1, "담당자 추가 성공")

    def test_listContact(self):
        contactList = self.htTaxinvoiceService.listContact(self.testCorpNum, self.testUserID)
        self.assertGreater(len(contactList), 0, "담당자 목록 조회")

    def test_updateContact(self):
        contactInfo = ContactInfo(
            personName="담당자 성명_0728",
            tel="010-8888-8888",
            hp="010-8888-8888",
            fax="02-6442-9700",
            email="weicome@linkhub.co.kr",
            searchAllAllowYN=True,
            mgtYN=False
        )
        response = self.htTaxinvoiceService.updateContact(self.testCorpNum, contactInfo, self.testUserID)
        self.assertEqual(response.code, 1, "담당자 정보 수정성공.")

    def test_getCorpInfo(self):
        corpInfo = self.htTaxinvoiceService.getCorpInfo(self.testCorpNum, self.testUserID)
        self.assertIsNotNone(corpInfo)

    def test_updateCorpInfo(self):
        corpInfo = CorpInfo(
            ceoname="대표자성명_0728",
            corpName="상호_0728",
            addr="주소_0728",
            bizType="업태_0728",
            bizClass="종목_0728"
        )
        response = self.htTaxinvoiceService.updateCorpInfo(self.testCorpNum, corpInfo, self.testUserID)
        self.assertEqual(response.code, 1, "회사정보 수정성공")

    def test_getChrgInfo(self):
        chrgInfo = self.htTaxinvoiceService.getChargeInfo(self.testCorpNum, self.testUserID)
        self.assertIsNotNone(chrgInfo)
        print("단가 : " + chrgInfo.unitCost)

    def test_requestJob(self):
        Type = "SELL"
        DType = "W"
        SDate = "20180101"
        EDate = "20181008"
        jobID = self.htTaxinvoiceService.requestJob(self.testCorpNum, Type, DType, SDate, EDate, self.testUserID)
        print("작업아이디 : " + jobID)
        self.assertIsNotNone(jobID, "수집요청 작업아이디 확인")

    def test_getJobState(self):
        JobID = "016072810000000006"

        state = self.htTaxinvoiceService.getJobState(self.testCorpNum, JobID, self.testUserID)
        self.assertIsNotNone(state, "수집 상태 확인")

        tmp = '\n\t======== getJobState Response ========\n'
        tmp += '\tjobID : ' + state.jobID + '\n'
        tmp += '\tjobState : ' + str(state.jobState) + '\n'
        tmp += '\tqueryType : ' + state.queryType + '\n'
        tmp += '\tqueryDateType : ' + state.queryDateType + '\n'
        tmp += '\tqueryStDate : ' + state.queryStDate + '\n'
        tmp += '\tqueryEnDate : ' + state.queryEnDate + '\n'
        tmp += '\terrorCode : ' + str(state.errorCode) + '\n'
        tmp += '\terrorReason : ' + state.errorReason + '\n'
        tmp += '\tjobStartDT : ' + state.jobStartDT + '\n'
        tmp += '\tjobEndDT : ' + state.jobEndDT + '\n'
        tmp += '\tcollectCount : ' + str(state.collectCount) + '\n'
        tmp += '\tregDT : ' + state.regDT
        print(tmp)

    def test_listACtiveJob(self):
        jobInfos = self.htTaxinvoiceService.listActiveJob(self.testCorpNum, self.testUserID)
        self.assertIsNotNone(jobInfos, "수집 목록 확인")

        state = jobInfos[0]

        tmp = '\n\t======== listACtiveJob Response ========\n'
        tmp += '\tjobID : ' + state.jobID + '\n'
        tmp += '\tjobState : ' + str(state.jobState) + '\n'
        tmp += '\tqueryType : ' + state.queryType + '\n'
        tmp += '\tqueryDateType : ' + state.queryDateType + '\n'
        tmp += '\tqueryStDate : ' + state.queryStDate + '\n'
        tmp += '\tqueryEnDate : ' + state.queryEnDate + '\n'
        tmp += '\terrorCode : ' + str(state.errorCode) + '\n'
        tmp += '\terrorReason : ' + state.errorReason + '\n'
        tmp += '\tjobStartDT : ' + state.jobStartDT + '\n'
        tmp += '\tjobEndDT : ' + state.jobEndDT + '\n'
        tmp += '\tcollectCount : ' + str(state.collectCount) + '\n'
        tmp += '\tregDT : ' + state.regDT
        print(tmp)

    def test_search(self):
        JobID = "016072810000000013"
        Type = ["N", "M"]
        TaxType = ["T", "N", "Z"]
        PurposeType = ["R", "C", "N"]
        TaxRegIDType = "S"
        TaxRegIDYN = ""
        TaxRegID = ""
        Page = 1
        PerPage = 10
        Order = "D"

        searchInfo = self.htTaxinvoiceService.search(self.testCorpNum, JobID, Type, TaxType, PurposeType, TaxRegIDType,
                                                     TaxRegIDYN, TaxRegID, Page, PerPage, Order, self.testUserID)
        self.assertIsNotNone(searchInfo, "수집 결과 조회")

        tmp = '\n\t======== search Response ========\n'
        tmp += '\t code : ' + str(searchInfo.code) + '\n'
        tmp += '\t message : ' + searchInfo.message + '\n'
        tmp += '\t total : ' + str(searchInfo.total) + '\n'
        tmp += '\t perPage : ' + str(searchInfo.perPage) + '\n'
        tmp += '\t pageNum : ' + str(searchInfo.pageNum) + '\n'
        tmp += '\t pageCount : ' + str(searchInfo.pageCount) + '\n'

        print(tmp)

    def test_summary(self):
        JobID = "016072810000000013"
        Type = ["N", "M"]
        TaxType = ["T", "N", "Z"]
        PurposeType = ["R", "C", "N"]
        TaxRegIDType = "S"
        TaxRegIDYN = ""
        TaxRegID = ""

        summaryInfo = self.htTaxinvoiceService.summary(self.testCorpNum, JobID, Type, TaxType, PurposeType,
                                                       TaxRegIDType, TaxRegIDYN, TaxRegID, self.testUserID)
        self.assertIsNotNone(summaryInfo, "수집결과 요약정보 조회")

        tmp = '\n\t======== Summary Response ========\n'
        tmp += '\t count : ' + str(summaryInfo.count) + '\n'
        tmp += '\t supplyCostTotal : ' + str(summaryInfo.supplyCostTotal) + '\n'
        tmp += '\t taxTotal : ' + str(summaryInfo.taxTotal) + '\n'
        tmp += '\t amountTotal : ' + str(summaryInfo.amountTotal) + '\n'

        print(tmp)

    def test_getTaxinvoice(self):
        NTSConfirmNum = "201607274100002900000209"
        taxinvoiceInfo = self.htTaxinvoiceService.getTaxinvoice(self.testCorpNum, NTSConfirmNum, self.testUserID)
        self.assertIsNotNone(taxinvoiceInfo, "상세정보 조회")

    def test_getXML(self):
        NTSConfirmNum = "201607274100002900000209"
        taxinvoiceXML = self.htTaxinvoiceService.getXML(self.testCorpNum, NTSConfirmNum, self.testUserID)
        self.assertIsNotNone(taxinvoiceXML, "상세정보 조회-XML")

    def test_getFlatRatePopUpURL(self):
        url = self.htTaxinvoiceService.getCertificatePopUpURL(self.testCorpNum, self.testUserID)
        self.assertIsNotNone(url, "정액제 결제 신청 URL")
        print url

    def test_getFlatRateState(self):
        flatRateInfo = self.htTaxinvoiceService.getFlatRateState(self.testCorpNum, self.testUserID)
        self.assertEqual(flatRateInfo.referenceID, self.testCorpNum)

    def test_getCertificateExpireDate(self):
        expireDate = self.htTaxinvoiceService.getCertificateExpireDate(self.testCorpNum, self.testUserID)
        self.assertIsNotNone(expireDate, "홈택스 공인인증서 만료일시 확인")

    def test_getPopUpURL(self):
        NTSConfirmNum = "201809194100020300000cd5"
        url = self.htTaxinvoiceService.getPopUpURL(self.testCorpNum, NTSConfirmNum)
        print url

    def test_checkCertValidation(self):
        try:
            response = self.htTaxinvoiceService.checkCertValidation(self.testCorpNum)
            print response.code
            print response.message
        except PopbillException as PE:
            print(PE.message)

    def test_registDeptUser(self):
        try:
            response = self.htTaxinvoiceService.registDeptUser(self.testCorpNum, "testpy", "123123")
            print response.code
            print response.message
        except PopbillException as PE:
            print(PE.message)

    def test_checkDeptUser(self):
        try:
            response = self.htTaxinvoiceService.checkDeptUser(self.testCorpNum)
            print response.code
            print response.message
        except PopbillException as PE:
            print(PE.message)

    def test_checkLoginDeptUser(self):
        try:
            response = self.htTaxinvoiceService.checkLoginDeptUser(self.testCorpNum)
            print response.code
            print response.message
        except PopbillException as PE:
            print(PE.message)

    def test_deleteDeptUser(self):
        try:
            response = self.htTaxinvoiceService.deleteDeptUser(self.testCorpNum)
            print response.code
            print response.message
        except PopbillException as PE:
            print(PE.message)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HTTaxinvoiceServiceTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
