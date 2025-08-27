# -*- coding: utf-8 -*-
# Module for Popbill Kakao API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Contributor : Linkhub Dev (code@linkhubcorp.com)
# Updated : 2025-08-27
# Thanks for your interest.
from .base import File, PopbillBase, PopbillException, Response

try:
    from urllib import parse as parse
except ImportError:
    import urllib as parse


class KakaoService(PopbillBase):

    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("153")
        self._addScope("154")
        self._addScope("155")

    def getURL(self, CorpNum, UserID, ToGo):


        if ToGo == "SENDER":
            result = self._httpget("/Message/?TG=" + ToGo, CorpNum, UserID)
        else:
            result = self._httpget("/KakaoTalk/?TG=" + ToGo, CorpNum, UserID)
        return result.url

    def getPlusFriendMgtURL(self, CorpNum, UserID):

        result = self._httpget("/KakaoTalk/?TG=PLUSFRIEND", CorpNum, UserID)
        return result.url

    def getSenderNumberMgtURL(self, CorpNum, UserID):

        result = self._httpget("/Message/?TG=SENDER", CorpNum, UserID)
        return result.url

    def getATSTemplateMgtURL(self, CorpNum, UserID):

        result = self._httpget("/KakaoTalk/?TG=TEMPLATE", CorpNum, UserID)
        return result.url

    def getSentListURL(self, CorpNum, UserID):

        result = self._httpget("/KakaoTalk/?TG=BOX", CorpNum, UserID)
        return result.url

    def listPlusFriendID(self, CorpNum, UserID=None):

        return self._httpget("/KakaoTalk/ListPlusFriendID", CorpNum, UserID)

    def checkSenderNumber(self, CorpNum, SenderNumber, UserID=None):

        if SenderNumber == None or SenderNumber == "":
            raise PopbillException(-99999999, "발신번호가 입력되지 않았습니다.")

        return self._httpget(
            "/KakaoTalk/CheckSenderNumber/" + SenderNumber, CorpNum, UserID
        )

    def getSenderNumberList(self, CorpNum, UserID=None):

        return self._httpget("/Message/SenderNumber", CorpNum, UserID)

    def getATSTemplate(self, CorpNum, templateCode, UserID=None):

        if templateCode == None or templateCode == "":
            raise PopbillException(-99999999, "발신번호가 입력되지 않았습니다.")

        result = self._httpget(
            "/KakaoTalk/GetATSTemplate/" + templateCode, CorpNum, UserID
        )
        return result

    def listATSTemplate(self, CorpNum, UserID=None):

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

        if PlusFriendID == None or PlusFriendID == "":
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


        if PlusFriendID == None or PlusFriendID == "":
            raise PopbillException(-99999999, "검색용 아이디가 입력되지 않았습니다.")

        if FilePath == None or FilePath == "":
            raise PopbillException(-99999999, "이미지 파일이 입력되지 않았습니다.")


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

    def sendFMSBinary(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FileDatas,
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

        return self.sendFMSBinary_same(
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
    def sendFMSBinary_multi(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FileDatas,
        ImageURL,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
        AltSubject=None,
    ):
        return self.sendFMSBinary_same(
            CorpNum,
            PlusFriendID,
            Sender,
            "",
            "",
            AltSendType,
            SndDT,
            FileDatas,
            ImageURL,
            KakaoMessages,
            KakaoButtons,
            AdsYN,
            UserID,
            RequestNum,
            None,
        )



    def sendFMSBinary_same(
        self,
        CorpNum,
        PlusFriendID,
        Sender,
        Content,
        AltContent,
        AltSendType,
        SndDT,
        FileDatas,
        ImageURL,
        KakaoMessages,
        KakaoButtons,
        AdsYN=False,
        UserID=None,
        RequestNum=None,
        AltSubject=None,
    ):


        if PlusFriendID == None or PlusFriendID == "":
            raise PopbillException(-99999999, "검색용 아이디가 입력되지 않았습니다.")

        if FileDatas == None:
            raise PopbillException(-99999999, "파일 정보가 입력되지 않았습니다.")


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
        for file in FileDatas:
            files.append(
                File(
                    fieldName="file",
                    fileName=file.fileName,
                    fileData=file.fileData,
                )
            )

        result = self._httppost_files("/FMS", postData, files, CorpNum, UserID)

        return result.receiptNum

    def cancelReserve(self, CorpNum, ReceiptNum, UserID=None):

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        return self._httpget("/KakaoTalk/" + ReceiptNum + "/Cancel", CorpNum, UserID)

    def cancelReserveRN(self, CorpNum, RequestNum, UserID=None):

        if RequestNum == None or RequestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        response = self._httpget("/KakaoTalk/Cancel/" + RequestNum, CorpNum, UserID)
        return Response(**response.__dict__)

    def getMessages(self, CorpNum, ReceiptNum, UserID=None):

        if ReceiptNum == None or ReceiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

        return self._httpget("/KakaoTalk/" + ReceiptNum, CorpNum, UserID)

    def getMessagesRN(self, CorpNum, RequestNum, UserID=None):

        if RequestNum == None or RequestNum == "":
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

        if MsgType == None:
            raise PopbillException(-99999999, "카카오톡 유형이 입력되지 않았습니다.")

        result = self._httpget("/KakaoTalk/UnitCost?Type=" + MsgType, CorpNum)

        return float(result.unitCost)

    def getChargeInfo(self, CorpNum, MsgType, UserID=None):

        if MsgType == None:
            raise PopbillException(-99999999, "카카오톡 유형이 입력되지 않았습니다.")

        return self._httpget("/KakaoTalk/ChargeInfo?Type=" + MsgType, CorpNum, UserID)

    def CancelReserveRNbyRCV(self, CorpNum, requestNum, receiveNum, UserID=None):

        if requestNum == None or requestNum == "":
            raise PopbillException(-99999999, "요청번호가 입력되지 않았습니다.")

        postData = self._stringtify(receiveNum)

        response = self._httppost(
            "/KakaoTalk/Cancel/" + requestNum, postData, CorpNum, UserID
        )
        return Response(response)

    def CancelReservebyRCV(self, CorpNum, receiptNum, receiveNum, UserID=None):

        if receiptNum == None or receiptNum == "":
            raise PopbillException(-99999999, "접수번호가 입력되지 않았습니다.")

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
