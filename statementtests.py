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

class StatementServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.statementService =  StatementService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.statementService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"
        self.testMgtKey = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',10))

    def test_getChargeInfo(self):
        ItemCode = "126"
        chrgInfo = self.statementService.getChargeInfo(self.testCorpNum, ItemCode, self.testUserID)
        print(chrgInfo.rateSystem)
        print(chrgInfo.unitCost)
        print(chrgInfo.chargeMethod)

    def test_attachStatement(self):
        ItemCode = "121"
        MgtKey = "7czksfi09b"
        SubItemCode = "121"
        SubMgtKey = "fbrdavxpsn"
        response = self.statementService.attachStatement(self.testCorpNum,ItemCode,MgtKey,SubItemCode,SubMgtKey,self.testUserID)
        print(response.message)

    def test_detachStatement(self):
        ItemCode = "121"
        MgtKey = "7czksfi09b"
        SubItemCode = "121"
        SubMgtKey = "fbrdavxpsn"
        response = self.statementService.detachStatement(self.testCorpNum,ItemCode,MgtKey,SubItemCode,SubMgtKey,self.testUserID)
        print(response.message)

    def test_search(self):
        DType = "W"
        SDate = "20160701"
        EDate = "20160831"
        State = ["2**", "3**"]
        ItemCode = ["121", "122", "123","124", "125", "126"]
        Page = 1
        PerPage = 10
        Order = "D"
        QString = ""

        response = self.statementService.search(self.testCorpNum,DType,SDate,EDate,State,ItemCode,Page,PerPage,Order,self.testUserID,QString)
        print(response.total)

    def test_FAXSend(self):
        statement = Statement(writeDate = "20160725",
                                purposeType = "영수",
                                taxType = "과세",
                                formCode = "",
                                itemCode = 121,
                                mgtKey = self.testMgtKey,
                                senderCorpNum = "1234567890",
                                senderCorpName = "공급자 상호",
                                senderAddr = "공급자 주소",
                                senderCEOName = "공급자 대표자 성명",
                                senderTaxRegID = "",
                                senderBizClass = "업종",
                                senderBizType = "업태",
                                senderContactName = "공급자 담당자명",
                                senderEmail = "test@test.com",
                                senderTEL = "070-7510-3710",
                                senderHP = "010-000-222",

                                receiverCorpNum = "8888888888",
                                receiverCorpName = "공급받는자 상호",
                                receiverCEOName = "공급받는자 대표자 성명",
                                receiverAddr = "공급받는자 주소",
                                receiverTaxRegID = "",
                                receiverBizClass = "공급받는자 업종",
                                receiverBizType = "공급받는자 업태",
                                receiverContactName = "공급받는자 담당자명",
                                receiverEmail = "frenchofkiss@gmail.com",
                                receiverTEL = "070111222",
                                receiverHP = "010-111-222",

                                supplyCostTotal = "20000",
                                taxTotal = "2000",
                                totalAmount = "22000",
                                serialNum = "123",
                                remark1 = "비고1",
                                remark2 = "비고2",
                                remark3 = "비고3",

                                businessLIcenseYN = False,
                                bankBookYN = False,

                                propertyBag = {
                                        'Balance': '20000',
                                        'Deposit' : '5000',
                                        'CBalance': '25000'
                                },

                                detailList = [
                                                StatementDetail(serialNum = 1,
                                                                itemName = "품목1",
                                                                purchaseDT = "20150323",
                                                                qty = 1,
                                                                supplyCost = "20000",
                                                                tax = "2000"),
                                                StatementDetail(serialNum = 2,
                                                                itemName = "품목2")
                                ]
                            )

        SendNum = "070-7510-3710"
        ReceiveNum = "070-111-222"

        result = self.statementService.FAXSend(self.testCorpNum, statement, SendNum, ReceiveNum, self.testUserID)
        print(result)
    def test_01_registIssue(self):

        statement = Statement(writeDate = "20160725",
                                purposeType = "영수",
                                taxType = "과세",
                                formCode = "",
                                itemCode = 121,
                                mgtKey = self.testMgtKey,
                                senderCorpNum = "1234567890",
                                senderCorpName = "공급자 상호",
                                senderAddr = "공급자 주소",
                                senderCEOName = "공급자 대표자 성명",
                                senderTaxRegID = "",
                                senderBizClass = "업종",
                                senderBizType = "업태",
                                senderContactName = "공급자 담당자명",
                                senderEmail = "test@test.com",
                                senderTEL = "070-7510-3710",
                                senderHP = "010-000-222",

                                receiverCorpNum = "8888888888",
                                receiverCorpName = "공급받는자 상호",
                                receiverCEOName = "공급받는자 대표자 성명",
                                receiverAddr = "공급받는자 주소",
                                receiverTaxRegID = "",
                                receiverBizClass = "공급받는자 업종",
                                receiverBizType = "공급받는자 업태",
                                receiverContactName = "공급받는자 담당자명",
                                receiverEmail = "frenchofkiss@gmail.com",
                                receiverTEL = "070111222",
                                receiverHP = "010-111-222",

                                supplyCostTotal = "20000",
                                taxTotal = "2000",
                                totalAmount = "22000",
                                serialNum = "123",
                                remark1 = "비고1",
                                remark2 = "비고2",
                                remark3 = "비고3",

                                businessLIcenseYN = False,
                                bankBookYN = False,

                                propertyBag = {
                                        'Balance': '20000',
                                        'Deposit' : '5000',
                                        'CBalance': '25000'
                                },

                                detailList = [
                                                StatementDetail(serialNum = 1,
                                                                itemName = "품목1",
                                                                purchaseDT = "20150323",
                                                                qty = 1,
                                                                supplyCost = "20000",
                                                                tax = "2000"),
                                                StatementDetail(serialNum = 2,
                                                                itemName = "품목2")
                                ]
                            )

        Memo = "즉시발행 메모"
        result = self.statementService.registIssue(self.testCorpNum, statement, Memo, self.testUserID)
        print(result.message)

    def test_getInfos(self):
        infos = self.statementService.getInfos(self.testCorpNum,121,["20150707-01","20150706-01"])
        for info in infos:
            print("info : %s" % info.mgtKey)
            for key, value in info.__dict__.items():
                if not key.startswith("__"):
                    print("     %s : %s" % (key,value))
        self.assertGreater(len(infos),0,"갯수 확인")

    def test_getBalance(self):
        balance = self.statementService.getBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_getPartnerBalance(self):
        balance = self.statementService.getPartnerBalance(self.testCorpNum)
        print(balance)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_getPopbillURL(self):
        url = self.statementService.getPopbillURL(self.testCorpNum,self.testUserID,"LOGIN")
        self.assertEqual(url[:5], "https", "https로 시작")

    def test_checkIsMember(self):
        result = self.statementService.checkIsMember(self.testCorpNum)
        self.assertEqual(result.code,1,result.message + ", 가입시 코드는 1")

        result = self.statementService.checkIsMember("1234568790")
        self.assertEqual(result.code,0,result.message + ", 미가입시 코드는 0")

    def test_getURL(self):
        url = self.statementService.getURL(self.testCorpNum,self.testUserID,"TBOX")
        print("TBOX URL = "+url)
        self.assertEqual(url[:5], "https","https로 시작")

    def test_getUnitCost(self):
        unitCost = self.statementService.getUnitCost(self.testCorpNum, 121)
        self.assertGreaterEqual(unitCost,0,"단가는 0 이상.")

    def test_checkMgtKeyInUse(self):
        bIsInUse = self.statementService.checkMgtKeyInUse(self.testCorpNum,121,"20150319-10")
        self.assertEqual(bIsInUse,True, "등록으로 확인")

        bIsInUse = self.statementService.checkMgtKeyInUse(self.testCorpNum,121,"20150323-10")
        self.assertEqual(bIsInUse,False, "미등록으로 확인")

    def test_01_register(self):

        statement = Statement(writeDate = "20150323",
                                purposeType = "영수",
                                taxType = "과세",
                                formCode = "",
                                itemCode = 121,
                                mgtKey = "20150325-01",
                                senderCorpNum = "1234567890",
                                senderCorpName = "공급자 상호",
                                senderAddr = "공급자 주소",
                                senderCEOName = "공급자 대표자 성명",
                                senderTaxRegID = "",
                                senderBizClass = "업종",
                                senderBizType = "업태",
                                senderContactName = "공급자 담당자명",
                                senderEmail = "test@test.com",
                                senderTEL = "070-7510-3710",
                                senderHP = "010-000-222",

                                receiverCorpNum = "8888888888",
                                receiverCorpName = "공급받는자 상호",
                                receiverCEOName = "공급받는자 대표자 성명",
                                receiverAddr = "공급받는자 주소",
                                receiverTaxRegID = "",
                                receiverBizClass = "공급받는자 업종",
                                receiverBizType = "공급받는자 업태",
                                receiverContactName = "공급받는자 담당자명",

                                receiverEmail = "test@test.com",
                                receiverTEL = "070111222",
                                receiverHP = "010-111-222",

                                supplyCostTotal = "20000",
                                taxTotal = "2000",
                                totalAmount = "22000",
                                serialNum = "123",
                                remark1 = "비고1",
                                remark2 = "비고2",
                                remark3 = "비고3",

                                businessLIcenseYN = False,
                                bankBookYN = False,

                                propertyBag = {
                                        'Balance': '20000',
                                        'Deposit' : '5000',
                                        'CBalance': '25000'
                                },

                                detailList = [
                                                StatementDetail(serialNum = 1,
                                                                itemName = "품목1",
                                                                purchaseDT = "20150323",
                                                                qty = 1,
                                                                supplyCost = "20000",
                                                                tax = "2000"),
                                                StatementDetail(serialNum = 2,
                                                                itemName = "품목2")
                                ]
                            )

        result = self.statementService.register(self.testCorpNum,statement)
        self.assertEqual(result.code, 1, "등록 오류 : " + result.message)

    def test_02_update(self):

        statement = Statement(writeDate = "20150323",
                                purposeType = "영수",
                                taxType = "과세",
                                formCode = "",
                                itemCode = 121,
                                mgtKey = "20150325-01",
                                senderCorpNum = "1234567890",
                                senderCorpName = "공급자 상호",
                                senderAddr = "공급자 주소",
                                senderCEOName = "공급자 대표자 성명",
                                senderTaxRegID = "",
                                senderBizClass = "업종",
                                senderBizType = "업태",
                                senderContactName = "공급자 담당자명",
                                senderEmail = "test@test.com",
                                senderTEL = "070-7510-3710",
                                senderHP = "010-000-222",

                                receiverCorpNum = "8888888888",
                                receiverCorpName = "공급받는자 상호",
                                receiverCEOName = "공급받는자 대표자 성명",
                                receiverAddr = "공급받는자 주소",
                                receiverTaxRegID = "",
                                receiverBizClass = "공급받는자 업종",
                                receiverBizType = "공급받는자 업태",
                                receiverContactName = "공급받는자 담당자명",

                                receiverEmail = "test@test.com",
                                receiverTEL = "070111222",
                                receiverHP = "010-111-222",

                                supplyCostTotal = "20000",
                                taxTotal = "2000",
                                totalAmount = "22000",
                                serialNum = "123",
                                remark1 = "비고1",
                                remark2 = "비고2",
                                remark3 = "비고3",

                                businessLIcenseYN = False,
                                bankBookYN = False,

                                propertyBag = {
                                        'Balance': '20000',
                                        'Deposit' : '5000',
                                        'CBalance': '25000'
                                },

                                detailList = [
                                                StatementDetail(serialNum = 1,
                                                                itemName = "품목1",
                                                                purchaseDT = "20150323",
                                                                qty = 1,
                                                                supplyCost = "20000",
                                                                tax = "2000"),
                                                StatementDetail(serialNum = 2,
                                                                itemName = "품목2")
                                ]
                            )

        result = self.statementService.update(self.testCorpNum, 121, "20150325-01", statement)
        self.assertEqual(result.code, 1, "등록 오류 : " + result.message)


    def test_03_issue(self):
                result = self.statementService.issue(self.testCorpNum, 121, "20150325-01", "발행메모")
                self.assertEqual(result.code, 1, "발행 오류: "+result.message)

    def test_04_cancel(self):
            result = self.statementService.cancel(self.testCorpNum, 121, "20150325-01", "취소메모")
            self.assertEqual(result.code, 1, "발행취소 오류 : "+result.message)

    def test_05_getInfo(self):
            result = self.statementService.getInfo(self.testCorpNum, 121, "20150325-01")
            print(result.itemCode)
            self.assertEqual(result.itemCode, 121, "getInfo오류 :" + str(result.message))

    def test_06_getDetailInfo(self):
            result = self.statementService.getDetailInfo(self.testCorpNum, 121, "20150325-01")
            print(result.propertyBag.Balance)
            self.assertEqual(result.mgtKey, "20150325-01", "getDetail오류 :" + str(result.message))

    def test_07_sendEmail(self):

            result = self.statementService.sendEmail(self.testCorpNum, 121, "20150325-01", "test@test.com")
            self.assertEqual(result.code,1, "이메일 재전송 오류 : "+result.message)


    def test_08_sendSMS(self):

        result = self.statementService.sendSMS(self.testCorpNum, 121, "20150325-01", "07075103710","010111222","문자메시지 테스트")
        self.assertEqual(result.code,1, "알림문자 전송 오류 : "+result.message)


    def test_09_sendFax(self):
        result = self.statementService.sendFAX(self.testCorpNum, 121, "20150325-01", "07075103710","010111222")
        self.assertEqual(result.code,1, "알림문자 전송 오류 : "+result.message)

    def test_10_getLogs(self):
        result = self.statementService.getLogs(self.testCorpNum, 121, "20150325-01")
        print(result[3].procMemo)

    def test_021_attachFile(self):
        result = self.statementService.attachFile(self.testCorpNum, 121, "20150325-01", "test.jpeg")
        self.assertEqual(result.code,1, "파일 첨부 오류 : "+result.message)

    def test_022_getFilesAndDelete(self):
        result = self.statementService.getFiles(self.testCorpNum, 121, "20150325-01")
        print(result[0].attachedFile)

        result2 = self.statementService.deleteFile(self.testCorpNum, 121, "20150325-01", result[0].attachedFile)
        self.assertEqual(result2.code,1, "첨부파일 삭제오류 : "+result2.message)

    def test_023_getPopUpURL(self):
        url = self.statementService.getPopUpURL(self.testCorpNum, 121, "20150325-01", self.testUserID)
        print("popup url : "+url)
        self.assertEqual(url[:5], "https", "https로 시작 ")

    def test_024_getPrintURL(self):
        url = self.statementService.getPrintURL(self.testCorpNum, 121, "20150325-01", self.testUserID)
        print("print url : "+url)
        self.assertEqual(url[:5], "https", "https로 시작 ")

    def test_025_getEPrintURL(self):
        url = self.statementService.getEPrintURL(self.testCorpNum, 121, "20150325-01", self.testUserID)
        print("Eprint url : "+url)
        self.assertEqual(url[:5], "https", "https로 시작 ")

    def test_026_getMailURL(self):
        url = self.statementService.getMailURL(self.testCorpNum, 121, "20150325-01", self.testUserID)
        print("Mail url : "+url)
        self.assertEqual(url[:5], "https", "https로 시작 ")

    def test_027_getMassPrintURL(self):
        MgtKeyList = ["20150323-01", "20150319-01"]
        url = self.statementService.getMassPrintURL(self.testCorpNum, 121, MgtKeyList, self.testUserID)
        print("Massprint url : "+url)
        self.assertEqual(url[:5], "https", "https로 시작 ")

    def test_99_delete(self):
        result = self.statementService.delete(self.testCorpNum, 121, "20150325-01")
        self.assertEqual(result.code,1, "삭제 오류 : "+result.message)

if __name__ == '__main__':
    unittest.main()
