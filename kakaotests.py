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


class KakaoServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.kakaoService = KakaoService('TESTER', 'SwWxqU+0TErBXy/9TVjIPEnI0VTUMMSQZtJf3Ed8q3I=')
        self.kakaoService.IsTest = True
        self.testCorpNum = "1234567890"
        self.testUserID = "testkorea"

    def test_getUR_sender(self):
        url = self.kakaoService.getURL(self.testCorpNum, self.testUserID, "SENDER")
        print(url)

    def test_getUR_plusfriend(self):
        url = self.kakaoService.getURL(self.testCorpNum, self.testUserID, "PLUSFRIEND")
        print(url)

    def test_getUR_template(self):
        url = self.kakaoService.getURL(self.testCorpNum, self.testUserID, "TEMPLATE")
        print(url)

    def test_getUR_box(self):
        url = self.kakaoService.getURL(self.testCorpNum, self.testUserID, "BOX")
        print(url)

    def test_listPlusFriendID(self):
        response = self.kakaoService.listPlusFriendID(self.testCorpNum, self.testUserID)

        i = 1
        for info in response:
            print("====== 플러시친구 목록 확인 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

    def test_checkSenderNumber(self):
        try:
            SenderNumber = ""
            response = self.kakaoService.checkSenderNumber(self.testCorpNum, SenderNumber)
            print(response)
        except PopbillException as PE:
            print(PE.message)

    def test_getSenderNumberList(self):
        response = self.kakaoService.getSenderNumberList(self.testCorpNum, self.testUserID)

        i = 1
        for info in response:
            print("====== 발신번호 목록 확인 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

    def test_listATSTemplate(self):
        response = self.kakaoService.listATSTemplate(self.testCorpNum, self.testUserID)

        i = 1
        for info in response:
            print("====== 알림톡 템플릿 목록 확인 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

    def test_sendATS(self):
        TemplateCode = "019020000163"
        Sender = ""
        Content = "[ 팝빌 ]\n"
        Content += "신청하신 #{템플릿코드}에 대한 심사가 완료되어 승인 처리되었습니다.\n"
        Content += "해당 템플릿으로 전송 가능합니다.\n\n"
        Content += "문의사항 있으시면 파트너센터로 편하게 연락주시기 바랍니다.\n\n"
        Content += "팝빌 파트너센터 : 1600-8536\n"
        Content += "support@linkhub.co.kr"
        AltContent = "알림톡 대체 문자"
        AltSendType = "C"
        SndDT = ""
        Receiver = ""
        ReceiverName = ""

        KakaoButtons = []
        KakaoButtons.append(
            KakaoButton(
                n="웹링크",
                t="WL",
                u1="https://www.popbill.com",
                u2="http://www.popbill.com"
            )
        )

        try:
            receiptNum = self.kakaoService.sendATS(self.testCorpNum, TemplateCode, Sender, Content, AltContent,
                                                   AltSendType, SndDT, Receiver, ReceiverName, self.testUserID,
                                                   "", KakaoButtons)
            print("접수번호 (receiptNum) : %s" % receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_sendATS_multi(self):
        TemplateCode = "019020000163"
        Sender = ""
        Content = "[ 팝빌 ]\n"
        Content += "신청하신 #{템플릿코드}에 대한 심사가 완료되어 승인 처리되었습니다.\n"
        Content += "해당 템플릿으로 전송 가능합니다.\n\n"
        Content += "문의사항 있으시면 파트너센터로 편하게 연락주시기 바랍니다.\n\n"
        Content += "팝빌 파트너센터 : 1600-8536\n"
        Content += "support@linkhub.co.kr"

        AltContent = "알림톡 대체 문자"
        AltSendType = ""
        SndDT = ""

        KakaoMessages = []
        for x in range(0, 1):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",
                    rcvnm="linkhub",
                    msg=Content,
                    altmsg="알림톡 우선순위 대체문자"
                )
            )

        KakaoButtons = []
        KakaoButtons.append(
            KakaoButton(
                n="웹링크",
                t="WL",
                u1="https://www.popbill.com",
                u2="http://www.popbill.com"
            )
        )
        try:
            receiptNum = self.kakaoService.sendATS_multi(self.testCorpNum, TemplateCode, Sender, "", "",
                                                         AltSendType, SndDT, KakaoMessages, self.testUserID,
                                                         "", KakaoButtons)
            print("접수번호 (receiptNum) : %s" % receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_sendFTS(self):
        PlusFriendID = "@팝빌"
        Sender = ""
        Content = "친구톡 내용"
        AltContent = "대체문자 내용"
        AltSendType = "A"
        SndDT = ""
        Receiver = ""
        ReceiverName = ""

        KakaoButtons = []
        for x in range(0, 1):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",
                    t="WL",
                    u1="http://www.popbill.com",
                    u2="http://www.popbill.com"
                )
            )

        KakaoButtons.append(
            KakaoButton(
                n="앱링크",
                t="AL",
                u1="http://www.popbill.com",
                u2="http://www.popbill.com"
            )
        )

        AdsYN = False

        try:
            receiptNum = self.kakaoService.sendFTS(self.testCorpNum, PlusFriendID, Sender, Content, AltContent,
                                                   AltSendType, SndDT, Receiver, ReceiverName, KakaoButtons, AdsYN,
                                                   self.testUserID, "")
            print("접수번호 (receiptNum) : %s" % receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_sendFTS_multi(self):
        PlusFriendID = "@팝빌"
        Sender = ""
        Content = "친구톡 내용"
        AltContent = "대체문자 내용"
        AltSendType = "A"
        SndDT = ""

        KakaoMessages = []
        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",
                    rcvnm="",
                    msg="친구톡 우선순위 내용",
                    altmsg="대체문자 우선순위 내용"
                )
            )

        KakaoButtons = []
        for x in range(0, 1):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",
                    t="MD",
                    u1="http://www.popbill.com",
                    u2="http://www.popbill.com"
                )
            )

        AdsYN = False

        try:
            receiptNum = self.kakaoService.sendFTS_same(self.testCorpNum, PlusFriendID, Sender, "", "",
                                                        AltSendType, SndDT, KakaoMessages, KakaoButtons, AdsYN,
                                                        self.testUserID, "20180809150622")
            print("접수번호 (receiptNum) : %s" % receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_sendFMS(self):
        PlusFriendID = "@팝빌"
        Sender = ""
        Content = "플러스친구 내용"
        AltContent = "플러스친구등록이 안되어있습니다. 대체문자로 전송됩니다."
        AltSendType = "A"
        SndDT = "20180301003000"
        FilePath = "FMSImage.jpg"
        ImageURL = "http://www.linkhub.co.kr"
        Receiver = ""
        ReceiverName = None

        KakaoButtons = []

        KakaoButtons.append(
            KakaoButton(
                n="팝빌 바로가기",
                t="WL",
                u1="http://www.popbill.com",
                u2="http://www.popbill.com"
            )
        )
        KakaoButtons.append(
            KakaoButton(
                n="링크허브 바로가기",
                t="WL",
                u1="http://www.linkhub.co.kr",
                u2="http://www.linkhub.co.kr"
            )
        )
        KakaoButtons.append(
            KakaoButton(
                n="메시지전달",
                t="MD",
            )
        )
        KakaoButtons.append(
            KakaoButton(
                n="봇키워드",
                t="BK",
            )
        )

        AdsYN = False

        try:
            receiptNum = self.kakaoService.sendFMS(self.testCorpNum, PlusFriendID, Sender, Content, AltContent,
                                                   AltSendType, SndDT, FilePath, ImageURL, Receiver, ReceiverName,
                                                   KakaoButtons, AdsYN, self.testUserID, "20180809150651")
            print("접수번호 (receiptNum) : %s" % receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_sendFMS_multi(self):
        PlusFriendID = "@팝빌"
        Sender = ""
        Content = "친구톡 내용"
        AltContent = "대체문자 내용"
        AltSendType = "A"
        SndDT = "20180810151226"
        FilePath = "FMSImage.jpg"
        ImageURL = "http://www.linkhub.co.kr"

        KakaoMessages = []
        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",
                    rcvnm="",
                    msg="친구톡 우선순위 내용",
                    altmsg="대체문자 우선순위 내용"
                )
            )

        for x in range(0, 2):
            KakaoMessages.append(
                KakaoReceiver(
                    rcv="",
                    rcvnm="",
                )
            )

        KakaoButtons = []
        for x in range(0, 5):
            KakaoButtons.append(
                KakaoButton(
                    n="팝빌 바로가기",
                    t="WL",
                    u1="http://www.popbill.com",
                    u2="http://www.popbill.com"
                )
            )

        AdsYN = False

        try:
            receiptNum = self.kakaoService.sendFMS_multi(self.testCorpNum, PlusFriendID, Sender, Content, AltContent,
                                                         AltSendType, SndDT, FilePath, ImageURL, KakaoMessages,
                                                         KakaoButtons, AdsYN, self.testUserID, "20180809151234")
            print("접수번호 (receiptNum) : %s" % receiptNum)
        except PopbillException as PE:
            print(PE.message)

    def test_cancelReserve(self):
        ReceiptNum = "018022814545600001"
        result = self.kakaoService.cancelReserve(self.testCorpNum, ReceiptNum, self.testUserID)
        print(result.code)
        print(result.message)

    def test_cancelReserveRN(self):
        RequestNum = "20180809151234"
        result = self.kakaoService.cancelReserveRN(self.testCorpNum, RequestNum, self.testUserID)
        print(result.code)
        print(result.message)

    def test_getMessage(self):
        ReceipNum = "018022815501800001"
        response = self.kakaoService.getMessages(self.testCorpNum, ReceipNum, self.testUserID)

        print("contentType (카카오톡 유형): %s " % response.contentType)
        print("templateCode (템플릿코드): %s " % response.templateCode)
        print("plusFriendID (플러스친구 아이디): %s " % response.plusFriendID)
        print("sendNum (발신번호): %s " % response.sendNum)
        print("altContent ([동보] 대체문자 내용): %s " % response.altContent)
        print("altSendType (대체문자 유형): %s " % response.sndDT)
        print("reserveDT (예약일시): %s " % response.reserveDT)
        print("adsYN (광고여부): %s " % response.adsYN)
        print("successCnt (성공건수): %s " % response.successCnt)
        print("failCnt (실패건수): %s " % response.failCnt)
        print("altCnt (대체문자 건수): %s " % response.altCnt)
        print("cancelCnt (취소건수): %s " % response.cancelCnt)
        print("adsYN (광고전송 여부): %s " % response.adsYN)
        print

        i = 1
        for info in response.msgs:
            print("====== 전송결과 정보 배열 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

        i = 1
        for info in response.btns:
            print("====== 버튼 목록 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

    def test_getMessageRN(self):
        RequestNum = "20180809151234"
        response = self.kakaoService.getMessagesRN(self.testCorpNum, RequestNum, self.testUserID)

        print("contentType (카카오톡 유형): %s " % response.contentType)
        print("templateCode (템플릿코드): %s " % response.templateCode)
        print("plusFriendID (플러스친구 아이디): %s " % response.plusFriendID)
        print("sendNum (발신번호): %s " % response.sendNum)
        print("altContent ([동보] 대체문자 내용): %s " % response.altContent)
        print("altSendType (대체문자 유형): %s " % response.sndDT)
        print("reserveDT (예약일시): %s " % response.reserveDT)
        print("adsYN (광고여부): %s " % response.adsYN)
        print("successCnt (성공건수): %s " % response.successCnt)
        print("failCnt (실패건수): %s " % response.failCnt)
        print("altCnt (대체문자 건수): %s " % response.altCnt)
        print("cancelCnt (취소건수): %s " % response.cancelCnt)
        print("adsYN (광고전송 여부): %s " % response.adsYN)
        print

        i = 1
        for info in response.msgs:
            print("====== 전송결과 정보 배열 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

        i = 1
        for info in response.btns:
            print("====== 버튼 목록 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

    def test_search(self):
        SDate = "20180901"
        EDate = "20181008"
        State = ['1', '2', '3', '4', '5']
        Item = ['ATS', 'FTS', 'FMS']
        ReserveYN = ''
        SenderYN = '0'
        Page = 1
        PerPage = 10
        Order = "D"
        QString = ""

        response = self.kakaoService.search(self.testCorpNum, SDate, EDate, State, Item, ReserveYN, SenderYN, Page,
                                            PerPage, Order, self.testUserID, QString)

        print("code (응답코드) : %s " % response.code)
        print("message (응답메시지) : %s " % response.message)
        print("total (검색결과 건수) : %s " % response.total)
        print("perPage (페이지당 검색개수) : %s " % response.perPage)
        print("pageNum (페에지 번호) : %s " % response.pageNum)
        print("pageCount (페이지 개수) : %s \n" % response.pageCount)
        print

        i = 1
        for info in response.list:
            print("====== 전송내역 목록 조회 [%d] ======" % i)
            for key, value in info.__dict__.items():
                print("%s : %s" % (key, value))
            i += 1
            print

    def test_getUnitCost(self):
        unitCost = self.kakaoService.getUnitCost(self.testCorpNum, "FTS")
        print(unitCost)
        self.assertGreaterEqual(unitCost, 0, "단가는 0 이상.")

    def test_getChargeInfo(self):
        chrgInfo = self.kakaoService.getChargeInfo(self.testCorpNum, "FTS", self.testUserID)
        print(chrgInfo.unitCost)
        print(chrgInfo.chargeMethod)
        print(chrgInfo.rateSystem)

    def test_getPlusFriendMgtURL(self):
        response = self.kakaoService.getPlusFriendMgtURL(self.testCorpNum, self.testUserID)
        print response

    def test_getSenderNumberMgtURL(self):
        response = self.kakaoService.getSenderNumberMgtURL(self.testCorpNum, self.testUserID)
        print response

    def test_getATSTemplateMgtURL(self):
        response = self.kakaoService.getATSTemplateMgtURL(self.testCorpNum, self.testUserID)
        print response

    def test_getSentListURL(self):
        response = self.kakaoService.getSentListURL(self.testCorpNum, self.testUserID)
        print response


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KakaoServiceTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
