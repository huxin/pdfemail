import os
import sys

if len(sys.argv) != 2:
    print "Usage:", sys.argv[0], "email_file"
    exit(1)


email_f = sys.argv[1]
email_list = [e.strip().lower() for e in open(email_f, 'r')]
email_set = set(email_list)
print "{} has {} emails, {} unique".format(email_f, len(email_list), len(email_set))


# step 1:
print "\nStep1: fix wrong formatted email"

step1_file = email_f + '.step.1'
if os.path.exists(step1_file):
    print "Warning! step1 file {} already exist! abort".format(step1_file)
    exit(1)

outf = open(step1_file, 'w')
good = []
valid_suffix = ['.cn', '.com', '.edu', '.net', '.org']

import re
def fix_common_mistakes(e):
    e = re.sub(r'(\d+)$', '', e)

    com_err = ['.coin', '.corn', '.corn','.tom','.comm', '.coml',
               '.eom', '.conl', '.con', '.comp', '.jom', '.col', '.eonl',
               '.oom', '.odm', '.cob', '.cem', '.corll', '.coill', '.com.']
    for err in com_err:
        if e.endswith(err) or e.find(err+'.') != -1:
            e = e.replace(err, '.com')

    cn_err = ['.ca', '.en']
    for err in cn_err:
        if e.endswith(err):
            e = e.replace(err, '.cn')

    if e.startswith('china.'):
        e = e.replace('china.', '')

    return e


for e in email_set:
    e = fix_common_mistakes(e)
    valid = False
    for vs in valid_suffix:
        if e.endswith(vs):
            valid=True
            break
    if not valid:
        print >>outf, e
    else:
        good.append(e)

print >>outf,  "\n"

print >>outf, "\n".join(good)
outf.close()

print "Step 1 file {} generated, please fix wrong email format".format(step1_file)
os.system('subl ' + step1_file)
raw_input("Press any key to continue")


print "\nStep1.5: containing analysis"
step1_5_file = email_f + '.step.1.5'
outf = open(step1_5_file, 'w')
email_set = set([l.strip() for l in open(step1_file, 'r')])
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
        print >> outf, e, " ".join(contain_lst)

print >>outf, "\n"
print >>outf, "\n".join(no_contain_lst)
outf.close()
print "Step 1.5 file {} generated, please fix duplicate analysis emails".format(step1_5_file)
os.system('subl ' + step1_5_file)
raw_input("Press any key to continue")



print "\nStep2, remove all opened and sent email"
email_list = [e.strip().lower() for e in open(step1_5_file, 'r')]
email_set = set(email_list)
print "{} has {} emails, {} unique".format(step1_file, len(email_list), len(email_set))

step2_file = email_f + '.step.2'

outf = open(step2_file, 'w')
ignoref = open(email_f + '.step.2.ignore', 'w')


all_status_path = '/Users/huxin/Dropbox/Documents/jin/emailSent'
sys.path.insert(0, all_status_path)
import all_status

ignore_cnt = 0
e_cnt = 0
res_lst = []
for e in email_set:
    e = e.replace('yahoo.com.cn', 'aliyun.com').replace('yahoo.cn', 'aliyun.com')

    sg_s, sg_d, sg_o, sp_s, sp_d, sp_o, gmail_s, gmail_o, person_o = all_status.email_status(e)

    if person_o == "Y" or gmail_s == "Y":
        # ignore
        ignore_cnt += 1
        print >> ignoref,e,  gmail_s, person_o
    else:
        res_lst.append(e)

print >>outf, "\n".join(sorted(res_lst))
outf.close()
ignoref.close()

print "{} generated has {} emails, ignored {}".format(step2_file, len(res_lst), ignore_cnt)
os.system('subl ' + step2_file)




