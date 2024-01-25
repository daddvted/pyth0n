import os
import re
import sys


if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} filename")
    sys.exit(2)



with open(sys.argv[1], 'r') as file:
    file_content = file.read()

# input_string = """
# object network nacxialianka
#  nat (dmz,outside) static 118.123.206.66 service tcp 7782 6602 
# object network yuyinsw
#  nat (dmz,outside) static 118.123.206.60 service tcp 8080 7730 
# object network yuyin
#  nat (dmz,outside) static 118.123.206.60 service udp sip sip 
# object network yuyinsrv
#  nat (dmz,outside) static 118.123.206.60 service tcp 7005 7005 
# object network yuyin-0
#  nat (dmz,outside) static 118.123.206.62
# object network inter
#  nat (any,outside) dynamic interface
# """

pattern_host = r'^object network (.+)\n host (.+)$'
pattern_nat = r'^object network (.+)\n nat \(.+\) static (.+) service (tcp|udp) (.+)$'


nats = {}

matches = re.findall(pattern_host, file_content, re.MULTILINE)
for item in matches:
    name, local_ip = item
    nats[name] = [local_ip]

matches = re.findall(pattern_nat, file_content, re.MULTILINE)
for item in matches:
    name, public_ip, _, ports = item
    local_port, public_port = ports.strip().split()

    if name in nats.keys():
        v = nats[name]
        v.append(local_port)
        v.append(public_ip)
        v.append(public_port)

# print(nats)
for k, v in nats.items():
    v.insert(0, k)
    print(','.join(v))
