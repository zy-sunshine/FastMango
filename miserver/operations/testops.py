#!/usr/bin/python
import time
from miutils.miregister import MiRegister
register = MiRegister()
from miserver.utils import Logger
Log = Logger.get_instance(__name__)
dolog = Log.i

@register.server_handler('short')
def test_short(mia, operid, sleepsec):
    Log.d('do test_short short method')
    #for step in range(sleepsec):
        #mia.set_step(operid, step, sleepsec)
    #    time.sleep(1)
    return 0, ''
    
@register.server_handler('long')
def test_step0(mia, operid, sleepsec):
    Log.d('do test_step0 long method')
    for step in range(sleepsec):
        mia.set_step(operid, step, sleepsec)
        time.sleep(1)
    return 0, ''
    
@register.server_handler('long')
def test_step1(mia, operid, sleepsec):
    Log.d('do test_step1 long method')
    for step in range(sleepsec):
        mia.set_step(operid, step, sleepsec)
        time.sleep(1)
    return 0, ''
    
@register.server_handler('long')
def sleep(mia, operid, sleepsec):
    Log.d('do sleep long method')
    for step in range(sleepsec):
        mia.set_step(operid, step, sleepsec)
        time.sleep(1)
    return 0, ''
