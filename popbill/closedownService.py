# -*- coding: utf-8 -*-
# Module for Popbill Closedown API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Contributor : Linkhub Dev (code@linkhubcorp.com)
# Updated : 2025-08-27
# Thanks for your interest.

from .base import PopbillBase, PopbillException


class ClosedownService(PopbillBase):

    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("170")

    def getChargeInfo(self, CorpNum, UserID=None):

        return self._httpget("/CloseDown/ChargeInfo", CorpNum, UserID)

    def getUnitCost(self, CorpNum):

        result = self._httpget("/CloseDown/UnitCost", CorpNum)

        return float(result.unitCost)

    def checkCorpNum(self, MemberCorpNum, CheckCorpNum):

        return self._httpget("/CloseDown?CN=" + CheckCorpNum, MemberCorpNum)

    def checkCorpNums(self, MemberCorpNum, CorpNumList):

        postData = self._stringtify(CorpNumList)

        return self._httppost("/CloseDown", postData, MemberCorpNum)
