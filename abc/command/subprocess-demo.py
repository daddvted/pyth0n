import subprocess

# cmd = 'sleep 3;ls a b'
cmd = 'ls a b'

obj = subprocess.run(cmd.split(), capture_output=True)
print(obj)

# obj = subprocess.run(cmd, shell=True, capture_output=True)
# print(type(obj))
# print(obj.stderr)

