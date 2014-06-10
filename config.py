#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.insert(0,"lib.zip")
import pymongo

from books import BookClasses, BookClass
from books.base import BaseFeedBook,  BaseUrlBook

def main():
    for book in BookClasses():  #添加内置书籍
        #print book.title
        # bk=BaseUrlBook()
        bk=book()
        print bk.title
        # print bk
        # print book
        if not hasattr(book, "Items"):                            
            print "no items function"
        for sec_or_media, url, title, content, brief, thumbnail in bk.Items():
            # if not sec_or_media or not title or not content:
            #         continue
            print "url:"+str(url)+"  ok"
            #print content

if __name__ == '__main__':
    main()