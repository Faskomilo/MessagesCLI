import os, time
from babel.messages.catalog import Message

class CLImessageClient(object):

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
            self.__repeated = len(repeatedDic)
        return messageDic

class Menu(object):
    def __init__(self):
        self.language = "en"

    def listLanguages(self,pathLanguages):
        options = os.listdir(os.path.join(".", pathLanguages)) 
        return options

    def showLanguageMenu(self, listLanguages):
        print ("Which Language do you wish to change?:")
        for x in range(len(listLanguages)):
            string = str(x + 1) + ": " + listLanguages[x]
            print(string)
        print ("0: Exit")
        self.option = input("Write the number of your choice: ")

    def showMenu(self, language):
        print ("Choose what would you like to do with the \"" + language + "\" messages:")
        print ("1: Add a message")
        print ("2: Look for a translation or comment with the message id")
        print ("3: See all")
        print ("4: Delete a message (message id, translation and comment)")
        print ("5: Create new empty Language")
        print ("0: Exit")
        self.option = input("Write the number of your choice: ")

class PathHandler(object):
        def buildPath(self, language):
            path = os.path.join("languages", language, "LC_MESSAGES", "messages.po")
            return path

class SpecificRecord(object):
    pass

class FileManager(object):
    def readfile(self, language, path):
        messages = open(path).read()
        return messages

    def writefile(self, language, message, path):
        file = open(path)
        file.write(message)

    def compile(self, pathToEs):
        os.system('-d' + pathToEs)

class Runner(CLImessageClient,Menu,PathHandler,SpecificRecord,FileManager):
    pathLanguages = os.path.join("languages")
    __path = ""
    __listLanguages = []
    language = "es"
    option = 1
    __message = ""
    option = ""
    repeated = 0

    def __init__(self):
        
        while self.option != 0:
            if os.name == 'nt':
                _ = os.system('cls') 
            else: 
                _ = os.system('clear') 
            self.__listLanguages = self.listLanguages(self.pathLanguages)
            self.showLanguageMenu(self.__listLanguages)
            if self.option != 0:
                self.showMenu("language")
                #print(self.option)

if __name__ == "__main__":
    Runner()

