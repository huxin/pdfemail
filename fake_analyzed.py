# fake the pdf file with one that has same md5 as name
import os
import shutil

# change to analyzed
os.chdir('analyzed')

upload_dir = 'toupload'

for f in os.listdir('.'):
    if f.endswith('.pdf') == False:
        continue

    fake_f_name = f + '.fake'
    open(fake_f_name, 'w').close()

    # move old file to upload_dir
    new_fullpath = os.path.join(upload_dir, f)
    print "Move", f, "to", new_fullpath, 'create', fake_f_name
    shutil.move(f, new_fullpath)
