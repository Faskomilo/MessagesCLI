import os
from babel.messages.catalog.Catalog import check

class CLImessageClient(object):
    __message = ""
    option = ""
    _repeated = 0

    def __init__(self):
        print("")

    def DictionaryGeneration(self, message):
        messageList = message.split("\n\n")
        messageDic = {}
        repeatedDic = {}
        a = 0
        for x in range(len(messageList)):
            a = a +1
            wholeLine = ""
            wholeLine = messageList[x]
            commentsLine = ""
            msgidLine = ""
            msgstrLine = ""
            msgid = ""
            msgstr = ""
            try:
                wholeLine = messageList[x]
                if "#" in wholeLine:
                    if "#~" in wholeLine:
                        commentsLine = ""
                        msgidLine = wholeLine[:wholeLine.index("\n#~ msgstr")]
                        msgstrLine = wholeLine[wholeLine.index("#~ msgstr"):]
                        msgid = msgidLine[msgidLine.index("\"")+1:-1]
                        msgstr = msgstrLine[msgstrLine.index("\"")+1:-1]
                    else:
                        commentsLine = wholeLine[:wholeLine.index("\nmsgid")]
                        msgidLine = wholeLine[wholeLine.index("ms"):wholeLine.index("\nmsgstr")]
                        msgstrLine = wholeLine[wholeLine.index("msgstr"):]
                        msgid = msgidLine[msgidLine.index("\"")+1:-1]
                        msgstr = msgstrLine[msgstrLine.index("\"")+1:-1]
                else:
                    commentsLine = ""
                    msgidLine = wholeLine[:wholeLine.index("\nmsgstr")]
                    msgstrLine = wholeLine[wholeLine.index("msgstr"):]
                    msgid = msgidLine[msgidLine.index("\"")+1:-1]
                    msgstr = msgstrLine[msgstrLine.index("\"")+1:-1]
            except Exception:
                print("error inesperado en" + wholeLine)
            if msgid in messageDic:
                if "#~" in msgidLine:
                    index = message.index(msgidLine[3:])
                    secondIndex = message.index(msgidLine[3:],index + 2)
                else:
                    index = message.index(msgidLine)
                    secondIndex = message.index(msgidLine,index + 2)
                firstInstance = len(message[:index].split("\n"))
                secondInstance = len(message[:secondIndex].split("\n"))
                repeatedDic[msgid] = {"Comments" : commentsLine, "msgstr" : msgstr, 
                    "Instance 1" : firstInstance,
                    "Instance 2" : secondInstance}
            else:
                messageDic[msgid] = {"Comments" : commentsLine, "msgstr" : msgstr}
            _repeated = len(repeatedDic)
        return messageDic

class Menu(object):
        def __init__(self):
            print("Welcome, choose the language you want to modify or check the translation of:")

        def choose(self):
            print "Escoja una opcion:"
            print "1"

class PathHandler(object):
        pathLanguages = os.path.join("languages")

        def listLanguages(self):
            options = os.listdir(os.path.join(".", self.pathLanguages)) 
            return options

class SpecificRecord(object):
    pass

class FileManager(object):
    def readfile(self, language):
        path = os.path.join("languages", language, "LC_MESSAGES", "messages.po")
        messages = open(path).read()
        return messages

    def writefile(self, language, message):
        path = os.path.join("languages", language, "LC_MESSAGES", "messages.po")
        file = open(path)
        file.write(message)

    def checkfile(self,file):
        Catalog.check()


CLImessageClient = CLImessageClient()
Menu = Menu()
PathHandler = PathHandler()
SpecificRecord = SpecificRecord()
FileManager = FileManager()
_message = FileManager.readfile("es")
#CLImessageClient.DictionaryGeneration(_message)
print(CLImessageClient.DictionaryGeneration(_message))
