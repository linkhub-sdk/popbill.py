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
from datetime import datetime
from popbill import *


class EasyFinBankServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.easyFinBankService = EasyFinBankService('TESTER', 'SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.easyFinBankService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_getChargeInfo(self):
        chrgInfo = self.easyFinBankService.getChargeInfo(self.testCorpNum, self.testUserID)
        print(chrgInfo.unitCost)
        print(chrgInfo.chargeMethod)
        print(chrgInfo.rateSystem)

    def test_getBankAccountMgtURL(self):
        url = self.easyFinBankService.getBankAccountMgtURL(self.testCorpNum)
        self.assertIsNotNone(url, "URL")
        print url

    def test_listBankAccount(self):
        bankAccountInfo = self.easyFinBankService.listBankAccount(self.testCorpNum, self.testUserID)
        self.assertIsNotNone(bankAccountInfo, "확인")
        print bankAccountInfo[11].accountNumber

    def test_requestJob(self):
        BankCode = "0048"
        AccountNumber = "131020538645"
        SDate = "20191004"
        EDate = "20191231"
        jobID = self.easyFinBankService.requestJob(self.testCorpNum, BankCode, AccountNumber, SDate, EDate, self.testUserID)
        print("작업아이디 : " + jobID)
        self.assertIsNotNone(jobID, "수집요청 작업아이디 확인")

    def test_getJobState(self):
        JobID = "020010211000000001"

        state = self.easyFinBankService.getJobState(self.testCorpNum, JobID, self.testUserID)
        self.assertIsNotNone(state, "수집 상태 확인")
        tmp = '\n\t======== getJobState Response ========\n'
        tmp += '\tjobID : ' + state.jobID + '\n'
        tmp += '\tjobState : ' + str(state.jobState) + '\n'
        tmp += '\tstartDate : ' + state.startDate + '\n'
        tmp += '\tendDate : ' + state.endDate + '\n'
        tmp += '\terrorCode : ' + str(state.errorCode) + '\n'
        tmp += '\terrorReason : ' + state.errorReason + '\n'
        tmp += '\tjobStartDT : ' + state.jobStartDT + '\n'
        tmp += '\tjobEndDT : ' + state.jobEndDT + '\n'
        tmp += '\tregDT : ' + state.regDT
        print(tmp)


    def test_listACtiveJob(self):
        jobInfos = self.easyFinBankService.listActiveJob(self.testCorpNum, self.testUserID)
        self.assertIsNotNone(jobInfos, "수집 목록 확인")

        # 020010211000000001
        state = jobInfos[0]

        tmp = '\n\t======== listACtiveJob Response ========\n'
        tmp += '\tjobID : ' + state.jobID + '\n'
        tmp += '\tjobState : ' + str(state.jobState) + '\n'
        tmp += '\tstartDate : ' + state.startDate + '\n'
        tmp += '\tendDate : ' + state.endDate + '\n'
        tmp += '\terrorCode : ' + str(state.errorCode) + '\n'
        tmp += '\terrorReason : ' + state.errorReason + '\n'
        tmp += '\tjobStartDT : ' + state.jobStartDT + '\n'
        tmp += '\tjobEndDT : ' + state.jobEndDT + '\n'
        tmp += '\tregDT : ' + state.regDT
        print(tmp)

    def test_search(self):
        JobID = "020010211000000001"
        TradeType = ["I", "O"]
        SearchString = ""
        Page = 1
        PerPage = 10
        Order = "D"

        try:
            searchInfo = self.easyFinBankService.search(self.testCorpNum, JobID, TradeType, SearchString,
                                                     Page, PerPage, Order, self.testUserID)
            self.assertIsNotNone(searchInfo, "수집 결과 조회")

            tmp = '\n\t======== search Response ========\n'
            tmp += '\t code : ' + str(searchInfo.code) + '\n'
            tmp += '\t message : ' + searchInfo.message + '\n'
            tmp += '\t total : ' + str(searchInfo.total) + '\n'
            tmp += '\t perPage : ' + str(searchInfo.perPage) + '\n'
            tmp += '\t pageNum : ' + str(searchInfo.pageNum) + '\n'
            tmp += '\t pageCount : ' + str(searchInfo.pageCount) + '\n'

            print(tmp)
            print(str(searchInfo.list[0].tid))
            print(str(searchInfo.list[0].memo))
        except PopbillException as e:
            print(e.code)

    def test_summary(self):
        JobID = "020010211000000001"
        TradeType = ["I", "O"]
        SearchString = ""

        try:
            searchInfo = self.easyFinBankService.summary(self.testCorpNum, JobID, TradeType, SearchString)
            self.assertIsNotNone(searchInfo, "수집 결과 요약정보 조회")

            tmp = '\n\t======== summary Response ========\n'
            tmp += '\t count : ' + str(searchInfo.count) + '\n'
            tmp += '\t cntAccIn : ' + str(searchInfo.cntAccIn) + '\n'
            tmp += '\t cntAccOut : ' + str(searchInfo.cntAccOut) + '\n'
            tmp += '\t totalAccIn : ' + str(searchInfo.totalAccIn) + '\n'
            tmp += '\t totalAccOut : ' + str(searchInfo.totalAccOut) + '\n'

            print(tmp)
        except PopbillException as e:
            print(e.code)

    def test_saveMemo(self):
        memo = '20200102-memo'
        tid = '01912181100000000120191231000001'

        response = self.easyFinBankService.saveMemo(self.testCorpNum, tid, memo, self.testUserID)
        self.assertNotEqual(response.code, "1")
        print(response.code)

    def test_getFlatRatePopUpURL(self):
        url = self.easyFinBankService.getFlatRatePopUpURL(self.testCorpNum)
        self.assertIsNotNone(url, "URL")
        print url

    def test_getFlatRateState(self):
        BankCode = "0048"
        AccountNumber = "131020538645"
        flatRateInfo = self.easyFinBankService.getFlatRateState(self.testCorpNum, BankCode, AccountNumber, self.testUserID)

        print(flatRateInfo.referenceID)
