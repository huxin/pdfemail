import os
import time


while True:
    l = raw_input()
    cnt = 1
    for f in os.listdir('.'):
        if f.lower().find(l.lower()) != -1:
            print cnt, ":", f
            cnt += 1
            os.system('open ' + f)
            time.sleep(2)
