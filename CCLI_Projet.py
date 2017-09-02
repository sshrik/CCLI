import os
import sys
import stringValue

def helpMode():
    for ccl in stringValue.ccli:
        print(ccl)

if len(sys.argv) == 1:
    helpMode()
elif sys.atgv[1] == "-h":
    helpMode()
elif sys.atgv[1] == "-l":
    helpMode()
elif sys.atgv[1] == "-d":
    helpMode()
elif sys.atgv[1] == "-a":
    helpMode()
else :
    helpMode()
