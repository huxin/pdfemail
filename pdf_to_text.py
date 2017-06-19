# -*- coding: utf-8 -*-
import slate
import os
import sys

# run pdftotext to convert it to text
def pdftotext_convert(pdffile):
    textfname = "tmp_pdftotext.txt"
    cmd = "/usr/local/bin/pdftotext '" + pdffile + "' " + textfname
    os.system(cmd)
    return open(textfname, 'r').read()


def slate_convert(pdffile):
    content = ""
    with open(pdffile, 'rb') as f:
        docs = slate.PDF(f)
        for d in docs:
            content += d
    return content

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "Usage:", sys.argv[0], "pdffile <converter. 0: pdftotext, 1: slate>"
        exit(1)


    pdffile = sys.argv[1]
    converter = sys.argv[2]

    if converter == '0':
        print pdftotext_convert(pdffile)
    else:
        print slate_convert(pdffile)