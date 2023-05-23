import sys
import socket

def get_hostname():
    return socket.gethostname()
    
def get_python_version():
    ver = sys.version_info
    return "{}.{}.{}".format(ver.major, ver.minor, ver.micro)
