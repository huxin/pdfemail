import os
import sys

email_set = set([l.strip() for l in open(sys.argv[1], 'r')])

no_contain_lst = []

for e in email_set:
    contain_lst = []
    for e2 in email_set:
        if e == e2:
            continue

        if e2.endswith(e):
            contain_lst.append(e2)

    if len(contain_lst) ==0:
        no_contain_lst.append(e)
    else:
        print e, " ".join(contain_lst)


print
for e in no_contain_lst:
    print e