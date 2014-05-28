#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, datetime, logging, __builtin__, hashlib, time,sys
from collections import OrderedDict, defaultdict

import gettext
import re
sys.path.insert(0,"lib.zip")

import web
import web_controller
import jinja2
import sqlite3 as db
from bs4 import BeautifulSoup
from config import *
from makeoeb import *

from helper import singleton

IsRunInLocal = (os.environ.get('SERVER_SOFTWARE', '').startswith('Development'))
log = logging.getLogger()

__builtin__.__dict__['default_log'] = log
__builtin__.__dict__['IsRunInLocal'] = IsRunInLocal


from books import BookClasses, BookClass



    
for book in BookClasses():  #添加内置书籍
    print book.title

    # if memcache.get(book.title): #使用memcache加速
    #     continue
    # b = Book.all().filter("title = ", book.title).get()
    # if not b:
        # b = Book(title=book.title,description=book.description,builtin=True)
        # b.put()
        # memcache.add(book.title, book.description, 86400)


class sqldb(object):
    #先验证数据库是否存在
    def __init__(self):
        if os.path.exists("msg.db"):
            #如果数据库存在，就直接连接
            self.conn = db.connect("msg.db")
            self.cu = self.conn.cursor()
        else:
            #如果数据库不存在，连接，并生成表
            self.conn = db.connect("msg.db")
            self.cu = self.conn.cursor()
            self.cu.execute("""create table msgs(
                     id integer primary key,
                     name text,
                     date text,
                     content text) """)
            self.cu.execute("""insert into msgs values(1,'Ahai','2010-05-19 15:11:20','Ahi alaws be ok!')""")
            self.conn.commit()



class Main(object):
    """docstring for Main"""
    def __init__(self):
        super(Main, self).__init__()

    def GET(self):
        #实例化sqldb，然后获取内容
        s = ""
        sdb = sqldb()
        rec = sdb.cu.execute("""select * from msgs""")
        dbre = sdb.cu.fetchall()
        for i in dbre:
            s =  "<p>"+i[2]+"  <span style=\"color: blue\">"+i[1]+' sad: '+r"</span>"+"  <span style=\"color: gray\">"+i[3]+r"</span></p>" + s

        sh = """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"><HTML>
        <HEAD><meta http-equiv="X-UA-Compatible" content="IE=8" />
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <TITLE> OK!</TITLE> </HEAD> <BODY><h1>Hello World!</h1>
        """
        sb = """
        <h2>add a note</h2>
        <form method="post" action="">
        UserName:<INPUT TYPE="text" NAME="uname"><br />
        <textarea name="content" ROWS="20" COLS="60"></textarea><br />
        <button type="submit">save</button></form></BODY></HTML>
        """
        s = sh + s + sb
        return s

    def POST(self):
        i = web.input('content')
        n = web.input('uname')
        date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        sdb = sqldb()
        rec = sdb.cu.execute("""select * from msgs""")
        dbre = sdb.cu.fetchall()
        for k in dbre:
            j = k[0]+1
        t = (j,n.uname,date,i.content)
        sdb.cu.execute('insert into msgs values(?,?,?,?)',t)
        sdb.conn.commit()
        return web.seeother('/')

urls = ( 
  "/test","Main",
  "/(.*)", "Gear",
)

hendler = web_controller.Handler()

class Gear(object):
    def GET(self, args = False):
        db = web.database(dbn='sqlite', db='mydatabase')
        # return "<html><body>hello world</body></html>"
        return hendler.control(args)
    def POST(self,args=False):
        return hendler.control(args)

application = web.application(urls, globals())
# store = MemcacheStore(memcache)
session = web.session.Session(application, web.session.DiskStore('sessions'), initializer={'username':'','login':0,"lang":''})

singleton.session=session
jjenv = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'),
                            extensions=["jinja2.ext.do",'jinja2.ext.i18n'])

web.config.debug=True
app = application.wsgifunc()
if __name__ == "__main__":

    application.run()
# web.config.debug = IsRunInLocal