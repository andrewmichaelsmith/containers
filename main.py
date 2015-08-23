#Credit: http://stackoverflow.com/questions/13373629/clone-process-support-in-python
#http://crosbymichael.com/creating-containers-part-1.html
#http://lxr.free-electrons.com/source/include/linux/sched.h?v=3.4
from ctypes import (
    CDLL,
    c_void_p,
    c_int,
    c_char_p,
    cast,
    CFUNCTYPE,
)

import time
import subprocess
import os

PARENT = "Parent"
CHILD = "Child"

CLONE_NEWPID = 0x20000000
CLONE_NEWNET = 0x40000000
CLONE_NEWUSER = 0x10000000
CLONE_NEWIPC = 0x08000000
CLONE_NEWUTS = 0x04000000

flags = CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWUSER \
    | CLONE_NEWIPC | CLONE_NEWUTS

libc = CDLL("libc.so.6")

# We need the top of the stack.
stack = c_char_p(" " * 8096)
stack_top = c_void_p(cast(stack, c_void_p).value + 8096)


def print_pid(ident):
    print "%s PID: %s" % (ident, os.getpid())

def namespaced_func():
    print_pid(CHILD)

    #This shows loads, why?
    #Because it can still see proc
    #print subprocess.check_output(['ps', 'aux'])
    return 0


def start_stats():
    print_pid(PARENT)

def app():
    # Conver function to c type returning an integer.
    f_c = CFUNCTYPE(c_int)(namespaced_func)

    # Call clone with the NEWPID Flag

    val = libc.clone(f_c, stack_top, CLONE_NEWPID)


def run():
    start_stats()
    app()

if __name__ == "__main__":
    run()

