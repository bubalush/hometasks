stat = dict()
with open('access.log') as f:
       for line in f:
            a = line.split(" ")
            if len(a) > 0:
                ip = a[0]
                stat[ip] = stat.get(ip, 0) + 1
c=sorted(stat.items(), key=lambda x:x[1], reverse=True)
for i in range(10):
    print (c[i][0], 'request ' + str(c[i][1]))

