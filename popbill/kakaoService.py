# -*- coding: utf-8 -*-
# Module for Popbill Kakao API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Kim Hyunjin (code@linkhubcorp.com)
# Written : 2018-02-26
# Updated : 2025-01-20
# Thanks for your interest.
from .base import File, PopbillBase, PopbillException, Response

try:
    from urllib import parse as parse
except ImportError:
    import urllib as parse


class KakaoService(PopbillBase):
    """팝빌 카카오톡 API Service Implementation."""

    def __init__(self, LinkID, SecretKey):
        """
        생성자
        :param LinkID: 링크허브에서 발급받은 링크아이디
        :param SecretKey: 링크허브에서 발급받은 비밀키
        """
        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("153")
        self._addScope("154")
        self._addScope("155")

    def getURL(self, CorpNum, UserID, ToGo):
        """
        :param CorpNum: 팝빌회원 사업자번호
        :param UserID: 팝빌회원 아이디
        :param ToGo: [PLUSFRIEND-카카오톡채널관리, SENDER-발신번호관리, TEMPLATE-알림톡템플릿관리, BOX-카카오톡전송내용]
        :return: 팝빌 URL
        """
        if ToGo == None or ToGo == "":
            raise PopbillException(-99999999, "TOGO값이 입력되지 않았습니다.")

        if ToGo == "SENDER":
            result = self._httpget("/Message/?TG=" + ToGo, CorpNum, UserID)
        else:
            result = self._httpget("/KakaoTalk/?TG=" + ToGo, CorpNum, UserID)
        return result.url

    def getPlusFriendMgtURL(self, CorpNum, UserID):
        """
        카카오톡 채널 관리 팝업 URL
        :param CorpNum: 팝빌회원 사업자번호
        :param UserID: 팝빌회원 아이디
        :return: 팝빌 URL
        """
        result = self._httpget("/KakaoTalk/?TG=PLUSFRIEND", CorpNum, UserID)
        return result.url

    def getSenderNumberMgtURL(self, CorpNum, UserID):
        """
        발신번호 관리 팝업 URL
        :param CorpNum: 팝빌회원 사업자번호
        :param UserID: 팝빌회원 아이디
        :return: 팝빌 URL
        """
        result = self._httpget("/Message/?TG=SENDER", CorpNum, UserID)
        return result.url

    def getATSTemplateMgtURL(self, CorpNum, UserID):
        """
        알림톡 템플릿관리 팝업 URL
        :param CorpNum: 팝빌회원 사업자번호
        :param UserID: 팝빌회원 아이디
        :return: 팝빌 URL
        """
        result = self._httpget("/KakaoTalk/?TG=TEMPLATE", CorpNum, UserID)
        return result.url

    def getSentListURL(self, CorpNum, UserID):
        """
        카카오톡 전송내역 팝업 URL
        :param CorpNum: 팝빌회원 사업자번호
        :param UserID: 팝빌회원 아이디
        :return: 팝빌 URL
        """
        result = self._httpget("/KakaoTalk/?TG=BOX", CorpNum, UserID)
        return result.url

    def listPlusFriendID(self, CorpNum, UserID=None):
        """
        카카오톡 채널 목록 확인
        :param CorpNum: 팝빌회원 사업자번호
        :param UserID: 팝빌회원 아이디
        :return: 카카오톡 채널 list
        """
        return self._httpget("/KakaoTalk/ListPlusFriendID", CorpNum, UserID)

    def checkSenderNumber(self, CorpNum, SenderNumber, UserID=None):
        """발신번호 등록여부 확인
        args
            CorpNum : 회원 사업자번호
            SenderNumber : 확인할 발신번호
            UserID  : 회원 팝빌아이디
        return
            처리결과. consist of code and message
        raise
            PopbillException
        """

        return self._httpget(
            "/KakaoTalk/CheckSenderNumber/" + SenderNumber, CorpNum, UserID
        )

    def getSenderNumberList(self, CorpNum, UserID=None):
        """
        발신번호 목록 확인
        :param CorpNum: 팝빌회원 사업자번호
        :param UserID: 팝빌회원 아이디
        :return: 발신번호목록 list
        """
        return self._httpget("/Message/SenderNumber", CorpNum, UserID)

    def getATSTemplate(self, CorpNum, templateCode, UserID=None):
        """
        알림톡 템플릿 정보 확인
        :param CorpNum: 팝빌회원 사업자번호
        :param templateCode: 알림톡 템플릿 코드
        :param UserID: 팝빌회원 아이디
        :return: templateCode (템플릿 코드), templateName (템플릿 이름), template (템플릿 내용), plusFriendID (채널 이름),
                 secureYN (보안템플릿 여부),  state (템플릿 상태), stateDT (템플릿 상태 일시)
        """
        if templateCode == None or templateCode == "":
            raise PopbillException(-99999999, "템플릿 코드가 입력되지 않았습니다.")

        result = self._httpget(
            "/KakaoTalk/GetATSTemplate/" + templateCode, CorpNum, UserID
        )
        return result

    def listATSTemplate(self, CorpNum, UserID=None):
        """
        알림톡 템플릿 목록 확인
        :param CorpNum: 팝빌회원 사업자번호
        :param UserID: 팝빌회원 아이디
        :return: 알림톡 템플릿 list
        """
        return self._httpget("/KakaoTalk/ListATSTemplate", CorpNum, UserID)

    def sendATS(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        Receiver,
        ReceiverName,
        UserID=None,
        RequestNum=None,
    ):

        KakaoMessages = []
        KakaoMessages.append(
            KakaoReceiver(
                rcv=Receiver, rcvnm=ReceiverName, msg=Content, altmsg=AltContent
            )
        )
        return self.sendATS_same(
            CorpNum,
            TemplateCode,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            UserID,
            RequestNum,
        )

    # 버튼 추가
    def sendATS(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        Receiver,
        ReceiverName,
        UserID=None,
        RequestNum=None,
        ButtonList=None,
    ):

        KakaoMessages = []
        KakaoMessages.append(
            KakaoReceiver(
                rcv=Receiver, rcvnm=ReceiverName, msg=Content, altmsg=AltContent
            )
        )
        return self.sendATS_same(
            CorpNum,
            TemplateCode,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            UserID,
            RequestNum,
            ButtonList,
        )

    # 대체문자 제목 추가
    def sendATS(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        Receiver,
        ReceiverName,
        UserID=None,
        RequestNum=None,
        ButtonList=None,
        AltSubject=None,
    ):

        KakaoMessages = []
        KakaoMessages.append(
            KakaoReceiver(
                rcv=Receiver,
                rcvnm=ReceiverName,
                msg=Content,
                altsjt=AltSubject,
                altmsg=AltContent,
            )
        )
        return self.sendATS_same(
            CorpNum,
            TemplateCode,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            UserID,
            RequestNum,
            ButtonList,
            "",
        )

    def sendATS_multi(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        UserID=None,
        RequestNum=None,
    ):
        return self.sendATS_same(
            CorpNum,
            TemplateCode,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            UserID,
            RequestNum,
        )

    # 버튼 추가

    def sendATS_multi(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        UserID=None,
        RequestNum=None,
        ButtonList=None,
    ):
        return self.sendATS_same(
            CorpNum,
            TemplateCode,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            UserID,
            RequestNum,
            ButtonList,
        )

    # 대체문자 제목 추가
    def sendATS_multi(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        UserID=None,
        RequestNum=None,
        ButtonList=None,
        AltSubject=None,
    ):
        return self.sendATS_same(
            CorpNum,
            TemplateCode,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            UserID,
            RequestNum,
            ButtonList,
            AltSubject,
        )

    def sendATS_same(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        UserID=None,
        RequestNum=None,
    ):
        return self.sendATS_same(
            CorpNum,
            TemplateCode,
            Sender,
            Content,
            AltContent,
            AltSendType,
            SndDT,
            KakaoMessages,
            UserID,
            RequestNum,
            None,
            None,
        )

    # 버튼 추가
    def sendATS_same(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        UserID=None,
        RequestNum=None,
        ButtonList=None,
    ):
        return self.sendATS_same(
            CorpNum,
            TemplateCode,
            Sender,
            Content,
            AltContent,
            AltSendType,
            SndDT,
            KakaoMessages,
            UserID,
            RequestNum,
            None,
            None,
        )

    # 대체문자 제목 추가
    def sendATS_same(
        self,
        CorpNum,
        TemplateCode,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        UserID=None,
        RequestNum=None,
        ButtonList=None,
        AltSubject=None,
    ):
        """
        알림톡 대량 전송
        :param CorpNum: 팝빌회원 사업자번호
        :param TemplateCode: 템플릿코드
        :param Sender: 발신번호
        :param Content: [동보] 알림톡 내용
        :param AltContent: [동보] 대체문자 내용
        :param AltSendType: 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        :param SndDT: 예약일시 [작성형식 : yyyyMMddHHmmss]
        :param KakaoMessages: 알림톡 내용 (배열)
        :param UserID: 팝빌회원 아이디
        :param RequestNum : 요청번호
        :param ButtonList : 버튼 (배열)
        :param AltSubject : 대체문자 제목
        :return: receiptNum (접수번호)
        """
        if TemplateCode is None or TemplateCode == "":
            raise PopbillException(-99999999, "알림톡 템플릿코드가 입력되지 않았습니다.")

        req = {}

        if TemplateCode is not None or TemplateCode != "":
            req["templateCode"] = TemplateCode
        if Sender is not None or Sender != "":
            req["snd"] = Sender
        if Content is not None or Content != "":
            req["content"] = Content
        if AltSubject is not None or AltSubject != "":
            req["altSubject"] = AltSubject
        if AltContent is not None or AltContent != "":
            req["altContent"] = AltContent
        if AltSendType is not None or AltSendType != "":
            req["altSendType"] = AltSendType
        if SndDT is not None or SndDT != "":
            req["sndDT"] = SndDT
        if KakaoMessages is not None or KakaoMessages != "":
            req["msgs"] = KakaoMessages
        if ButtonList is not None:
            req["btns"] = ButtonList
        if RequestNum is not None or RequestNum != "":
            req["requestnum"] = RequestNum

        postData = self._stringtify(req)

        result = self._httppost("/ATS", postData, CorpNum, UserID)

        return result.receiptNum

    def sendFTS(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        Receiver,
        ReceiverName,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
    ):
        KakaoMessages = []
        KakaoMessages.append(
            KakaoReceiver(
                rcv=Receiver, rcvnm=ReceiverName, msg=Content, altmsg=AltContent
            )
        )

        return self.sendFTS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
        )

    # 대체문자 제목 추가
    def sendFTS(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        Receiver,
        ReceiverName,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
        AltSubject=None,
    ):
        KakaoMessages = []
        KakaoMessages.append(
            KakaoReceiver(
                rcv=Receiver,
                rcvnm=ReceiverName,
                msg=Content,
                altsjt=AltSubject,
                altmsg=AltContent,
            )
        )

        return self.sendFTS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
            "",
        )

    def sendFTS_multi(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
    ):
        return self.sendFTS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
        )

    # 대체문자 제목 추가
    def sendFTS_multi(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
        AltSubject=None,
    ):
        return self.sendFTS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
            AltSubject,
        )

    def sendFTS_same(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
    ):
        return self.sendFTS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
            None,
        )

    # 대체문자 제목 추가
    def sendFTS_same(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
        AltSubject=None,
    ):
        """
        친구톡 텍스트 대량 전송
        :param CorpNum: 팝빌회원 사업자번호
        :param PlusFriendID: 검색용 아이디
        :param Sender: 발신번호
        :param Content: [동보] 친구톡 내용
        :param AltContent: [동보] 대체문자 내용
        :param AltSendType: 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        :param SndDT: 예약일시 [작성형식 : yyyyMMddHHmmss]
        :param KakaoMessages: 친구톡 내용 (배열)
        :param KakaoButtons: 버튼 목록 (최대 5개)
        :param AdsYN: 광고 전송여부
        :param UserID: 팝빌회원 아이디
        :param RequestNum : 요청번호
        :param AltSubject : 대체문자 제목
        :return: receiptNum (접수번호)
        """
        if PlusFriendID is None or PlusFriendID == "":
            raise PopbillException(-99999999, "검색용 아이디가 입력되지 않았습니다.")

        req = {}
        if PlusFriendID is not None or PlusFriendID != "":
            req["plusFriendID"] = PlusFriendID
        if Sender is not None or Sender != "":
            req["snd"] = Sender
        if AltSendType is not None or AltSendType != "":
            req["altSendType"] = AltSendType
        if Content is not None or Content != "":
            req["content"] = Content
        if AltSubject is not None or AltSubject != "":
            req["altSubject"] = AltSubject
        if AltContent is not None or AltContent != "":
            req["altContent"] = AltContent
        if SndDT is not None or SndDT != "":
            req["sndDT"] = SndDT
        if KakaoMessages:
            req["msgs"] = KakaoMessages
        if KakaoButtons:
            req["btns"] = KakaoButtons
        if AdsYN:
            req["adsYN"] = True
        if RequestNum is not None or RequestNum != "":
            req["requestNum"] = RequestNum

        postData = self._stringtify(req)

        result = self._httppost("/FTS", postData, CorpNum, UserID)

        return result.receiptNum

    def sendFMS(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FilePath,
        ImageURL,
        Receiver,
        ReceiverName,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
    ):

        KakaoMessages = []
        KakaoMessages.append(
            KakaoReceiver(
                rcv=Receiver, rcvnm=ReceiverName, msg=Content, altmsg=AltContent
            )
        )

        return self.sendFMS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            FilePath,
            ImageURL,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
        )

    # 대체문자 제목 추가
    def sendFMS(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FilePath,
        ImageURL,
        Receiver,
        ReceiverName,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
        AltSubject=None,
    ):

        KakaoMessages = []
        KakaoMessages.append(
            KakaoReceiver(
                rcv=Receiver,
                rcvnm=ReceiverName,
                msg=Content,
                altsjt=AltSubject,
                altmsg=AltContent,
            )
        )

        return self.sendFMS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            FilePath,
            ImageURL,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
            "",
        )

    def sendFMS_multi(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FilePath,
        ImageURL,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
    ):
        return self.sendFMS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            FilePath,
            ImageURL,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
        )

    # 대체문자 제목 추가
    def sendFMS_multi(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FilePath,
        ImageURL,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
        AltSubject=None,
    ):
        return self.sendFMS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            FilePath,
            ImageURL,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
            None,
        )

    def sendFMS_same(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FilePath,
        ImageURL,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
    ):
        return self.sendFMS_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            FilePath,
            ImageURL,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
            None,
        )

    # 대체문자 제목 추가
    def sendFMS_same(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FilePath,
        ImageURL,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
        AltSubject=None,
    ):
        """
        친구톡 이미지 대량 전송
        :param CorpNum: 팝빌회원 사업자번호
        :param PlusFriendID: 검색용 아이디
        :param Sender: 발신번호
        :param Content: [동보] 친구톡 내용
        :param AltContent: [동보] 대체문자 내용
        :param AltSendType: 대체문자 유형 [공백-미전송, C-알림톡내용, A-대체문자내용]
        :param SndDT: 예약일시 [작성형식 : yyyyMMddHHmmss]
        :param FilePath: 파일경로
        :param ImageURL: 이미지URL
        :param KakaoMessages: 친구톡 내용 (배열)
        :param KakaoButtons: 버튼 목록 (최대 5개)
        :param AdsYN: 광고 전송여부
        :param UserID: 팝빌회원 아이디
        :param RequestNum : 요청번호
        :param AltSubject : 대체문자 제목
        :return: receiptNum (접수번호)
        """
        if PlusFriendID is None or PlusFriendID == "":
            raise PopbillException(-99999999, "검색용 아이디가 입력되지 않았습니다.")

        req = {}
        if PlusFriendID is not None or PlusFriendID != "":
            req["plusFriendID"] = PlusFriendID
        if Sender is not None or Sender != "":
            req["snd"] = Sender
        if Content is not None or Content != "":
            req["content"] = Content
        if AltSubject is not None or AltSubject != "":
            req["altSubject"] = AltSubject
        if AltContent is not None or AltContent != "":
            req["altContent"] = AltContent
        if AltSendType is not None or AltSendType != "":
            req["altSendType"] = AltSendType
        if SndDT is not None or SndDT != "":
            req["sndDT"] = SndDT
        if KakaoMessages is not None or KakaoMessages != "":
            req["msgs"] = KakaoMessages
        if ImageURL is not None or ImageURL != "":
            req["imageURL"] = ImageURL
        if KakaoButtons:
            req["btns"] = KakaoButtons
        if AdsYN:
            req["adsYN"] = True
        if RequestNum is not None or RequestNum != "":
            req["requestNum"] = RequestNum

        postData = self._stringtify(req)

        files = []
        try:
            with open(FilePath, "rb") as F:
                files = [File(fieldName="file", fileName=F.name, fileData=F.read())]
        except IOError:
            raise PopbillException(-99999999, "해당경로에 파일이 없거나 읽을 수 없습니다.")

        result = self._httppost_files("/FMS", postData, files, CorpNum, UserID)

        return result.receiptNum

    def cancelReserve(self, CorpNum, ReceiptNum, UserID=None):
        """
        예약전송 취소
        :param CorpNum: 팝빌회원 사업자번호
        :param ReceiptNum: 접수번호
        :param UserID: 팝빌회원 아이디
        :return: code (요청에 대한 상태 응답코드), message (요청에 대한 응답 메시지)
        """
        if ReceiptNum == None or len(ReceiptNum) != 18:
            raise PopbillException(-99999999, "접수번호가 올바르지 않습니다.")

        return self._httpget("/KakaoTalk/" + ReceiptNum + "/Cancel", CorpNum, UserID)

    def cancelReserveRN(self, CorpNum, RequestNum, UserID=None):
        """
        예약전송 취소
        :param CorpNum: 팝빌회원 사업자번호
        :param RequestNum: 전송요청시 할당한 전송요청번호
        :param UserID: 팝빌회원 아이디
        :return: code (요청에 대한 상태 응답코드), message (요청에 대한 응답 메시지)
        """
        if RequestNum is None or RequestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다")

        response = self._httpget("/KakaoTalk/Cancel/" + RequestNum, CorpNum, UserID)
        return Response(**response.__dict__)

    def getMessages(self, CorpNum, ReceiptNum, UserID=None):
        """
        알림톡/친구톡 전송내역 확인
        :param CorpNum: 팝빌회원 사업자번호
        :param ReceiptNum: 접수번호
        :param UserID: 팝빌회원 아이디
        :return: 알림톡/친구톡 전송내역 및 전송상태
        """
        if ReceiptNum == None or len(ReceiptNum) != 18:
            raise PopbillException(-99999999, "접수번호가 올바르지 않습니다.")

        return self._httpget("/KakaoTalk/" + ReceiptNum, CorpNum, UserID)

    def getMessagesRN(self, CorpNum, RequestNum, UserID=None):
        """
        알림톡/친구톡 전송내역 확인
        :param CorpNum: 팝빌회원 사업자번호
        :param RequestNum: 전송요청시 할당한 전송요청번호
        :param UserID: 팝빌회원 아이디
        :return: 알림톡/친구톡 전송내역 및 전송상태
        """
        if RequestNum is None or RequestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        return self._httpget("/KakaoTalk/Get/" + RequestNum, CorpNum, UserID)

    def search(
        self,
        CorpNum,
        SDate,
        EDate,
        State,
        Item,
        ReserveYN,
        SenderYN,
        Page,
        PerPage,
        Order,
        UserID=None,
        QString=None,
    ):
        """
        카카오톡 전송내역 목록을 조회한다.
        - 버튼정보를 확인하는 경우 GetMessages (알림톡/친구톡 전송내역 확인) API 사용
        :param CorpNum: 팝빌팝빌회원 사업자번호
        :param SDate: 시작일자, 표시형식(yyyyMMdd)
        :param EDate: 종료일자, 표시형식(yyyyMMdd)
        :param State: 전송상태 배열 [1-대기, 2-성공, 3-실패, 4-취소]
        :param Item: 검색대상 [SMS-단문, LMS-장문, MMS-포토]
        :param ReserveYN: 예약여부 [0-전체조회, 1-예약전송]
        :param SenderYN: 개인조회 여부 [0-전체조회, 1-개인조회]
        :param Page: 페이지번호
        :param PerPage: 페이지당 목록개수
        :param Order: 정렬방향, [D-내림차순, A-오름차순]
        :param UserID: 팝빌 회원아이디
        :param QString : 조회 검색어, 수신자명 기재
        :return: 알림톡/친구톡 전송내역 및 전송상태 및 검색결과 조회
        """

        if SDate == None or SDate == "":
            raise PopbillException(-99999999, "시작일자가 입력되지 않았습니다.")

        if EDate == None or EDate == "":
            raise PopbillException(-99999999, "종료일자가 입력되지 않았습니다.")

        if State == None or len(State) < 1:
            raise PopbillException(-99999999, "전송상태가 입력되지 않았습니다.") 

        uri = "/KakaoTalk/Search"
        uri += "?SDate=" + SDate
        uri += "&EDate=" + EDate
        uri += "&State=" + ",".join(State)
        
        if Item is not None and len(Item) > 0:
            uri += "&Item=" + ",".join(Item)
        if ReserveYN is not None and ReserveYN != "":
            uri += "&ReserveYN=" + ReserveYN
        if SenderYN is not None:
            uri += "&SenderOnly=" + str(SenderYN)
        if Page is not None and Page > 0:
            uri += "&Page=" + str(Page)
        if PerPage is not None and (PerPage > 0 and PerPage <= 1000):    
            uri += "&PerPage=" + str(PerPage)
        if Order is not None and Order != "":    
            uri += "&Order=" + Order
        if QString is not None and QString != "":
            uri += "&QString=" + parse.quote(QString)

        return self._httpget(uri, CorpNum, UserID)

    def getUnitCost(self, CorpNum, MsgType, UserID=None):
        """
        전송단가 확인
        :param CorpNum: 팝빌회원 사업자번호
        :param MsgType: 카카오톡 유형
        :param UserID: 팝빌 회원아이디
        :return: unitCost
        """
        if MsgType is None or MsgType == "":
            raise PopbillException(-99999999, "전송유형이 입력되지 않았습니다.")

        result = self._httpget("/KakaoTalk/UnitCost?Type=" + MsgType, CorpNum)
        return float(result.unitCost)

    def getChargeInfo(self, CorpNum, MsgType, UserID=None):
        """
        서비스 과금정보를 확인한다.
        :param CorpNum: 팝빌회원 사업자번호
        :param MsgType: 카카오톡 유형
        :param UserID: 팝빌 회원아이디
        :return: unitCost, chargeMethod, rateSystem
        """
        return self._httpget("/KakaoTalk/ChargeInfo?Type=" + MsgType, CorpNum, UserID)

    def CancelReserveRNbyRCV(self, CorpNum, requestNum, receiveNum, UserID=None):
        """예약 메시지 전송 취소. 예약시간 기준 10분전의 건만 취소 가능

        Args:
            CorpNum (str): 연동회원 사업자번호
            receiptNum (str): 전송시 접수 번호
            receiveNum (str): 전송시 수신 번호
            UserID (str): 연동회원 아이디

        Raises:
        PopbillException
        """
        if requestNum == None or requestNum == "":
            raise PopbillException(-99999999, "전송요청번호가 입력되지 않았습니다.")
        if receiveNum == None or receiveNum == "":
            raise PopbillException(-99999999, "수신번호가 입력되지 않았습니다.")

        postData = self._stringtify(receiveNum)

        response = self._httppost(
            "/KakaoTalk/Cancel/" + requestNum, postData, CorpNum, UserID
        )
        return Response(response)

    def CancelReservebyRCV(self, CorpNum, receiptNum, receiveNum, UserID=None):
        """예약 메시지 전송 취소. 예약시간 기준 10분전의 건만 취소 가능

        Args:
            CorpNum (str): 연동회원 사업자번호
            receiptNum (str): 전송시 접수 번호
            receiveNum (str): 전송시 수신 번호
            UserID (str): 연동회원 아이디

        Returns:

        Raises:
        PopbillException
        """

        if receiptNum == None or receiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")
        if receiveNum == None or receiveNum == "":
            raise PopbillException(-99999999, "수신번호가 입력되지 않았습니다.")

        postData = self._stringtify(receiveNum)
        resposne = self._httppost(
            "/KakaoTalk/" + receiptNum + "/Cancel", postData, CorpNum, UserID
        )
        return Response(resposne)


class KakaoReceiver(object):
    def __init__(self, **kwargs):
        self.__dict__ = dict.fromkeys(
            ["rcv", "rcvnm", "msg", "altsjt", "altmsg", "btns", "interOPRefKey"]
        )
        self.__dict__.update(kwargs)


class KakaoButton(object):
    def __init__(self, **kwargs):
        self.__dict__ = dict.fromkeys(["n", "t", "u1", "u2"])
        self.__dict__.update(kwargs)
