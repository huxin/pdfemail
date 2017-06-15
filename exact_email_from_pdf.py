# -*- coding: utf-8 -*-
import slate
import os
import sys
import hashlib
import shutil

if len(sys.argv) != 2:
    print "Usage:", sys.argv[0], "directory"
    exit(1)

os.chdir(sys.argv[1])

dup_dir = "dup"
if not os.path.exists(dup_dir):
    os.mkdir(dup_dir)

def load_processed_md5():
    # TODO: read history for processed md5s, so we don't do duplicate work
    return set()

processed_md5 = set()



def AnalyzePdf(pdffile):
    # read pdf
    md5 = hashlib.md5(open(pdffile, 'rb').read()).hexdigest()

    if md5 in processed_md5:
        # move to duplicate directory
        shutil.move(pdffile, os.path.join(dup_dir, md5+'_'+pdffile))
        return

    # run pdftotext to convert it to text
    textfname = "tmp.txt"
    cmd = "/usr/local/bin/pdftotext '" + pdffile + "' " + textfname
    os.system(cmd)

    # read through txt files and identify potential emails



    processed_md5.add(md5)




for f in os.listdir('.'):
    # read file, process it
    if not f.endswith('pdf'):
        continue
    AnalyzePdf(f)

    break