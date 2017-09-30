
#!/usr/bin/env python

import os
def test_port(port_num = 4422):
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	return sock.connect_ex(('127.0.0.1', port_num)) ==0


cmd = "ssh -N -f -L 4422:localhost:4000 gcp"

if test_port() == False:
	os.system(cmd)