# -*- coding: utf-8 -*-
# Module for Popbill Closedown API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Jeong Yohan (code@linkhubcorp.com)
# Written : 2020-06-24
# Updated : 2025-08-27
# Thanks for your interest.

from .base import PopbillBase, PopbillException

try:
    from urllib import parse as parse
except ImportError:
    import urllib as parse
import re


class AccountCheckService(PopbillBase):

    def __init__(self, LinkID, SecretKey):

        super(self.__class__, self).__init__(LinkID, SecretKey)
        self._addScope("182")
        self._addScope("183")

    def getChargeInfo(self, CorpNum, UserID=None, ServiceType=None):

        url = "/EasyFin/AccountCheck/ChargeInfo"

        if ServiceType != None and ServiceType != "":
            url = "/EasyFin/AccountCheck/ChargeInfo?serviceType=" + parse.quote(
                ServiceType
            )

        return self._httpget(url, CorpNum, UserID)

    def getUnitCost(self, CorpNum, UserID=None, ServiceType=None):

        url = "/EasyFin/AccountCheck/UnitCost"

        if ServiceType != None and ServiceType != "":
            url = "/EasyFin/AccountCheck/UnitCost?serviceType=" + parse.quote(
                ServiceType
            )

        result = self._httpget(url, CorpNum, UserID)

        return float(result.unitCost)

    def checkAccountInfo(self, CorpNum, BankCode, AccountNumber, UserID=None):

        uri = "/EasyFin/AccountCheck"
        uri += "?c=" + BankCode
        uri += "&n=" + AccountNumber

        return self._httppost(uri, "", CorpNum, UserID)

    def checkDepositorInfo(
        self,
        CorpNum,
        BankCode,
        AccountNumber,
        IdentityNumType,
        IdentityNum,
        UserID=None,
    ):

        uri = "/EasyFin/DepositorCheck"
        uri += "?c=" + BankCode
        uri += "&n=" + AccountNumber
        uri += "&t=" + IdentityNumType
        uri += "&p=" + IdentityNum

        return self._httppost(uri, "", CorpNum, UserID)
