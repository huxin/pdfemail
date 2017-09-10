import os
import shutil

for f in os.listdir('.'):
    if f.endswith('.pdf') == False:
        continue

    d = f[0]

    if not os.path.exists(d):
        os.mkdir(d)

    shutil.move(f, os.path.join(d, f))

