#encoding=utf-8
import os, sys, time
import traceback

'''colors, for nice output'''

##################### Windows Cmd Start ###########################
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED  = 0x04 # text color contains red.

FOREGROUND_INTENSITY = 0x08 # text color is intensified.
BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED  = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.



# 颜色配对 See http:http://lcs.syr.edu/faculty/morphet/screen.cpp

#define FOREGROUND_BLACK   (0)
#define FOREGROUND_WHITE   (FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
#define FOREGROUND_YELLOW  (FOREGROUND_RED | FOREGROUND_GREEN)
#define FOREGROUND_MAGENTA (FOREGROUND_RED | FOREGROUND_BLUE)
#define FOREGROUND_CYAN    (FOREGROUND_GREEN | FOREGROUND_BLUE)
#define BACKGROUND_BLACK   (0)
#define BACKGROUND_WHITE   (BACKGROUND_RED | BACKGROUND_GREEN | BACKGROUND_BLUE)
#define BACKGROUND_YELLOW  (BACKGROUND_RED | BACKGROUND_GREEN)
#define BACKGROUND_MAGENTA (BACKGROUND_RED | BACKGROUND_BLUE)
#define BACKGROUND_CYAN    (BACKGROUND_GREEN | BACKGROUND_BLUE)

import ctypes

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    '''(color) -> BOOL
    
    Example: set_cmd_text_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    '''
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool

def resetColor():
    '''重新设置成黑白色'''
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

def printError(mess):
    '''
    打印错误信息
    '''
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
    print(mess)
    resetColor()

def printProcess(mess):
    '''
    打印处理进度信息
    '''
    set_cmd_text_color(FOREGROUND_GREEN | FOREGROUND_BLUE)
    print(mess)
    resetColor()

def printResult(mess):
    '''
    打印结果或选择后的信息
    '''
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_BLUE| FOREGROUND_INTENSITY)
    print(mess)
    resetColor()

def printWait(mess):
    '''
    打印等候信息
    '''
    set_cmd_text_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    print(mess)
    resetColor()

def tprintList():
    '''
    打印选择列表前先设置的颜色
    '''
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY)
#
def tprintTip():
    '''
    在 raw_input 前先设置的颜色
    '''
    set_cmd_text_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)

##################### Windows Cmd End ###########################

class color_default:
    def __init__(self):
        self.name = 'default'
        self.black =    ('\x1b[0;30m', FOREGROUND_BLACK)
        self.red =  ('\x1b[0;31m', FOREGROUND_RED)
        self.green =    ('\x1b[0;32m', FOREGROUND_GREEN)
        self.yellow =   ('\x1b[0;33m', FOREGROUND_RED | FOREGROUND_GREEN)
        self.blue = ('\x1b[0;34m', FOREGROUND_BLUE)
        self.magenta =  ('\x1b[0;35m', BACKGROUND_RED | BACKGROUND_BLUE)
        self.cyan = ('\x1b[0;36m', BACKGROUND_GREEN | BACKGROUND_BLUE)
        self.white =    ('\x1b[0;37m', FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
        self.normal =   ('\x1b[0m', FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
        self.bold = ('\x1b[1m', BACKGROUND_INTENSITY)
        self.clear =    ('\x1b[J', FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

class color_bw:
    def __init__(self):
        self.name = 'bw'
        self.black =    '\x1b[0;30m'
        self.red =  '\x1b[0m'
        self.green =    '\x1b[0m'
        self.yellow =   '\x1b[0m'
        self.blue = '\x1b[0m'
        self.magenta =  '\x1b[0m'
        self.cyan = '\x1b[0m'
        self.white =    '\x1b[0m'
        self.normal =   '\x1b[0m'
        self.bold = '\x1b[0m'
        self.clear =    '\x1b[J'

### different useful prints
color_classes = {
    'default':  color_default,
    'bw':       color_bw
}
c = color_classes['default']()    

def printl(line, color = c.normal, bold = 0):
    'Prints a line with a color'
    if os.name == 'nt':
        c = color[1]
        if bold:
            c = c | FOREGROUND_INTENSITY
        set_cmd_text_color(c)
        safe_write(line)
        resetColor()
    elif os.name == 'posix':
        out = ''
        if bold:
            out = c.bold
        out = color[0] + out + line + c.normal[0]
        safe_write(out)
    else:
        safe_write(out)
    safe_flush()
    
def i(line):
    'Prints an infor'
    printl(line, c.green, 1)
    
def d(line):
    'Prints an debug'
    printl(line, c.blue, 1)

def w(line):
    'Prints an warning'
    printl(line, c.yellow, 1)

def e(line):
    'Prints an error'
    printl(line, c.red, 1)

def exception(line):
    '''Prints an exception, but sometime it will only print one layer exception message, 
        so it will make debug from exception information hardly
        and better not use it in exception to print exception information'''
    safe_write('\n')
    printl('! ! !', c.cyan, 1)
    printl(line, c.cyan, 1)
    traceback.print_exc()
    safe_write('\n')
    safe_flush()
    beep()

def beep(q = 0):
    'Beeps unless it\'s told to be quiet'
    if not q:
        printl('\a')


def safe_flush():
    '''Safely flushes stdout. It fixes a strange issue with flush and
    nonblocking io, when flushing too fast.'''
    c = 0
    while c < 100:
        try:
            sys.stdout.flush()
            return
        except IOError:
            c +=1
            time.sleep(0.01 * c)
    raise Exception, 'flushed too many times, giving up. Please report!'

def safe_write(text):
    '''Safely writes to stdout. It fixes the same issue that safe_flush,
    that is, writing too fast raises errors due to nonblocking fd.'''
    c = 1
    while c:
        try:
            sys.stdout.write(text)
            return
        except IOError:
            c += 1
            time.sleep(0.01 * c)
    raise Exception, 'wrote too many times, giving up. Please report!'
