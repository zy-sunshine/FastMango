import os
import threading
import StringIO
import ConfigParser
from miutils import printer

class MiConfig_SubCategory(object):
    def __init__(self, confobj, section):
        self.__dict__['confobj'] = confobj
        self.__dict__['section'] = section
    
    def __getattr__(self, key):
        confobj = self.__dict__['confobj']
        section = self.__dict__['section']
        #if not confobj.has_option(section, key):
        #    confobj.set(section, key, None)
        #try:
        ret = confobj.get(section, key)
        #except:
        #    import pdb;pdb.set_trace()
        return ret

    def __setattr__(self, key, value):
        confobj = self.__dict__['confobj']
        section = self.__dict__['section']
        confobj.set(section, key, value)
        
class MiConfig(object):
    def __init__():
        "disable the __init__ method, and this config class current not thread safely"
    
    __inst = None # make it so-called private

    __lock = threading.Lock() # used to synchronize code

    @staticmethod
    def get_instance():
        MiConfig.__lock.acquire()
        if not MiConfig.__inst:
            MiConfig.__inst = object.__new__(MiConfig)
            object.__init__(MiConfig.__inst)
            printer.d('MiConfig.get_instance --> Create a MiConfig Instance\n')
            MiConfig.__inst.init()
        MiConfig.__lock.release()
        return MiConfig.__inst
        
    def init(self):
        self.__dict__['confobj'] = ConfigParser.RawConfigParser()
        self.__dict__['secobjs'] = {}
        conf_file = os.path.dirname(os.path.abspath(__file__))+'/config.ini'
        if not os.path.exists(conf_file):
            printer.exception('MiConfig.init --> Cannot load config file %s\n' % conf_file)
        self.load_from_file(conf_file)
        
    def __getattr__(self, key):
        confobj = self.__dict__['confobj']
        secobjs = self.__dict__['secobjs']
        if not confobj.has_section(key):
            confobj.add_section(key)
        if not secobjs.has_key(key):
            secobjs[key] = MiConfig_SubCategory(confobj, key)
        return secobjs[key]
        
    def save_to_file(self, conf_file):
        printer.d('MiConfig.save_to_file --> %s\n' % conf_file)
        confobj = self.__dict__['confobj']
        with open(conf_file, 'wb') as configfile:
            confobj.write(configfile)
        
    def load_from_file(self, conf_file):
        printer.d('MiConfig.load_from_file --> %s\n' % conf_file)
        confobj = self.__dict__['confobj']
        confobj.read(conf_file)
        
    def dump(self):
        output = StringIO.StringIO()
        confobj = self.__dict__['confobj']
        confobj.write(output)
        print output.getvalue()

    def __del__(self):
        printer.d('MiConfig.__del__ --> %s' % self)

def TestMiConfig_SaveConfig():
    mc = MiConfig.get_instance()
    mc.LOAD.teststring = 'stringstring test test abcde'
    mc.RUN.pkgarr_probe = [['/dev/sda1', 'ntfs', '/dev/sda1'], ['/dev/sda2',
    'ntfs', '/dev/sda2'], ['/dev/sda5', 'linux-swap(v1)', '/dev/sda5'],
    ['/dev/sda6', 'ext3', '/dev/sda6'], ['/dev/sda7', 'ext4', '/dev/sda7'],
    ['/dev/sda8', 'ntfs', '/dev/sda8']]

    mc.save_to_file('t-config.ini')
    mc2 = MiConfig.get_instance()
    mc.dump()
    print '-'*40
    mc2.dump()
    
def TestMiConfig_LoadConfig():
    mc = MiConfig.get_instance()
    mc2 = MiConfig.get_instance()
    mc2.load_from_file('t-config.ini')
    mc.dump()
    print '-'*40
    mc2.dump()
    
if __name__ == '__main__':
    TestMiConfig_SaveConfig()
    TestMiConfig_LoadConfig()