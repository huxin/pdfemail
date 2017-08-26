import os
from collections import defaultdict

tld_cnt = defaultdict(int)

for l in open('all_sent.lst', 'r'):
    tld = l.strip().split('@')[-1]
    tld_cnt[tld] += 1


for tld, cnt in sorted(tld_cnt.items(), key=lambda x:x[1], reverse=True):
    print tld, cnt
