import re
import syntaxer as syt

def ccliAnalyzer(fileName):
    '''
    Parse input data to tags and contents.
    ex )
        input = <head><title>Today`s work!</title></head>
        return = {head : {"title" : "Today`s work"}}
    ARGS :
        rawInputData - raw data of CCLI files.
    RETURN :
        tags - contents dictionary.
    RAISE :
        tagsNotMatchError = input tags are not matched.
    '''
    f = open(fileName, "r")
    lines = f.readlines()
    f.close()
   
    for l in range(0, len(lines)):
       lines[l] = lines[l].split("\n")[0]

    # Init tempfiles.
    conList = getContents([], lines)
#    print(conList)
    return conList

def ccliCompile(fileName, echo="on"):
    '''
    Check syntax of file.
    '''
    error = 1
    f = open(fileName, "r")
    lines = f.readlines()
    f.close()
    
    stack = []
    for l in range(0, len(lines)):
        tags = syt.getTagList(lines[l])
        
        # Doing stack job with tags.
        for tag in tags:
            if syt.getTagType(tag) == "start":
                error = syt.bigStartFunction(stack, tag, l+1, lines[l].split("\n")[0])
            else:
                error = syt.bigFinishFunction(stack, tag, l+1, lines[l].split("\n")[0])
    return error

def getHeader(fileName):
    '''
    get ccli files header.
    '''
    con = ccliAnalyzer(fileName)
    return con["ccli"]["head"]

def getFileContents(fileName):
    '''
    get ccli files contents.
    '''
    con = ccliAnalyzer(fileName)
    return con["ccli"]["body"]

def getContents(stack, lines, startL=0):
    '''
    get all tag-contents set of file.
    '''
    l = startL

    retTemp = {}

    while l in range(startL, len(lines)):
        tags = syt.getTagList(lines[l])
#        print("====================================================")
#        print("Now line : " + lines[l])
#        print("Now Tags : " + str(tags))
#        print("Now Stck : " + str(stack))
#        print("Now Dick : " + str(retTemp))
#        print("====================================================")
        for tag in tags:
            if syt.getTagType(tag) == "start":
                syt.stackPush(stack, tag)
                if syt.getMatchTag(tag) in tags:
                    # If one line has start and end tag...
                    src = syt.stackPop(stack)
                    con = syt.getTagContents(src, syt.getMatchTag(src), lines[l])
                    retTemp[syt.getRawTag(tag)] = con
                    break
                else:
                    con, l = getContents(stack, lines, startL=l+1)
                    retTemp[syt.getRawTag(tag)] = con
            else:
                # if tag is finishing tag...
                src = syt.stackPop(stack)
                if syt.isTagSame(src, tag):
                    return retTemp, l
                else:
                    syt.stackPush(stack, src)
                    return retTemp, l
        l += 1

    return retTemp


