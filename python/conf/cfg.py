# encoding=utf-8

#===============================================================================
# @author roger.xia
#===============================================================================
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.readfp(open('../conf/config.properties'))

def getProperty(section, key):
    return cf.get(section, key)
    
def getSection(section):
    return cf.items(section)

if __name__ == '__main__':
    print getProperty("soufun", "url")