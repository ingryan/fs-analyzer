import os
import sys

def scan_fs(*args):
    #topdir=args[0]
    topdir="C:/"

    maxsize = 0
    fattestdir = "C:"

    for dirpath, dirnames, filenames in os.walk(topdir,
                                                topdown=True,
                                                onerror=print_error,
                                                followlinks=False):
        newsum = 0
        for name in filenames:
            try:
                newsum += os.path.getsize(os.path.join(dirpath, name))
            except (PermissionError, OSError) as err:
                print(str(err))
                continue
            except Exception as err:
                print(str(err))
                exit()
            except FileNotFoundError as err:
                print("File not found, skipping")


        if newsum>100000000:
            print("{0} has size {1}B".format(dirpath, newsum))

        if newsum>maxsize:
            maxsize = newsum
            fattestdir = dirpath

    print("{0} is the winner with size {1}B".format(fattestdir, maxsize))

def print_error(exceptionobject):
    print(str(exceptionobject))

scan_fs()