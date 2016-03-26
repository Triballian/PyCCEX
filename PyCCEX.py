#!/usr/bin/env python
# coding=iso-8859-1

# PyCCEX: a Python binding to the C-CEX API
#
# Copyright © 2014 Scott Alfter
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import pycurl
import StringIO
import json
import certifi

class PyCCEX:
    

# constructor (key: API key; needed for private API calls)
    def __init__(self, key):
            self.key=key

# issue a query (method: string, params: dictionary with method parameters)
# private methods require a key to have been passed in with the constructor
    def Query(self, method, params):
        url=""
        if (method=="orderlist" or method=="getbalance" or method=="makeorder" or method=="cancelorder" or method=="tradehistory"):
            if (self.key==""):
                raise ValueError("private API calls require an API key")
            url="https://c-cex.com/t/r.html?key="+self.key+"&a="+method
        else:
            if (method=="tradehistory" or method=="volume" or method=="lastvolumes"):
                url="https://c-cex.com/t/s.html?a="+method
            if (url==""): # pairs, prices, currency-pair
                url="https://c-cex.com/t/"+method+".json"
        for i, param in enumerate(params):
            url+="&"+param+"="+params[param]
        b=StringIO.StringIO()
        ch=pycurl.Curl()
#fixed "SSL certificate problem: unable to get local issuer certification" error
        ch.setopt(pycurl.CAINFO, certifi.where())
        ch.setopt(pycurl.URL, url)
# this next bit is because Cloudflare sucks burro balls and blocks curl...
# we'll pretend we're Firefox
        ch.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0')
        ch.setopt(pycurl.WRITEFUNCTION, b.write)
        try:
            ch.perform()
        except pycurl.error, error:
            errno, errstr=error
            raise Exception("pycurl error: "+errstr)
        try:
            rtnval=json.loads(b.getvalue())
        except:
            raise Exception("unable to decode response")
        return rtnval

# see https://c-cex.com/?id=api for more information
#
# quick summary:
# 
# public calls: pairs, prices, tradehistory, volume, lastvolumes,
#               any currency pair (retrieves ticker for that pair)
# private calls: orderlist, getbalance, makeorder, cancelorder, 
#                tradehistory
#
# parameters get passed in as a dictionary of name-value pairs; pass
# in a null dictionary if no parameters are needed (as for pairs)
        