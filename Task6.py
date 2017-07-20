import configparser
import json
import psutil
from datetime import datetime
import time
import os

class Iniconfig():
    @classmethod
    def get(cls, file):
        config = configparser.ConfigParser()
        config.read(file)
        a = int(config.get('common', 'interval')) * 60
        b = config.get('common', 'output')
        return a, b

class Data:
    def __init__(self):
        self.cpu=str(psutil.cpu_percent(interval=1))
        self.virtmem=str(psutil.virtual_memory().used // 1024 // 1024)+'MB'
        self.swap=str(psutil.swap_memory().used // 1024 // 1024)+'MB'
        self.iocounter=psutil.disk_io_counters(perdisk=False)
        self.netcounter=psutil.net_io_counters()
    def busytime(self):
        return str(self.iocounter.busy_time//1000)+'sec'
    def bytesrecv(self):
        return str(self.netcounter.bytes_recv//1024 ** 2) +'MB'

class Textsuper(Data):
    def create(self):
        self.pop ='SNAPSHOT '+str(i)+': ' + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.pop +=': CPU load '+self.cpu
        self.pop += ': Memory '+ self.virtmem
        self.pop += ': VirtMem '+self.swap
        self.pop += ': IO '+ self.busytime()
        self.pop += ': Network Received ' +self.bytesrecv()+'\n'
        return self.pop

class Jsonsuper(Data):
    def create(self):
        self.dictforjson= {}
        self.dictforjson['SNAPSHOT'] = num + 1
        self.dictforjson['TIMESTAMP'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.dictforjson['CPU load'] = self.cpu
        self.dictforjson['Memory'] = self.virtmem
        self.dictforjson['VirtMem'] = self.swap
        self.dictforjson['IO'] = self.busytime()
        self.dictforjson['Network Received'] = self.bytesrecv()
        return self.dictforjson
i=1
a, b =Iniconfig.get('conf.ini')

while True:
    if b == 'json':
        try:
            f = open("output.json", 'a+')
            f.seek(0, 0)
            info=json.load(f)
            num=len(info["LOG"])
            f.close()
            f=open("output.json", 'w')
            print("Appending")
        except json.decoder.JSONDecodeError:
            print("New")
            info={}
            info["LOG"]=[]
            num=0
        write=Jsonsuper().create()
        info["LOG"].append(write)
        json.dump(info, f, indent=4)
        f.close()
    elif b == 'txt':
        f=open('output.txt','a+')
        if os.stat('output.txt').st_size > 0:
            f.seek(0, 0)
            i = int(f.readlines()[-1].split(':')[0].split(' ')[1]) + 1
        kok=Textsuper().create()
        f.write(kok)
        f.close()
    else:
        print("Specify 'json' or 'txt' format output in conf.ini")
        break
    time.sleep(a)


