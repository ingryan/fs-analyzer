import os
import sys

from collections import OrderedDict

def scan_fs(excludelist, *args):
    #topdir=args[0]
    topdir="C:\\"

    maxsize = 0
    fattestdir = "C:"

    results = {}
    resultscutoff = 10**8

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


        if dirsum>resultscutoff:
            dirsum = dirsum // 10**6 #stored as megabytes
            print("{0} has size {1}MB".format(dirpath, dirsum))
            results[dirpath]=dirsum

            if dirsum>maxsize:
                maxsize = dirsum #also stored as megabytes
                fattestdir = dirpath

    print("{0} is the winner with size {1}MB".format(fattestdir, maxsize))
    return results

def print_error(exceptionobject):
    print(str(exceptionobject))

def print_results(outdict, filename=None):
    if not filename:
        filename = os.getcwd()+"/logs/output.txt"

    if not os.path.exists(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))

    sorted_output = OrderedDict(sorted(outdict.items(), key=lambda x: x[1], reverse=True))
    print("Writing to {0}".format(filename))

    with open(filename, 'w+') as log:
        for path in sorted_output:
            log.write("{0}: {1}MB \n".format(path, sorted_output[path]))





exclusions = {'Windows',
            'ProgramData',
            'C:/Users/Default',
            'AppData'
            }

pathdict = scan_fs(exclusions)
print_results(pathdict, filename='C:/proglogs/out.txt')