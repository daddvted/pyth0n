import os
import sys
import socket
import example.util
from pyspark.sql import SparkSession
from example.http.url import detect_url


spark = SparkSession.builder.appName("PythonExample").getOrCreate()

print("\n")
print("====================================")
print("======     Python Example     ======")
print("====================================")

print("Hostname: {}".format(example.util.get_hostname()))
print("Python Version: {}".format(example.util.get_python_version())) 
print("Working directory: {}".format(os.getcwd()))
print("\nFiles in working directory:")
for f in os.listdir(os.getcwd()):
    print(f)

print("\nSys path:")
for path in sys.path:
    print(path)

url = "https://python.org"
print("\nStatus of {}:".format(url))
print(detect_url(url))

print("====================================")

print("\n")

spark.stop()
