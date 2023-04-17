import sys
import unittest
from fractions import _ComparableNum
from unittest import main

from popbill.base import PaymentForm, PopbillBase, RefundForm

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.baseService = PopbillBase(
            "TESTER", "SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I="
        )
        self.baseService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_paymentRequest(self):
        CorpNum = "1234567890"
        paymentForm = PaymentForm(
            settlerName="담당자명",
            settlerEmail="test@test.com",
            notifyHP="01022223333",
            paymentName="홍길동",
            settleCost="10000",
        )
        result = self.baseService.paymentRequest(CorpNum, paymentForm)

        print(result)

    def test_paymentRequest_with_UserID(self):
        CorpNum = "1234567890"
        UserID = "testkorea"
        paymentForm = PaymentForm(
            settlerName="담당자명",
            settlerEmail="test@test.com",
            notifyHP="01022223333",
            paymentName="홍길동",
            settleCost="10000",
        )
        result = self.baseService.paymentRequest(CorpNum, paymentForm, UserID)

        print(result)

    def test_GetSettleResult(self):
        test_settle_code = "202303070000000052"
        result = self.baseService.getSettleResult(self.testCorpNum, test_settle_code)
        print(result.__dict__)

    def test_GetUseHistory(self):
        SDate = "20230101"
        EDate = "20230102"
        result = self.baseService.getUseHistory(self.testCorpNum, SDate, EDate)
        print(result)

    def test_GetPaymentHistory(self):
        SDate = "20220101"
        EDate = "20220601"
        result = self.baseService.getPaymentHistory(self.testCorpNum, SDate, EDate)
        print(result)

    def test_Refund(self):
        refundForm = RefundForm(
            contactname="환불신청테스트",
            tel="01077777777",
            requestpoint="10",
            accountbank="국민",
            accountnum="123123123-123",
            accountname="예금주",
            reason="",
        )
        result = self.baseService.refund(self.testCorpNum, refundForm, self.testUserID)
        self.assertTrue(result != None)

    def test_RefundHistory(self):
        result = self.baseService.getRefundHistory(self.testCorpNum)
        self.assertTrue(result != None)

    def test_getBalance(self):
        result = self.baseService.getBalance(self.testCorpNum)
        self.assertTrue(result != None)

    def test_QuitRequest(self):
        # 회원 탈퇴 사유
        QuitReason = "회원 탈퇴 사유입니다"

        result = self.baseService.QuitRequest(
            self.testCorpNum, QuitReason, self.testUserID
        )
        # TODO : 회원 탈퇴 검증 로직 작성

    def test_GetRefundResult(self):
        # 환불 코드 (환불 신청시 반환된 코드)
        RefundCode = ""
        result = self.GetRefundResult(self.testCorpNum, RefundCode, self.testUserID)
        # TODO : 환불 결과 검증 로직 작성

    def test_GetRefundablePoint(self):
        result = self.GetRefundablePoint(self.testCorpNum, self.testUserID)
        # TODO : 환불 가능 포인트 검증 로직 작성


if __name__ == "__main__":
    main()
