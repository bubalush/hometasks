import configparser
import json
import psutil
from datetime import datetime
import time
import os

config = configparser.ConfigParser()
config.read('conf.ini')
a=config.get('common', 'interval')
b=config.get('common', 'output')
i=1


while True:
    cpu = str(psutil.cpu_percent(interval=1))
    virtmem = str(psutil.virtual_memory().used // 1024 // 1024)+'MB'
    swap = str(psutil.swap_memory().used // 1024 // 1024)+'MB'
    iocounter = str(psutil.disk_io_counters(perdisk=False).busy_time // 100)+'sec'
    netcounter = str(psutil.net_io_counters().bytes_recv // 1024 // 1024)+'MB'
    if b == 'json':
        num="SNAPSHOT {}".format(i)
        jsondict={num:{'TIMESTAMP': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),'CPU load': cpu, 'Memory': virtmem,'VirtMem': swap,'IO': iocounter,'Network': netcounter}}
        if os.path.isfile('output.json') is True:
            if os.stat('output.json').st_size ==0:
                with open('output.json', 'w') as outfile:
                    json.dump(jsondict, outfile, indent=4)
            else:
                f=open('output.json', 'r+')
                dictforjson=json.load(f)
                g=1
                for x in dictforjson.keys():
                    if int(x.split(" ")[1]) > g:
                        g=int(x.split(" ")[1])
                i=g+1
                num="SNAPSHOT {}".format(i)
                dictforjson[num]={'TIMESTAMP': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),'CPU load': cpu, 'Memory': virtmem,'VirtMem': swap,'IO': iocounter, 'Network': netcounter}
 +              f.seek(0, 0)
 +              json.dump(dictforjson, f, indent=4)
 +              f.close()

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
        pop+= ': Network '+netcounter+'\n'
        f.write(pop)
        f.close()

    else:
        print("Specify 'json' or 'txt' format output in conf.ini")
        break

    time.sleep(1)


