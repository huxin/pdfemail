#!/usr/bin/env python
import os
import sys
import shutil

if len(sys.argv) < 4:
    print "Usage:", sys.argv[0], "<src dir> <dst_dir> <cnt>"
    exit(1)

src_dir, dst_dir, mov_cnt = sys.argv[1:4]

cnt = 0
for f in os.listdir(src_dir):
    if not f.endswith('.pdf'):
        continue

    src_full = os.path.join(src_dir, f)
    dst_full = os.path.join(dst_dir, f)

    shutil.move(src_full, dst_full)
    cnt += 1

    if cnt >= int(mov_cnt):
        break

print "Moved:", cnt
