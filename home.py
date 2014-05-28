#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
class Home(object):
    """
    首页及帐户管理
    """
    def index(self, **args):
        """首页"""
        #default_log.warn("test")
        return "it's work"
        #return self.render('home.html',"Home")


