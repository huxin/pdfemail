import os
import hashlib
import shutil

for f in os.listdir('.'):
    if not f.endswith('.pdf'):
        continue

    md5 = hashlib.md5(open(f, 'rb').read()).hexdigest()
    print f, "->", md5+'.pdf'
    shutil.move(f, md5+'.pdf')