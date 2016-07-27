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
from datetime import datetime
from popbill import *

class TaxinvoiceServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.taxinvoiceService =  TaxinvoiceService('TESTER','SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.taxinvoiceService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"
        self.testMgtKey = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',10))

    def test_attachStmt(self):
        response = self.taxinvoiceService.attachStatement(self.testCorpNum, "SELL", "chzovl6d5u", "121", "fbrdavxpsn", self.testUserID)
        print(response.message)

    def test_detachStmt(self):
        response = self.taxinvoiceService.detachStatement(self.testCorpNum, "SELL", "chzovl6d5u", "121", "fbrdavxpsn", self.testUserID)
        print(response.message)

    def test_1_registIssue(self):

        taxinvoice = Taxinvoice(writeDate = "20160725", #작성일자
                                chargeDirection = "정과금",
                                issueType = "정발행",
                                purposeType = "영수",
                                issueTiming = "직접발행",
                                taxType = "과세",
                                invoicerCorpNum = self.testCorpNum,
                                invoicerTaxRegID = '',
                                invoicerCorpName = "공급자 상호",
                                invoicerMgtKey = self.testMgtKey,
                                invoicerCEOName = "공급자 대표자 성명",
                                invoicerAddr = "공급자 주소",
                                invoicerBizClass = "공급자 업종",
                                invoicerBizType = "공급자 업태",
                                invoicerContactName = "공급자 담당자명",
                                invoicerEmail = "test@test.com",
                                invoicerTEL = "070-7510-6766",
                                invoicerHP = '010-1111-2222',
                                invoicerSMSSendYN = False,

                                invoiceeType = '사업자',
                                invoiceeCorpNum = '8888888888',
                                invoiceeCorpName = "공급받는자 상호_#$@#$!<>&_Python",
                                invoiceeMgtKey = None,
                                invoiceeCEOName = "공급받는자 상호",
                                invoiceeAddr = "공급받는자 주소",
                                invoiceeBizClass = "공급받는자 업종",
                                invoiceeBizType = "공급받는자 업태",
                                invoiceeContactName1 = "공급받는자 담당자",
                                invoiceeEmail1 = "frenchofkiss@gmail.com",
                                invoiceeHP1 = "010-2222-1111",
                                invoiceeFAX1 = "070-7510-6767",

                                supplyCostTotal = "100000",
                                taxTotal = "10000",
                                totalAmount = "110000",

                                modifyCode = None,
                                originalTaxinvoiceKey = None,
                                serialNum = '123',
                                cash = '',
                                chkBill = None,
                                credit = '',
                                remark1 = '비고1',
                                remark2 = '비고2',
                                remark3 = '비고3',
                                kwon = 1,
                                ho = 2,

                                businessLicenseYN  = False,
                                bankBookYN = False,

                                detailList = [
                                                TaxinvoiceDetail(serialNum = 1,
                                                                 purchaseDT = '20150121',
                                                                 itemName="품목1",
                                                                 spec = '규격',
                                                                 qty = 1,
                                                                 unitCost = '100000',
                                                                 supplyCost = '100000',
                                                                 tax = '10000',
                                                                 remark = '품목비고'),
                                                TaxinvoiceDetail(serialNum = 2,
                                                                 itemName = "품목2")
                                                ],
                                addContactList = [
                                                    Contact(serialNum = 1,
                                                            contactName='추가담당자 성명',
                                                            email='test1@test.com'),
                                                    Contact(serialNum = 2,
                                                            contactName='추가담당자2',
                                                            email='test2@test.com')
                                                ]

                                )

        writeSpecification = False
        forceIssue = False
        dealInvoiceMgtKey = "20160725-03"
        memo = "즉시발행 체크"
        emailSubject = "즉시발행메일_20160725"

        result = self.taxinvoiceService.registIssue(self.testCorpNum, taxinvoice, writeSpecification, forceIssue, dealInvoiceMgtKey, memo, emailSubject, self.testUserID)
        print(result.message)
        self.assertEqual(result.code,1,"등록 오류 : " + result.message)


    def test_search(self):
        MgtKeyType = "SELL"
        DType = "W"
        SDate = "20160601"
        EDate = "20160831"
        State = ["3**", "6**"]
        Type = ["N", "M"]
        TaxType = ["T", "N", "Z"]
        LateOnly = ""
        TaxRegIDYN = ""
        TaxRegIDType = "S"
        TaxRegID = ""
        Page = 1
        PerPage = 10
        Order = "D"

        response = self.taxinvoiceService.search(self.testCorpNum,MgtKeyType,DType,SDate,EDate,State,Type,TaxType,LateOnly,TaxRegIDYN,TaxRegIDType,TaxRegID,Page,PerPage,Order,self.testUserID)

        print(response.code)
    def test_getInfos(self):
        infos = self.taxinvoiceService.getInfos(self.testCorpNum,"SELL",["1234","1234567890"])
        self.assertGreater(len(infos),0,"갯수 확인")
    def test_checkID(self):
        response = self.taxinvoiceService.checkID('testkorea')
        print(response.message)

    def test_registContact(self) :
        contactInfo = ContactInfo (
                        id = "testkorea_0725",
                        pwd = "popbill",
                        personName = "정씨네",
                        tel = "010-1234-1234",
                        hp = "010-4324-5117",
                        fax = "070-7510-3710",
                        email = "code@linkhub.co.kr",
                        searchAllAllowYN = True,
                        mgrYN = True
                        )
        response = self.taxinvoiceService.registContact(self.testCorpNum, contactInfo, self.testUserID)
        print(response.message)

    def test_updateCorpInfo(self) :
        corpInfo = CorpInfo (
                        ceoname = "대표자성명_0725",
                        corpName = "상호_0725",
                        addr = "주소_0725",
                        bizType = "업태_0725",
                        bizClass = "업종_0725"
                        )
        response = self.taxinvoiceService.updateCorpInfo(self.testCorpNum, corpInfo, self.testUserID)
        print(response.message)
    def test_getCorpInfo(self):
        corpInfo = self.taxinvoiceService.getCorpInfo(self.testCorpNum, self.testUserID)
        print(corpInfo.addr)

    def test_getChargeInfo(self):
        chrgInfo = self.taxinvoiceService.getChargeInfo(self.testCorpNum,self.testUserID)
        print (chrgInfo.unitCost)
        print (chrgInfo.rateSystem)


    def test_listContact(self):
        contactList = self.taxinvoiceService.listContact(self.testCorpNum)
        print (contactList[1].id)

    def test_updateContact(self):
        contactInfo = ContactInfo(
                            personName = "담당자 성명_py",
                            tel = "010-1234-1234",
                            hp = "010-4324-4324",
                            fax = "02-6442-9700",
                            email = "code@linkhub.co.kr",
                            searchAllAllowYN = True,
                            mgtYN = False
                            )
        response = self.taxinvoiceService.updateContact(self.testCorpNum, contactInfo, self.testUserID)
        print (response.message)

    def test_getBalance(self):
        balance = self.taxinvoiceService.getBalance(self.testCorpNum)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')
        balance = self.taxinvoiceService.getBalance(self.testCorpNum)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_getPartnerBalance(self):
        balance = self.taxinvoiceService.getPartnerBalance(self.testCorpNum)
        self.assertGreaterEqual(balance,0,'잔액 0 이상.')

    def test_getPopbillURL(self):
        url = self.taxinvoiceService.getPopbillURL(self.testCorpNum,self.testUserID,"CHRG")
        self.assertEqual(url[:5],"https","https로시작")

    def test_checkIsMember(self):
        result = self.taxinvoiceService.checkIsMember(self.testCorpNum)
        self.assertEqual(result.code,1,result.message + ", 가입시 코드는 1")

        result = self.taxinvoiceService.checkIsMember("1234568790")
        self.assertEqual(result.code,0,result.message + ", 미가입시 코드는 0")

    def test_joinMember(self):
        newMember = JoinForm(CorpNum = "1231212312",
                            CorpName = "테스트가입상호",
                            CEOName = "테스트대표자성명",
                            Addr = "테스트 회사 주소",
                            ZipCode = "123-231",
                            BizType = "테스트업태",
                            BizClass = "테스트업종",
                            ID = "testUserID",
                            PWD = "testPassword",
                            ContactName = "담당자성명",
                            ContactTEL = "070-7510-6766",
                            ContactHP = "010-2222-3333",
                            ContactFAX = "070-7510-6767",
                            ContactEmail = "test@test.com")
        self.assertRaises(PopbillException, self.taxinvoiceService.joinMember , newMember)

    def test_getURL(self):
        url = self.taxinvoiceService.getURL(self.testCorpNum,self.testUserID,"SBOX")
        self.assertEqual(url[:5],"https","https로시작")

    def test_getUnitCost(self):
        unitCost = self.taxinvoiceService.getUnitCost(self.testCorpNum)
        self.assertGreaterEqual(unitCost,0,"단가는 0 이상.")

    def test_getCertificateExpireDate(self):
        expireDate = self.taxinvoiceService.getCertificateExpireDate("4108600477")
        self.assertGreaterEqual(expireDate,datetime.today(),"만료일은 오늘보다 큰날.")

    def test_getEmailPublicKeys(self):
        Emails = self.taxinvoiceService.getEmailPublicKeys(self.testCorpNum)
        self.assertGreaterEqual(len(Emails),0,"이메일 목록은 1개 이상")

    def test_checkMgtKeyInUse(self):
        bIsInUse = self.taxinvoiceService.checkMgtKeyInUse(self.testCorpNum,"SELL","1234")
        self.assertEqual(bIsInUse,True,"등록으로 확인")

        bIsInUse = self.taxinvoiceService.checkMgtKeyInUse(self.testCorpNum,"SELL","12345678901")
        self.assertEqual(bIsInUse,False,"미등록으로 확인")

    def test_1_register(self):

        taxinvoice = Taxinvoice(writeDate = "20150121", #작성일자
                                chargeDirection = "정과금",
                                issueType = "정발행",
                                purposeType = "영수",
                                issueTiming = "직접발행",
                                taxType = "과세",
                                invoicerCorpNum = self.testCorpNum,
                                invoicerTaxRegID = '',
                                invoicerCorpName = "공급자 상호",
                                invoicerMgtKey = self.testMgtKey,
                                invoicerCEOName = "공급자 대표자 성명",
                                invoicerAddr = "공급자 주소",
                                invoicerBizClass = "공급자 업종",
                                invoicerBizType = "공급자 업태",
                                invoicerContactName = "공급자 담당자명",
                                invoicerEmail = "test@test.com",
                                invoicerTEL = "070-7510-6766",
                                invoicerHP = '010-1111-2222',
                                invoicerSMSSendYN = False,

                                invoiceeType = '사업자',
                                invoiceeCorpNum = '8888888888',
                                invoiceeCorpName = "공급받는자 상호_#$@#$!<>&_Python",
                                invoiceeMgtKey = None,
                                invoiceeCEOName = "공급받는자 상호",
                                invoiceeAddr = "공급받는자 주소",
                                invoiceeBizClass = "공급받는자 업종",
                                invoiceeBizType = "공급받는자 업태",
                                invoiceeContactName1 = "공급받는자 담당자",
                                invoiceeEmail1 = "test@test.com",
                                invoiceeHP1 = "010-2222-1111",
                                invoiceeFAX1 = "070-7510-6767",

                                supplyCostTotal = "100000",
                                taxTotal = "10000",
                                totalAmount = "110000",

                                modifyCode = None,
                                originalTaxinvoiceKey = None,
                                serialNum = '123',
                                cash = '',
                                chkBill = None,
                                credit = '',
                                remark1 = '비고1',
                                remark2 = '비고2',
                                remark3 = '비고3',
                                kwon = 1,
                                ho = 2,

                                businessLicenseYN  = False,
                                bankBookYN = False,

                                detailList = [
                                                TaxinvoiceDetail(serialNum = 1,
                                                                 purchaseDT = '20150121',
                                                                 itemName="품목1",
                                                                 spec = '규격',
                                                                 qty = 1,
                                                                 unitCost = '100000',
                                                                 supplyCost = '100000',
                                                                 tax = '10000',
                                                                 remark = '품목비고'),
                                                TaxinvoiceDetail(serialNum = 2,
                                                                 itemName = "품목2")
                                                ],
                                addContactList = [
                                                    Contact(serialNum = 1,
                                                            contactName='추가담당자 성명',
                                                            email='test1@test.com'),
                                                    Contact(serialNum = 2,
                                                            contactName='추가담당자2',
                                                            email='test2@test.com')
                                                ]

                                )

        result = self.taxinvoiceService.register(self.testCorpNum,taxinvoice)
        print(result.message)
        self.assertEqual(result.code,1,"등록 오류 : " + result.message)

    def test_update(self):

        taxinvoice = Taxinvoice(writeDate = "20150121", #작성일자
                                chargeDirection = "정과금",
                                issueType = "정발행",
                                purposeType = "영수",
                                issueTiming = "직접발행",
                                taxType = "과세",
                                invoicerCorpNum = self.testCorpNum,
                                invoicerTaxRegID = '',
                                invoicerCorpName = "공급자 상호",
                                invoicerMgtKey = self.testMgtKey,
                                invoicerCEOName = "공급자 대표자 성명",
                                invoicerAddr = "공급자 주소",
                                invoicerBizClass = "공급자 업종",
                                invoicerBizType = "공급자 업태",
                                invoicerContactName = "공급자 담당자명",
                                invoicerEmail = "test@test.com",
                                invoicerTEL = "070-7510-6766",
                                invoicerHP = '010-1111-2222',
                                invoicerSMSSendYN = False,

                                invoiceeType = '사업자',
                                invoiceeCorpNum = '8888888888',
                                invoiceeCorpName = "공급받는자 상호_#$@#$!<>&_Python_mod",
                                invoiceeMgtKey = None,
                                invoiceeCEOName = "공급받는자 상호",
                                invoiceeAddr = "공급받는자 주소",
                                invoiceeBizClass = "공급받는자 업종",
                                invoiceeBizType = "공급받는자 업태",
                                invoiceeContactName1 = "공급받는자 담당자",
                                invoiceeEmail1 = "test@test.com",
                                invoiceeHP1 = "010-2222-1111",
                                invoiceeFAX1 = "070-7510-6767",

                                supplyCostTotal = "100000",
                                taxTotal = "10000",
                                totalAmount = "110000",

                                modifyCode = None,
                                originalTaxinvoiceKey = None,
                                serialNum = '123',
                                cash = '',
                                chkBill = None,
                                credit = '',
                                remark1 = '비고1',
                                remark2 = '비고2',
                                remark3 = '비고3',
                                kwon = 1,
                                ho = 2,

                                businessLicenseYN  = False,
                                bankBookYN = False,

                                detailList = [
                                                TaxinvoiceDetail(serialNum = 1,
                                                                 purchaseDT = '20150121',
                                                                 itemName="품목1",
                                                                 spec = '규격',
                                                                 qty = 1,
                                                                 unitCost = '100000',
                                                                 supplyCost = '100000',
                                                                 tax = '10000',
                                                                 remark = '품목비고'),
                                                TaxinvoiceDetail(serialNum = 2,
                                                                 itemName = "품목2")
                                            ],
                                addContactList = [
                                                    Contact(serialNum = 1,
                                                            contactName='추가담당자 성명',
                                                            email='test1@test.com'),
                                                    Contact(serialNum = 2,
                                                            contactName='추가담당자2',
                                                            email='test2@test.com')
                                                ]

                                )

        result = self.taxinvoiceService.update(self.testCorpNum,"SELL",self.testMgtKey,taxinvoice)
        self.assertEqual(result.code,1,"수정 오류 : " + result.message)

    def test_attachFile(self):
        result = self.taxinvoiceService.attachFile(self.testCorpNum,"SELL",self.testMgtKey,"test.jpeg")
        self.assertEqual(result.code,1,"첩부 오류 : " + result.message)

    def test_getInfo(self):
        info = self.taxinvoiceService.getInfo(self.testCorpNum,"SELL","1234")
        self.assertIsNotNone(info.itemKey,"아이템키 확인")

    def test_getDetailInfo(self):
        info = self.taxinvoiceService.getDetailInfo(self.testCorpNum,"SELL","123456789012")
        self.assertIsNotNone(info.invoicerMgtKey,"아이템키 확인")
        self.assertIsNone(info.trusteeCorpNum,"빈값 확인")

    def test_z_delete(self):
        result = self.taxinvoiceService.delete(self.testCorpNum,"SELL",self.testMgtKey)
        self.assertEqual(result.code,1,"삭제 오류 : " + result.message)

    def test_getLogs(self):
        logs = self.taxinvoiceService.getLogs(self.testCorpNum,"SELL","1234")
        print (logs[1].procMemo)
        self.assertGreater(len(logs),0,"로그 갯수 확인")


if __name__ == '__main__':
    unittest.main()
