from email_from_text import comprehensive
import string

def onlyascii(s):
    r = ''
    for c in s:
        if c in string.printable:
            r += c
    return r


while True:
    l = raw_input()
    emails, invalids = comprehensive(l)

    # print candidate
    print emails, invalids
    for e in emails.union(invalids):
        p = onlyascii(e)
        if p != '':
            print p