import os, sys, time
import web
import json
#import Queue
import multiprocessing
import threading

from miserver import handlers_long
from miserver import handlers_short

urls = (
r'/init/(.*)', 'Init', 
r'/testaa', 'Test', 
r'/(favicon\.ico)', 'Static', 
r'/(js|css|images|data)/(.*)', 'Static', 
r'/(.*\.(htm|html))', 'Html',
r'/(.*)', 'Server')

search_dirs = ['../miweb/tests/', '../miweb/', '../miweb/static']
static_dir = '../miweb/static/'

class HttpdError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Static(object):
    def GET(self, *arg, **kw):
        print arg
        fpath = os.path.join(static_dir, *arg)
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                return f.read()
        else:
            raise HttpdError('Can not found %s in %s' % (fn, static_dir))
            
class Html(object):
    def GET(self, *arg, **kw):
        print arg
        fn = arg[0]
        fpath = self.search_file(fn)
        if fpath:
            with open(fpath, 'r') as f:
                return f.read()
        else:
            raise HttpdError('Can not found %s in %s' % (fn, search_dirs))
            
    def search_file(self, fn):
        for p in search_dirs:
            if os.path.exists(os.path.join(p, fn)):
                return os.path.join(p, fn)
        return ''
        
class ResultFormat(object):
    def __init__(self, id, ret, data = '', msg = ''):
        self.__dict__['result'] = {}
        result = self.__dict__['result']
        result['id'] = id
        result['ret'] = ret
        result['data'] = data
        result['msg'] = msg
    def __getattr__(self, key):
        result = self.__dict__['result']
        return result[key]
    
    def __setattr__(self, key, value):
        result = self.__dict__['result']
        result[key] = value
        
    def get_json(self):
        return json.dumps(self.result)
RF = ResultFormat

class Server(object):
    qcmds = multiprocessing.Queue()
    qresults = multiprocessing.Queue()
    qsteps = multiprocessing.Queue()
    mia_h = None
    def get_params(self):
        return json.loads(web.input()['params'])
        
    def get_operid(self):
        return int(web.input()['id'])
        
    def GET(self, url):
        return self.server_handle(url)

    def POST(self, url):
        return self.server_handle(url)
        
    def server_handle(self, url):
        from miserver.utils import LoggerShort
        Log = LoggerShort.get_instance(__name__)
        print web.input()
        rf = None
        method = url
        if method:
            params = self.get_params()
            cid = self.get_operid()
        else:
            params = []
            cid = -1
        print 'method: "%s", params: "%s"' % (method, params)
        
        if not method:
            data = 'handlers_long: %s, handlers_short: %s' % (handlers_long, handlers_short)
            rf = RF(0, True, data, 'empty method msg')
            
        elif method == 'test':
            rf = RF(0, True, 'test data', 'test msg')
            #Server.qcmds.put((Server.id, 'do cmd test', ()))
            
        elif method == 'probe_step':
            qres = []
            while not Server.qsteps.empty():
                qres.append(Server.qsteps.get())
            rf = RF(cid, qres and True or False, qres, 'probe_step msg')
            
        elif method == 'get_results':
            qres = []
            while not Server.qresults.empty():
                qres.append(Server.qresults.get())
            rf = RF(cid, qres and True or False, qres, 'get_results msg')
            
        elif handlers_short.has_key(method):
            Log.d('%s(%s)' % (method, params))
            res = handlers_short[method](*params)
            rf = RF(cid, *res)
            
        elif handlers_long.has_key(method):
            Server.qcmds.put((cid, (method, params)))
            rf = RF(cid, True, '', 'long method run background')
        else:
            raise HttpdError('Server cannot handle "%s" method' % method)
            
        return rf.get_json()
        
class Init(object):
    def get_params(self):
        return json.loads(web.input()['params'])
        
    def get_operid(self):
        return int(web.input['id'])
        
    def GET(self, *arg, **kw):
        method = arg[0]
        if method == 'startserver':
            Server.mia_h = multiprocessing.Process(target=RunLongServer, args=(Server.qcmds, Server.qresults, Server.qsteps))
            Server.mia_h.start()
        if method == 'stopserver':
            #Server.id += 1
            Server.qcmds.put((self.get_operid(), 'quit', ()))
            if Server.mia_h: print 'join Server.mia_h...'; Server.mia_h.join()
            else: print 'None... %s' % Server.mia_h
            sys.exit(0)
            
class Test():
    def GET(self, *arg, **kw):
        print Server.id
        print "Server.qcmds id: %s" % id(Server.qcmds)
        print "Server.qresults id: %s" % id(Server.qresults)
    
class MiAction(object):
    def __init__(self, qcmds, qresults, qsteps):
        self.qcmds = qcmds
        self.qresults = qresults
        self.qsteps = qsteps
    def _run_cmd(self, cmd):
        method, params = cmd
        ret, msg = handlers_long[method](*params)
        result['ret'] = ret
        if ret: result['data'] = msg
        else: result['msg'] = msg
        return result
    def set_step(self, operid, step_cur, step_total):
        self.qsteps.put((operid, step_cur, step_total))
    def run(self):
        while True:
            from miserver.utils import LoggerLong
            Log = LoggerLong.get_instance(__name__)
            Log.d('Wait Cmds')
            cid, (cmd, params) = self.qcmds.get()
            Log.d('Get Cmd -> cid: %d, cmd: %s, params: %s' % (cid, cmd, params))
            operid = cid
            if cmd == 'quit':
                break
            try:
                res = handlers_long[cmd](self, operid, *params)
                self.qresults.put(res)
            except Exception, e:
                Log.e('[Error]: %s' % e)
            
            
            #print 'Get %s' % self.qcmds.get()
            #cid, cmd, params = self.qcmds.get()
            #print 'Get The Cmd: %s' % cmd
            #if cmd == 'quit':
            #    break
            #self.qresults.put((cid, self._run_cmd(cmd)))
            
def RunLongServer(qcmds, qresults, qsteps):
    mia = MiAction(qcmds, qresults, qsteps)
    mia.run()

if __name__ == "__main__":
    print '-' * 40
    app = web.application(urls, globals()) 
    app.request("/init/startserver")
    app.run()
    app.request("/init/stopserver")
    #time.sleep(3)