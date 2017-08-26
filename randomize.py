import random
import os
import sys

if len(sys.argv) == 1:
    lst = []

    print "paste data:"
    while True:
        l = raw_input()
        l = l.strip()
        if l == 'done':
            break
        lst.append(l)
    random.shuffle(lst)
    print
    print  "------RANDOMIZE------"
    print
    print "\n".join(lst)


else:
    inf_name = sys.argv[1]

    email_lst = [l.strip().lower() for l in open(inf_name, 'r')]
    email_set = set(email_lst)

    if len(email_set) != len(email_lst):
        print "Email not unique!!", len(email_set), len(email_lst)

    random.shuffle(email_lst)
    with open(inf_name+'.random', 'w') as f:
        print >>f, "\n".join(email_lst)
