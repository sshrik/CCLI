'''
XML or HTML, CCML(CCLI HTML) File syntax analyzer. Check only simple "Gemizip" CFG files.
'''
import re

tagDefList = [  "key_value_tag",        # If key="value" is correctly.
                "big_start_tag",        # If <tag>
                "big_finish_tag",       # If <tag/>
                "not_accessible_key",   # If key is not grammatically correct.
                "not_accessible_value", # If value is not grammatically correct.
                "not_accessible_pair",  # If key-value is not pair.
                "comment_tag",          # If start with # or start with <!-- and end with -->
                "unnecessary_information", # If finished with > and added more data.
             ]

errorMessage = {
                    "not_match_tag" : "<tag> does not matching.",
                    "not_accessible_key" : "key value is invalid.",
                    "not_accessible_value" : "value value is invalid.",
                    "not_accessible_pair" : "key value pair does not matching.",
                    "unnecessary_information" : "unnecessary information is at line.",
               } 

def stackPush(element, stack):
    # Push to stack.
    element.append(stack)

def stackPop(stack):
    # Pop from stack.
    if len(stack) != 0:
        # get stack element and delete it.
        returnValue = stack[-1]
        del stack[-1]
        return returnValue
    else:
        # if empty, return -1
        return -1

def isTagSame(src, dst):
    # Check <src> and <dst/> is same.
    return src == getMatchTag(dst)

def getTagList(tagString):
    # Input line and output \t or " " parsed tag and word.
    '''
    get tags from input data.
    '''
    tagApp = re.compile('<[a-zA-Z0-9/]+>')
    rawTags = tagApp.findall(tagString)

    return rawTags

def getMatchTag(tag):
    '''
    get matched tag with input.
    '''
    if tag.startswith("</") and tag.endswith(">"):
        # like </ head > values.
        ret = re.compile("/")
        return ret.sub("", tag)

    elif tag.startswith("<") and tag.endswith("/>"):
        ret = re.compile("/")
        return ret.sub("", tag)

    elif tag.startswith("<") and tag.endswith(">"):
        ret = re.compile("<")
        return ret.sub("</", tag)

def getRawTag(tag):
    ret = re.compile("<|>|/")
    return ret.sub("", tag)

def getTagContents(stag, ftag, line):
    '''
    return tag`s contents
    '''
    ret = re.compile(stag + ".*" + ftag)
    tagReduce = re.compile(stag + "|" + ftag)
    con = ret.findall(line)[0]

    return tagReduce.sub("", con)

def getTagType(tag):
    '''
    get if tag is finish or start.
    '''
    if tag.startswith("<") and tag.endswith("/>"):
        return "finish"
    elif tag.startswith("</") and tag.endswith(">"):
        return "finish"
    else:
        return "start"

def keyValueFunction(stack, word, lineNumber, nowLine):
    # If key-value is fine, pass.
    ''' '''

def bigStartFunction(stack, word, lineNumber, nowLine):
    # push into stack and pass.
    stackPush(stack, word)
    return 1

def bigFinishFunction(stack, word, lineNumber, nowLine):
    # pop from stack. if not same tag-values, raise error.
    src = stackPop(stack)
    if src == -1:
        # Stack is empty, so doesn`t match.
        errorPrint(nowLine, word + " not have pair.", lineNumber, 'not_match_tag')
        return -1
    else:
        # Stack is not empty, check tag is same.
        if(isTagSame(src, word)):
            return 1
        else:
            errorPrint(nowLine, word + " != " + src, lineNumber, 'not_match_tag')
            return -1

def notAccKeyFunction(stack, word, lineNumber, nowLine):
    # key value is invalid. print word and raise error.
    errorPirnt(nowLine, word, lineNumber, 'not_accessible_key')

def notAccValueFunction(stack, word, lineNumber, nowLine):
    # value value is invalid. print word and raise error.
    errorPrint(nowLine, word, lineNumber, 'not_accessible_value')

def notAccPairFunction(stack, word, lineNumber, nowLine):
    # Pair value is invalid. print word and raise error.
    errorPrint(nowLine, word, lineNumber, 'not_accessible_pair')

def commentFunction(stack, word, lineNumber, nowLine):
    # Comment tag, pass.
    ''' '''

def unnecessaryInfoFunction(stack, word, lineNumber, nowLine):
    # Unnecessary Information is added. It may warn.
    warnPrint(nowLine, word, lineNumber, 'unnecessary_information')

def errorPrint(errorLine, errorWord, errorLineNumber, errorDesc):
    # Print Error Message. Line = Y, errorWord = S, errorLineNumber = Y, errorDesc = R
    printc("S", "At line [")
    printc("Y", "%d" % errorLineNumber)
    printc("S", "] : ")
    printc("G", errorLine + "\n")
   
    printc("S", "Error occured[")
    printc("R", errorDesc)
    printc("S", "] : ")
    printc("R", errorMessage[errorDesc] + "\n" )
     
    printc("Y", errorWord + "\n\n")
    
def warnPrint(warnLine, warnWord, warnLineNumber, warnDesc):
    # Print Warning Message. Line = Y, warnWord = S, warnLineNumber = Y, warnDesc = BL
    printc("S", "At line [")
    printc("Y", "%d" % warnLineNumber)
    printc("S", "] : ")
    printc("Y", warnWord)
    printc("S", " in ")
    printc("G", warnLine + "\n")
    printc("S", "Warning [")
    printc("BL", warnDesc)
    printc("S", "] : ")
    printc("BL", errorMessage[warnDesc] + "\n\n" )

def printc(pColor, printStr):
    '''
    To use printc, printc("WB", "Hello World!"), or printc("BR", "ETC...").
    ARGS :
        pColor      = print color.
        printStr    = want to printing strring,
    RETURNS :
        nothing.
    RAISE :
        NotColorException
    '''
    # Definition List.
    colorList = ["WB", "R", "G", "Y", "BL", "C", "WBL", "W",\
            "BR", "BG", "BY", "BBL", "BC", "BWBL", "BW",\
            "UL", "BLK", "S"]
    colorInt = [30, 31, 32, 33, 34, 35, 36, 37, \
            41, 42, 43, 44, 45, 46, 47,
            4, 5, 0]

    # Color Printing Prefix and Postfix.
    colorPrefix = "\x1b[1;"
    colorPostfix = "\x1b[1;m"
    
    # If not color in list...
    if pColor not in colorList:
        raise NotColorException
        print(printStr)

    # Make Color.
    color = str(colorInt[colorList.index(pColor)])
    color = color + "m"

    print(colorPrefix + color + printStr + colorPostfix, end="")


# Tag Fucntion definition.
tagFuncList = [ keyValueFunction,
                bigStartFunction,
                bigFinishFunction,
                notAccKeyFunction,
                notAccValueFunction,
                notAccPairFunction,
                commentFunction,
                unnecessaryInfoFunction,
              ]

