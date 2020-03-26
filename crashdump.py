import sys
import subprocess

if len(sys.argv) < 3:
    print("usage: {} logfile elf_file".format(sys.argv[0]))
    exit(1)

for l in open(sys.argv[1]):
    begin = l.find("[<")
    if begin < 0:
        continue
    end = l.find(">]")
    if end < 0:
        continue
    if begin >= end:
        continue
    addr = l[begin + 2: end]
    commands = ["addr2line", "-a", addr, "-e",  sys.argv[2]]
    # print(commands)
    res = subprocess.Popen(commands,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = res.communicate()
    if stderr:
        print(stderr.decode())
        break
    print("{}: {}".format(
        stdout.decode().splitlines()[1],
        l[begin:].strip()))
