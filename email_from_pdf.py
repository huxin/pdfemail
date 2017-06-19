# -*- coding: utf-8 -*-
import sys
from pdf_to_text import pdftotext_convert
import email_from_text


def analyze(pdffile):
    # TODO: use better converter here
    content = pdftotext_convert(pdffile)
    return  email_from_text.comprehensive(content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "pdffile"
        exit(1)


    print analyze(sys.argv[1])






