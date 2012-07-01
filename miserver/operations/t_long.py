#!/usr/bin/python
import time
from miutils.miregister import MiRegister
register = MiRegister()
from miserver.utils import Logger
Log = Logger.get_instance(__name__)

@register.server_handler('long')
def l_test(mia, operid, sleepsec):
    Log.d('do l_test method')
    for step in range(sleepsec):
        mia.set_step(operid, step, sleepsec)
        time.sleep(1)
    return (True, 'l_test return data', 'The description message')
