import os
import time
import random
import stringValue
from colorConsole import printc
from colorConsole import printEnableColor
import ccliCompiler as ccc
import syntaxer as syt

def doingWithARGV(argv, fileLocation, stringValue, inputType):
    fileName = ""
    if len(argv) > 3:
        for al in range(2, len(argv)):
            fileName = fileName + argv[al] + " "
        argv[2] = fileName.strip()

    # fileLocation mean DB location.
    fileList = os.listdir(fileLocation)
    if len(argv) == 1:
        helpMode()
    elif argv[1] == "-c": # Creates
        if len(argv) > 3:
            create(fileLocation, fileList, stringValue, inputType, file=argv[2])
        else:
            create(fileLocation, fileList, stringValue, inputType)
    elif argv[1] == "-s": # Show
        show(fileLocation, stringValue)
    elif argv[1] == "-r": # Read
        if len(argv) > 3:
            read(fileLocation, fileList, stringValue, inputType, file=argv[2], no=True)
        else:
            read(fileLocation, fileList, stringValue, inputType, no=True)
    elif argv[1] == "-u": # Update
        if len(argv) > 3:
            update(fileLocation, fileList, stringValue, inputType, file=argv[2])
        else:
            update(fileLocation, fileList, stringValue, inputType)
    elif argv[1] == "-d":
        if len(argv) > 3:
            delete(fileLocation, fileList, stringValue, file=argv[2])
        else:
            delete(fileLocation, fileList, stringValue)
    elif argv[1] == "-h":
        helpMode()
    elif argv[1] == "-t":
        printc("G", "Now time : ")
        printc("BL", getTime(), enter=True)
    elif argv[1] == "-rs":
        fileName = fileList[random.randint(0, len(fileList) - 1)]
        read(fileLocation, fileList, stringValue, inputType, file=fileName, no=True)
    else:
        helpMode()

def create(fileLocation, fileList, stringValue, inputType, file=-1):
    fileName = getFileName(fileList, stringValue, file=file)
    header = getHeader(inputType, fileName, stringValue)

    nowColor = "W"
    buffer = ""
    contents = []
    lineNum = 0

    contents.append("<body>")
    while True:
        buffer = input(stringValue[15])
        if buffer == ":q": # Stop write and add it to file.
            break
        elif buffer == ":c": # Change Color
            printEnableColor()
            print() # Enter
            buffer = input("색깔 선택 : ")
            nowColor = buffer
        else:
            contents.append("\t<" + str(lineNum) + ">\n" + \
                    "\t\t" + "<" + nowColor +">" + buffer + "</" + nowColor + ">" \
                    + "\n\t</" + str(lineNum) + ">")
            lineNum += 1
    contents.append("</body>")
    contents.append("</ccli>")
    toWrite = header + contents
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
    header = ccc.getHeader(fileLocation + "/" + fileName)
    contents = ccc.getFileContents(fileLocation + "/" + fileName)
    
    if inputType == "memo":
        printc("W", stringValue[8] + header["title"], enter=True)
        printc("W", stringValue[9] + header["date"], enter=True)
    elif inputType == "diary":
        printc("W", stringValue[8] + header["title"], enter=True)
        printc("W", stringValue[9] + header["date"], enter=True)
        printc("W", stringValue[10] + header["doing"], enter=True)
    elif inputType == "todo":
        printc("W", stringValue[8] + header["title"], enter=True)
        printc("W", stringValue[9] + header["date"], enter=True)

    print(stringValue[11])

    for num in range(0,len(contents)):
        for c in contents[str(num)].keys():
            color = c
        printc(c, str(contents[str(num)][color]), enter=True)

def show(fileLocation, stringValue):
    print(stringValue[3])
    printc("W", stringValue[7], enter=True)
    titleList, dateList = getFileInfor(fileLocation)
    for l in range(0, len(titleList)):
        printc("G", dateList[l] + "\t\t")
        printc("BL", titleList[l], enter=True)
    printc("W",stringValue[7], enter=True)

def getFileInfor(location):
    '''
    Get file information with it`s create days.
    '''
    fileList = os.listdir(location)
    dateList = []
    titleList = []

    for files in fileList :
        header = ccc.getHeader(location + "/" + files)
        dateList.append(header["date"])
        titleList.append(header["title"])

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
    header.append("<ccli>")
    header.append("<head>")
    header.append("\t<title>" + fileName + "</title>")
    if inputType == "memo":
        header.append("\t<date>" + getTime() + "</date>") # date
    elif inputType == "diary":
        header.append("\t<date>" + input(stringValue[5]) + \
                "</date>") # date
        header.append("\t<doing>" + input(stringValue[6]) + \
                "</doing>") # did
    elif inputType == "todo":
        header.append("\t<date>" + input(stringValue[5]) + 
                "</date>") # date
    header.append("</head>")
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
        while not isExist(fileList, fileName): # select file is exist.
            print(fileName + stringValue[1])
            fileName = input(stringValue[0])
    else:
        # if no flag is not setted...
        while isExist(fileList, fileName): # select file does not exist.
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
    return ccc.getFileContents(fileLocation + "/" + fileName)
