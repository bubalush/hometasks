import configparser
import json
import psutil
from datetime import datetime
import time
import os

config = configparser.ConfigParser()
config.read('conf.ini')
a=int(config.get('common', 'interval'))*60
b=config.get('common', 'output')
i=1


while True:
    cpu = str(psutil.cpu_percent(interval=1))
    virtmem = str(psutil.virtual_memory().used // 1024 // 1024)+'MB'
    swap = str(psutil.swap_memory().used // 1024 // 1024)+'MB'
    iocounter = str(psutil.disk_io_counters(perdisk=False).busy_time // 100)+'sec'
    netcounter = str(psutil.net_io_counters().bytes_recv // 1024 // 1024)+'MB'
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
        write={}
        write['SNAPSHOT']=num+1
        write['TIMESTAMP']=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        write['CPU load']=cpu
        write['Memory']=virtmem
        write['VirtMem']=swap
        write['IO']=iocounter
        write['Network Received']=netcounter
        info["LOG"].append(write)
        json.dump(info, f, indent=4)
        f.close()
    elif b == 'txt':
        f=open('output.txt','a+')
        if os.stat('output.txt').st_size > 0:
            f.seek(0, 0)
            i = int(f.readlines()[-1].split(':')[0].split(' ')[1]) + 1
        pop='SNAPSHOT '+str(i)+': ' + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        pop+=': CPU load '+cpu
        pop+= ': Memory '+virtmem
        pop+= ': VirtMem '+swap
        pop+= ': IO '+iocounter
        pop+= ': Network Received' +netcounter+'\n'
        f.write(pop)
        f.close()

    else:
        print("Specify 'json' or 'txt' format output in conf.ini")
        break

    time.sleep(a)


