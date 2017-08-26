# split based on valid tlds
import os
import sys

valid_tld_set = set([l.strip().lower() for l in open(os.path.join(os.path.dirname(__file__), 'valid_tld.lst'), 'r')])


inf_name = sys.argv[1]

valid_file = open(inf_name+'.valid.tld', 'w')
invalid_file = open(inf_name+'.invalid.tld', 'w')

for l in open(inf_name, 'r'):
    e = l.strip()
    tld = e.split('@')[-1].lower()
    if tld in valid_tld_set:
        print >>valid_file, e
    else:
        print >> invalid_file, e

valid_file.close()
invalid_file.close()