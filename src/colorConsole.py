colorList = ["WB", "R", "G", "Y", "BL", "C", "WBL", "W",\
            "BR", "BG", "BY", "BBL", "BC", "BWBL", "BW",\
            "UL", "BLK", "NL", "WBB", "WBR", "WBG", "WBY", "WBBL", "WBC", "WBWBL", "WBW"]
colorInt = [30, 31, 32, 33, 34, 35, 36, 37, \
            41, 42, 43, 44, 45, 46, 47,
            4, 5, 2, 100, 101, 102, 103, 104, 105, 106, 107]

def printEnableColor():
    for color in colorList:
        printc(color, color + " ")

def printc(pColor, printStr, enter=False):
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
    if enter:
        print(colorPrefix + color + printStr + colorPostfix)
    else:
        print(colorPrefix + color + printStr + colorPostfix, end="")
