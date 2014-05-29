#!usr/bin/Python
# -*- coding:utf-8 -*-
"""为了应付时不时出现的Too many redirects异常，使用此类打开链接。
此类会自动处理redirect和cookie，同时增加了失败自动重试功能"""
import urllib, urllib2, Cookie, urlparse, time
# from google.appengine.api import urlfetch
# from config import CONNECTION_TIMEOUT

import helper

CONNECTION_TIMEOUT=30

class URLOpener(object):
    def __init__(self, host=None, maxfetchcount=2, maxredirect=3, 
                timeout=CONNECTION_TIMEOUT, addreferer=False):
        self.cookie = Cookie.SimpleCookie()
        self.maxFetchCount = maxfetchcount
        self.maxRedirect = maxredirect
        self.host = host
        self.addReferer = addreferer
        self.timeout = timeout
        self.realurl = ''
    
    def open(self, url, data=None):
        method = "GET" if data is None else "POST"
        self.realurl = url
        maxRedirect = self.maxRedirect
        
        class resp: #出现异常时response不是合法的对象，使用一个模拟的
            status_code=555
            content=None
            headers={}
        
        response = resp()
        if url.startswith('data:image/'):
            from base64 import b64decode
            try:
                idx_begin = url.find(';base64,') or url.find(';BASE64,')
                response.content = b64decode(url[idx_begin+8:])
                response.status_code = 200
            except TypeError:
                response.status_code = 404
        else:
            while url and (maxRedirect > 0):
                print url
                cnt = 0
                
                try:
                    response.content=helper.read_page(url,method=method,data=data)                        
                    # print response.content
                    # response = urlfetch.fetch(url=url, payload=data, method=method,
                    #     headers=self._getHeaders(url),
                    #     allow_truncated=False, follow_redirects=False, 
                    #     deadline=self.timeout, validate_certificate=False)
                    response.status_code=200                        
                except Exception, e: 
                    response.status_code = 504
                    cnt += 1
                    time.sleep(1)
                else: 
                    break
        return response
        

    def _getHeaders(self, url=None):
        headers = {
             'User-Agent':"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
        cookie = '; '.join(["%s=%s" % (v.key, v.value) for v in self.cookie.values()])
        if cookie:
            headers['Cookie'] = cookie
        if self.addReferer and (self.host or url):
            headers['Referer'] = self.host if self.host else url
        return headers
        
    def SaveCookies(self, cookies):
        if not cookies:
            return
        self.cookie.load(cookies[0])
        for cookie in cookies[1:]:
            obj = Cookie.SimpleCookie()
            obj.load(cookie)
            for v in obj.values():
                self.cookie[v.key] = v.value
            