import os



for d in os.listdir('.'):
    if not os.path.isdir(d):
        continue
        
    cmd = 'tar czvf {}.tar.gz {}'.format(d, d)
    print cmd
    os.system(cmd)



