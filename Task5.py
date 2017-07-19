import configparser
import json
import psutil
import datetime
import time
import os

config = configparser.ConfigParser()
config.read('conf.ini')
a=config.get('common', 'interval')
b=config.get('common', 'output')
print (a,b)
i=1


while True:
    cpu = str(psutil.cpu_percent(interval=1))
    virtmem = str(psutil.virtual_memory().used // 1024 // 1024)+'MB'
    swap = str(psutil.swap_memory().used // 1024 // 1024)+'MB'
    iocounter = str(psutil.disk_io_counters(perdisk=False).busy_time // 100)+'sec'
    netcounter = str(psutil.net_io_counters().bytes_recv // 1024 // 1024)+'MB'
    if b == 'json':
        with open('output.json', 'w') as outfile:
            json.dump(network, outfile)
    elif b == 'txt':
        f=open('output.txt','a+')
        if os.stat('output.txt').st_size > 0:
            f.seek(0, 0)
            i = int(f.readlines()[-1].split(':')[0].split(' ')[1]) + 1
        pop='SNAPSHOT '+str(i)+': ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        pop+=': CPU load '+cpu
        pop+= ': Memory '+virtmem
        pop+= ': VirtMem '+swap
        pop+= ': IO '+iocounter
        pop+= ': Network '+netcounter+'\n'
        f.write(pop)
        f.close()

    else:
        print('Specify json or txt format output in conf.ini')
        break

    time.sleep(1)


