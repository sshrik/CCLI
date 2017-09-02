import os
import time
import random
import stringValue

def doingWithARGV(argv, fileLocation, stringValue, inputType):
    # fileLocation mean DB location.
    fileList = os.listdir(fileLocation)
    if len(argv) == 1:
        helpMode()
    elif argv[1] == "-c": # Creates
        if len(argv) == 3:
            create(fileLocation, fileList, stringValue, inputType, file=argv[2])
        else:
            create(fileLocation, fileList, stringValue, inputType)
    elif argv[1] == "-s": # Show
        show(fileLocation, stringValue)
    elif argv[1] == "-r": # Read
        if len(argv) == 3:
            read(fileLocation, fileList, stringValue, inputType, file=argv[2], no=True)
        else:
            read(fileLocation, fileList, stringValue, inputType, no=True)
    elif argv[1] == "-u": # Update
        if len(argv) == 3:
            update(fileLocation, fileList, stringValue, inputType, file=argv[2])
        else:
            update(fileLocation, fileList, stringValue, inputType)
    elif argv[1] == "-d":
        if len(argv) == 3:
            delete(fileLocation, fileList, stringValue, file=argv[2])
        else:
            delete(fileLocation, stringValue, fileList)
    elif argv[1] == "-h":
        helpMode()
    elif argv[1] == "-t":
        print("Now time : " + getTime())
    elif argv[1] == "-rs":
        fileName = fileList[random.randint(0, len(fileList) - 1)]
        read(fileLocation, fileList, stringValue, inputType, file=fileName, no=True)
    else:
        helpMode()

def create(fileLocation, fileList, stringValue, inputType, file=-1):
    fileName = getFileName(fileList, stringValue, file=file)
    header = getHeader(inputType, fileName, stringValue)

    buffer = ""
    memoContents = []
    while True:
        buffer = input(stringValue[15])
        if buffer == ":q": # Stop write and add it to file.
            break
        else:
            memoContents.append(buffer)
    toWrite = header + memoContents
    writeFile(fileLocation, fileName, toWrite)

def update(fileLocation, fileList, stringValue, inputType, file=-1):
    fileName = getFileName(fileList, stringValue, file=file, no=True)
    print(stringValue[13])
    read(fileLocation, fileList, stringValue, inputType, file=fileName, no=True)
    print(stringValue[14])
    delete(fileLocation, fileList, stringValue, file=fileName, go=True)
    fileList = os.listdir(fileLocation)
    create(fileLocation, fileList, stringValue, inputType, file=fileName)
    
def delete(fileLocation, fileList, stringValue, file=-1, go=False):
    fileName = getFileName(fileList, stringValue, file=file, no=True)
    if go:
        os.remove(fileLocation + "/" + fileName)
    else:
        print(fileName + stringValue[16])
        y = input("y / n")
        if y == "y":
            os.remove(fileLocation + "/" + fileName)
            print(fileName + stringValue[2])
        else :
            print(stringValue[12])

def read(fileLocation, fileList, stringValue, inputType, file=-1, no=False):
    fileName = getFileName(fileList, stringValue, file=file, no=no)
    lines = getFileContents(fileLocation, fileName)

    if inputType == "memo":
        print(stringValue[8] + lines[0])
        print(stringValue[9] + lines[1])
        contents = lines[2:-1]
    elif inputType == "diary":
        print(stringValue[8] + lines[0])
        print(stringValue[9] + lines[1])
        print(stringValue[10] + lines[2])
        contents = lines[3:-1]
    elif inputType == "todo":
        print(stringValue[8] + lines[0])
        print(stringValue[9] + lines[1])
        contents = lines[2:-1]

    for c in contents:
        print(stringValue[11] + c)

def show(fileLocation, stringValue):
    print(stringValue[3])
    print(stringValue[7])
    titleList, dateList = getFileInfor(fileLocation)
    for l in range(0, len(titleList)):
        print(dateList[l] + "\t" + titleList[l])
    print(stringValue[7])
    
def getFileInfor(location):
    '''
    Get file information of date and name.
    Return 2 list of date and name.
    '''
    fileList = os.listdir(location)
    dateList = []
    titleList = []

    for files in fileList:
        f = open(location + "/" + files)
        titleList.append(f.readline().split("\n")[0])
        dateList.append(f.readline().split("\n")[0])
    # File all have name - date format at first 2 lines.

    for t1 in range(0, len(titleList)):
        for t2 in range(t1, len(titleList)):
            if dateList[t1] > dateList[t2]:
                temp = dateList[t1]
                dateList[t1] = dateList[t2]
                dateList[t2] = temp

                temp = titleList[t1]
                titleList[t1] = titleList[t2]
                titleList[t2] = temp

    return titleList, dateList

def getHeader(inputType, fileName, stringValue):
    header = []
    header.append(fileName)
    if inputType == "memo":
        header.append(getTime()) # date
    elif inputType == "diary":
        header.append(input(stringValue[5])) # date
        header.append(input(stringValue[6])) # did
    elif inputType == "todo":
        header.append(input(stringValue[5])) # date
    return header

def getTime():
    now = time.localtime()
    return str(now.tm_year) + "." + str(now.tm_mon) + "." + str(now.tm_mday) + "." + str(now.tm_hour) + "." + str(now.tm_min)

def isExist(fileList, fileName):
    return fileName in fileList

def getFileName(fileList, stringValue, file=-1, no=False):
    if file == -1:
        fileName = input(stringValue[0])
    else:
        fileName = file
    if no:
        # If no flag is setted...
        while not isExist(fileList, fileName):
            print(fileName + stringValue[1])
            fileName = input(stringValue[0])
    else:
        # if no flag is not setted...
        while isExist(fileList, fileName):
            print(fileName + stringValue[1])
            fileName = input(stringValue[0])

    return fileName

def helpMode():
    for hl in stringValue.helpLang:
        print(hl)

def writeFile(fileLocation, fileName, lines):
    f = open(fileLocation + "/" + fileName, 'w')
    for line in lines:
        f.write(line + "\n")
    f.close()

def getFileContents(fileLocation, fileName):
    f = open(fileLocation + "/" + fileName, "r")
    lines = f.readlines()
    returnValue = []
    for l in lines:
        returnValue.append(l.split("\n")[0])
    f.close()
    return returnValue
