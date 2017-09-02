import os
import time

lst = []
while True:
    l = raw_input().strip()
    if l == "done":
    	break
    lst.append(l)



for l in lst:
    cnt = 1
    print "open:", l
    for f in os.listdir('.'):
        if f.lower().find(l.lower()) != -1:
            print cnt, ":", f
            cnt += 1
            os.system('open ' + f)
            time.sleep(2)

    print "finish open", l, "press any key to continue"
    raw_input()



