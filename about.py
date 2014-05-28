#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
class About(object):   
    def __init__(self):


        self.env = web.ctx.get('env')
        self.method = web.ctx.get('method')
        #self.params = params

    def index(self, **args):
        """首页"""
        #default_log.warn("test")
        return "it's work"
        #return self.render('home.html',"Home")


