import os
import sys
from collections import deque

# pre-processing burp logs, so that it won't run out of memory

byte_len = 100
pre = ""
next = ""

buffer = deque([""]*100)
at_lst = []

with open(sys.argv[1], 'rb') as f:
    cur = f.read(byte_len)
    pre = next
    next = cur

    while cur != "":
        # do something
        if pre.find('@') != -1:
            at_lst.append(pre+next)

        cur = f.read(byte_len)
        pre = next
        next = cur


for l in at_lst:
    print l


