#!/usr/bin/python
import time
from miutils.miregister import MiRegister
register = MiRegister()
from miserver.utils import Logger
Log = Logger.get_instance(__name__)

@register.server_handler('short')
def s_test(x, y):
    Log.d('d s_test method')
    return (True, x + y, 'This is an short operate to sum x and y')
    