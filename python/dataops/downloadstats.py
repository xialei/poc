# coding=utf-8

import commands
from tools import mongoclient

miui="MiuiBrowser"
uc="UCBrowser"
qq="QQ"
micro="MicroMessenger"

huawei=["HUAWEI"]
samsung=["SAMSUNG","SM-G","SCH-I","GT-I"]
htc=["HTC"]
xiaomi=["MI","XiaoMi"]
sony=["L39h"]
mx=["M040"]

android="/app/log/android_t.sh"
ios="/app/log/iphone_t.sh"

def downloadstats(db):

    stats = db['appdownload']
    
    #android
    a,b = commands.getstatusoutput('ls') # a:status; b:result
    
    
    
    
if __name__ == "__main__":
    downloadstats(mongoclient.get_db())


