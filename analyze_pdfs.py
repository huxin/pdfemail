# -*- coding: utf-8 -*-
import slate
import os
import sys
import hashlib
import shutil

import email_from_pdf

if len(sys.argv) != 2:
    print "Usage:", sys.argv[0], "directory"
    exit(1)

def load_processed_md5():
    # TODO: read history for processed md5s, so we don't do duplicate work
    d = "analyzed"
    ret = set()
    for f in os.listdir(d):
        md5 = f.split('.')[0].split('_')[0]
        ret.add(md5)

    return ret

processed_md5 = load_processed_md5()

os.chdir(sys.argv[1])

dup_dir = "dup"
if not os.path.exists(dup_dir):
    os.mkdir(dup_dir)



emailf = open('emails.lst', 'w')
invalidf = open('invalid_emails.lst', 'w')


def AnalyzePdf(pdffile):
    # read pdf
    md5 = hashlib.md5(open(pdffile, 'rb').read()).hexdigest()

    if md5 in processed_md5:
        # move to duplicate directory
        print "duplicate:", md5
        shutil.move(pdffile, os.path.join(dup_dir, md5+'_'+pdffile))
        return


    # read through txt files and identify potential emails
    emails, invalid_emails = email_from_pdf.analyze(pdffile)


    newname = md5
    if len(emails) > 0:
        newname += "_"+'_'.join(list(emails))

        print >>emailf, "\n".join(list(emails))

    if len(invalid_emails) > 0:
        print >>invalidf, "\n".join(list(invalid_emails))

    print newname[:100]+'.pdf'
    shutil.move(pdffile, newname[:100]+'.pdf')

    processed_md5.add(md5)


for f in os.listdir('.'):
    # read file, process it
    if not f.endswith('pdf'):
        continue
    AnalyzePdf(f)

emailf.close()
invalidf.close()