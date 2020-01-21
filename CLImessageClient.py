import os, time
from babel.messages.catalog import Message

class CLImessageClient(object):
    def __init__(self):
        print("")

    def clearScreen(self):
        if os.name == 'nt':
            _ = os.system('cls') 
        else: 
            _ = os.system('clear') 

    def addLanguage(self):
        language = ""
        language = raw_input("Which language do you wish to add? ")
        if any(char.isdigit() for char in language):
            print("ok")
        return language

    def dictionaryToText(self, messages):
        messagesDictionary = messages
        #for x in range(len(messagesDictionary)):
                
        pass

    def addMessage(self, message, language):
        errors = 1
        while errors == 1:
            try:
                newMsgid = raw_input("Write a message (a message in English that can be translated): ")
                if any(char.isdigit() for char in newMsgid):
                    raise Exception("No numbers")
                errors = 0
            except:
                print("Message id should not contain numbers")
        errors = 1
        while errors == 1:
            try:
                newMsgstr = raw_input("Write the translation of the message on " + language + ": ")
                if any(char.isdigit() for char in newMsgstr):
                    raise Exception("No numbers")
                errors = 0
            except:
                print("Message translation should not contain numbers")
        while errors == 1:
            try:
                newCommentsLine = raw_input("Write a comment on where it's gonna be used (can be left blank):")
                errors = 0
            except:
                print("Error on Comment")   
        if newCommentsLine != "":
            newCommentsLine = "#" + newCommentsLine
        if newMsgid in message:
            print("That message id already exists")
        else:  
            message[newMsgid] = {"Comments" : newCommentsLine, "msgstr" : newMsgstr}
            return message

    def dictionaryGeneration(self, message):
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
        print ("100: Add a new Language")
        help = 1
        while help != 0: 
            try:
                self.optionLan = int(raw_input("Write the number of your choice: "))
                if (self.optionLan < 0 or self.optionLan > len(listLanguages)) and self.optionLan != 100:
                    raise Exception('Option outside of bounds')
                help = 0
            except:
                print("\n")
                print("Error :: Invalid option, try again\n")

    def showMenu(self, language):
        print ("Choose what would you like to do with the \"" + language + "\" messages:")
        print ("1: Add a message")
        print ("2: Look for a translation or comment with the message id")
        print ("3: See all")
        print ("4: Delete a message (message id, translation and comment)")
        print ("5: Create new empty Language")
        print ("9: Return to Languages Menu")
        print ("0: Exit the CLI")
        
        __help = 1
        while __help != 0: 
            try:
                self.option = int(raw_input("Write the number of your choice: "))
                if (self.option < 0 or self.option > 5) and self.option != 9:
                    raise Exception('Option outside of bounds')
                __help = 0
            except:
                print("\n")
                print("Error :: Invalid option, try again\n")

class PathHandler(object):
        def buildPathMessages(self, language):
            path = os.path.join("languages", language, "LC_MESSAGES", "messages.po")
            return path
        
        def buildPath(self, language):
            path = os.path.join("languages", language, "LC_MESSAGES")
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

    def compile(self, pathToCatalog):
        print("")
        path = os.path.join(pathToCatalog,"messages")
        os.system('pybabel compile -i ' + path + '.po -o ' + path + '.mo')
        print("")

    def extract(self, pathToCatalog):
        print("")
        path = os.path.join(pathToCatalog,"messages")
        os.system('pybabel extract ' + path+ '.po -o '  + 'messages.pot')
        print("")

    def init(self, newLanguage, pathToCatalog):
        print("")
        path = os.path.join(pathToCatalog,"messages")
        os.system('pybabel init -l ' + newLanguage +  ' -i messages.pot -o ' + path + '.po')
        print("")

class Runner(CLImessageClient,Menu,PathHandler,SpecificRecord,FileManager):
    pathLanguages = ""
    language = ""
    __pathCatalog = ""
    __pathMessages = ""
    __listLanguages = []
    option = 0
    optionLan = 0
    __message = ""
    repeated = 0
    __messageDictionary = {}

    def __init__(self):

        self.optionLan = 1
        self.runApp()

    def runApp(self):

        while self.optionLan != 0:
            self.__pathCatalog = ""
            self.__pathMessages = ""
            self.__listLanguages = []
            self.language = "es"
            self.pathLanguages = os.path.join(".","languages")
            self.option = 1
            self.clearScreen()
            self.__listLanguages = self.listLanguages(self.pathLanguages)
            self.showLanguageMenu(self.__listLanguages)
            if self.optionLan == 100:
                self.clearScreen()
                self.language = self.addLanguage()
                self.__pathCatalog = self.buildPathMessages("es")
                self.extract(self.__pathCatalog)
                self.__path = self.buildPath(self.language)
                self.init(self.language, self.__path)
            elif self.optionLan != 0:
                while self.option != 0:
                    self.language = self.__listLanguages[self.optionLan -1]
                    self.__pathCatalog = self.buildPath(self.language)
                    self.__pathMessages = self.buildPathMessages(self.language)
                    self.__messageDictionary = {}
                    self.__message = ""
                    self.showMenu(self.language)
                    
                    if self.option == 1:
                        self.__pathCatalog
                        self.__message = self.readfile(self.language, self.__pathMessages)
                        self.__messageDictionary = self.dictionaryGeneration(self.__message)
                        self.__message = self.addMessage(self.__message, self.language)
                        #to text
                        #check if correct
                        self.compile(self.__pathCatalog)
                    elif self.option == 2:
                        pass
                    elif self.option == 3:
                        self.__pathCatalog
                        self.__message = self.readfile(self.language, self.__pathMessages)
                        self.__messageDictionary = self.dictionaryGeneration(self.__message)
                        print(self.__messageDictionary)

                    elif self.option == 4:
                        pass
                    elif self.option == 5:
                        pass
                    elif self.option == 6:
                        pass
                    elif self.option == 7:
                        pass
                    elif self.option == 8:
                        pass
                    elif self.option == 9:
                        self.option = 0
                    elif self.option == 0:
                        self.optionLan = 0

if __name__ == "__main__":
    Runner()

