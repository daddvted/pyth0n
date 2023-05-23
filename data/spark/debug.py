import os
import sys
import socket
import pkg_resources
from pyspark.sql import SparkSession


spark = SparkSession.builder.appName("Debug").getOrCreate()
#spark = SparkSession.builder.master(master).appName("EnvDemo").getOrCreate()

ver = sys.version_info
print("====== Python Info ======")

print("Hostname: {}".format(socket.gethostname()))
print("Python Version: {}.{}.{}".format(ver.major, ver.minor, ver.micro)) 
print("Working directory: {}".format(os.getcwd()))
for f in os.listdir(os.getcwd()):
    print(f)

print("====== sys.path ======")
for path in sys.path:
    print(path)

print("==============================================")

installed = pkg_resources.working_set
installed_pkgs = sorted(["{} == {}".format(pkg.key, pkg.version) for pkg in pkg_resources.working_set])

for p in installed_pkgs:
    print(p)

print("\n\n")

spark.stop()
