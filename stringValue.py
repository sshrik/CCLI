# 0 = simple input // get file name
# 1 = evalid input // not exist or deleted file name
# 2 = finished. // finished deleted.
# 3 = to show. // file list below
# 4 = input name // what is the name of memo / diary ...
# 5 = input date // what is the date of memo / diary ...
# 6 = input did // what did you do at diary ...
# 7 = "Date============\tTitle==============================="
# 8 = "Name : "
# 9 = "Date : "
# 10 = "Did : "
# 11 = "Contents "
# 12 = "Canceled..."
# 13 = "Given..."
# 14 = "To change"
# 15 = "Contents (:q to exit) : "

confLocation = "C:/workspace/bin"
confFile = "configure"
memoLocation = "C:/workspace/memoLocation"
diaryLocation = "C:/workspace/diaryLocation"
todoLocation = "C:/workspace/todoLocation"

stringValue = [ "파일의 이름을 입력하십시오 : " # 0
    , "잘못된 파일 이름입니다." # 1
    , "파일의 삭제가 끝났습니다." # 2
    , "파일 리스트" # 3
    , "입력할 메모 / 일기 / 일정의 이름을 입력하시오." # 4
    , "입력할 일기 / 일정의 일자를 입력하시오." # 5
    , "입력할 일기의 대표적인 한 일을 입력하시오." # 6
    , "일자============\t제목===============================" # 7
    , "제목 : " # 8
    , "일자 : " # 9
    , "한일 : " # 10
    , "내용 : " # 11
    , "취소됨..." # 12
    , "원래의 내용" # 13
    , "바꿀 내용" # 14
    , "내용 (:q 로 취소) : " # 15
    , "파일을 삭제하시겠습니까?" # 16
    ]
ccli = ["메모, 일기, 일정을 표시하는 CLI 환경의 도움말입니다."
    , "언어 설정을 하시려면 -l"
    , "db 설정을 하시려면 -d"
    , "alias 단축키 설정을 하시려면 -a를 누르세요."
    ]
helpLang = [ "-c = 생성하기. [fileName]을 바로 입력하면 바로 생성 할 수 있습니다."
    , "-r = 읽기. [fileName] 을 바로 입력하면 바로 읽을수 있습니다."
    , "-u = 업데이트. [fileName] 을 바로 입력하면 바로 업데이트 할 수 있습니다."
    , "-d = 삭제하기. [fileName] 을 바로 입력하면 바로 삭제 할 수 있습니다."
    , "-h = 도움말."
    , "-t = 현재 컴퓨터의 시각."
    , "-rs = 아무거나 보기."
]
lang = "kr"

def readConf(fileLocation, fileName):
    lines = readFile(fileLocation, fileName + "conf")
    lang = lines[0]
    
    lines = readFile(fileLocation, fileName + "db")
    memoLocation = lines[0]
    diaryLocation = lines[1]
    todoLocation = lines[2]

    stringValue = readFile(fileLocation, fileName + "sv")
    ccli = readFile(fileLocation, fileName + "cl")
    helpLang = readFile(fileLocation, fileName + "hl")

def readFile(fileLocation, fileName):
    f = open(fileLocation + "/" + fileName, "r")
    lines = f.readlines()
    returnValue = []

    for l in lines:
        returnValue.append(l.split("\n")[0])
    f.close()
    return returnValue

readConf(confLocation, confFile)