#!/usr/bin/env python
# -*- coding: utf-8 -*-
from web import utils
#from web import webapi as web

def background(func):
    """A function decorator to run a long-running function as a background thread."""
    def internal(*a, **kw):
        web.data() # cache it

        tmpctx = web._context[threading.currentThread()]
        web._context[threading.currentThread()] = utils.storage(web.ctx.copy())

        def newfunc():
            web._context[threading.currentThread()] = tmpctx
            func(*a, **kw)
            myctx = web._context[threading.currentThread()]
            for k in myctx.keys():
                if k not in ['status', 'headers', 'output']:
                    try: del myctx[k]
                    except KeyError: pass
        
        t = threading.Thread(target=newfunc)
        background.threaddb[id(t)] = t
        t.start()
        web.ctx.headers = []
        return seeother(changequery(_t=id(t)))
    return internal
background.threaddb = {}

def backgrounder(func):
    def internal(*a, **kw):
        i = web.input(_method='get')
        if '_t' in i:
            try:
                t = background.threaddb[int(i._t)]
            except KeyError:
                return web.notfound()
            web._context[threading.currentThread()] = web._context[t]
            return
        else:
            return func(*a, **kw)
    return internal

from datetime import datetime; now = datetime.now
from time import sleep

urls = (
    '/', 'index',
    )

class index:
    @backgrounder
    def GET(self):
        print "Started at %s" % now()
        print "hit f5 to refresh!"
        longrunning()


@background
def longrunning():
    for i in range(10):
        sleep(1)
        print "%s: %s" % (i, now())

if __name__ == '__main__':
    app = web.application(urls, globals()) 
    app.run()