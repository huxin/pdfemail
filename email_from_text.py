# -*- coding: utf-8 -*-
from regex_email import analyze_for_emails
import sys
import unicodedata


def different_processes(content):
    print "As ascii:", analyze_for_emails(content)

    content_newline_as_space = content.replace("\n", " ").replace("\r", " ")
    print "new line as space:", analyze_for_emails(content_newline_as_space)

    content_utf8 = content.decode('utf-8')
    print "as utf-8", analyze_for_emails(content_utf8)


    normal = unicodedata.normalize('NFKD', content_utf8)
    print "after normalization", analyze_for_emails(normal)

    normal_newline_asspace = normal.replace("\n", ' ').replace('\r', ' ')
    print "newline as space:", analyze_for_emails(normal_newline_asspace)

    # remove all "\n"
    normal = normal.replace('\n', '').replace("\r", '')
    print "after removing new line:", analyze_for_emails(normal)


def comprehensive(content):
    ei_lst = []

    # as it is
    ei_lst.append(analyze_for_emails(content))

    content_nonewline = content.replace("\n", "").replace("\r", "")
    ei_lst.append(analyze_for_emails(content_nonewline))


    content_utf8 = content.decode('utf-8')
    ei_lst.append(analyze_for_emails(content_utf8))

    normal = unicodedata.normalize('NFKD', content_utf8)
    ei_lst.append(analyze_for_emails(normal))

    normal_nonewline = normal.replace('\n', '').replace("\r", '')
    ei_lst.append(analyze_for_emails(normal_nonewline))


    emails, invalids = set(), set()

    for (e, i) in ei_lst:
        emails = emails.union(e)
        invalids = invalids.union(i)

    return emails, invalids







if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "textfile"
        exit(1)



    content = open(sys.argv[1]).read()
    different_processes(content)

