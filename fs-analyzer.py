import os
import sys

def scan_fs(excludelist, *args):
    #topdir=args[0]
    topdir="C:/"

    maxsize = 0
    fattestdir = "C:"

    for dirpath, dirnames, filenames in os.walk(topdir,
                                                topdown=True,
                                                onerror=print_error,
                                                followlinks=False):

        dirnames[:] = [x for x in dirnames if x not in excludelist]
        dirsum = 0
        for name in filenames:
            try:
                dirsum += os.path.getsize(os.path.join(dirpath, name))
            except (PermissionError, OSError) as err:
                print(str(err))
                continue
            except Exception as err:
                print(str(err))
                exit()
            except FileNotFoundError as err:
                print("File not found, skipping")


        if dirsum>100000000:
            mbdirsum = dirsum // 10**6
            print("{0} has size {1}MB".format(dirpath, mbdirsum))

        if dirsum>maxsize:
            maxsize = dirsum
            fattestdir = dirpath

    print("{0} is the winner with size {1}MB".format(fattestdir, maxsize//10**6))

def print_error(exceptionobject):
    print(str(exceptionobject))

exclusions = {'Windows',
            'ProgramData',
            'C:/Users/Default',
            'AppData'
            }


scan_fs(exclusions)