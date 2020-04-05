import sys
import subprocess
import os

if len(sys.argv) < 3:
    print("usage: {} logfile elf_file_or_path".format(sys.argv[0]))
    exit(1)


def address_from_crash(lines, elf):
    """yield tuple of address and original line
    """
    for l in lines:
        begin = l.find("[<")
        if begin < 0:
            continue
        end = l.find(">]")
        if end < 0:
            continue
        if begin >= end:
            continue
        yield l[begin + 2: end], l[begin:], elf


def address_from_trace(lines, path):
    """yield tuple of address and original line
    """
    for l in lines:
        begin = l.find(" pc ")
        if begin < 0:
            continue
        end = l.find(" ", begin+4)
        if end < 0:
            continue
        if begin >= end:
            continue
        elf_begin = l.find("/", end)
        if elf_begin < 0:
            continue
        elf_end = l.find(" ", elf_begin)
        if elf_end < 0:
            continue
        elf = os.path.join(path, l[elf_begin+1: elf_end])
        yield l[begin + 4: end], l[begin:], elf


def print_crash_dump(addr, l, elf):
    commands = ["addr2line", "-a", addr, "-e",  elf]
    #print(' '.join(commands))
    res = subprocess.Popen(commands,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = res.communicate()
    if stderr:
        print(stderr.decode())
        return
    so = stdout.decode().splitlines()
    # print(so)
    if len(so) != 2:
        print(so)
        return
    print("{}: {}".format(so[1], l), end="")


lines = open(sys.argv[1]).readlines()
e = sys.argv[2]

c = (sum(1 for _ in address_from_crash(lines, e)), address_from_crash)
t = (sum(1 for _ in address_from_trace(lines, e)), address_from_trace)

if not c[0] and not t[0]:
    print("failed to parse addresses")
    exit(0)

s = max(c, t)

for addr, l, elf in s[1](lines, sys.argv[2]):
    print_crash_dump(addr, l, elf)
