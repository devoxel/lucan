# -*- coding: utf-8 -*-
import datetime

def time():
    t = str(datetime.datetime.now())
    t = t[:t.find('.')] # remove mircrosecond (i know i'm lazy)
    return t

def log(msg, *args):
    try:
        for elm in args:
            msg = msg.format(elm)
    except:
        pass
    print "{} -> {}".format(time(), msg)
