import os, time
from babel.messages.catalog import Message
from babel.messages.frontend import CommandLineInterface, compile_catalog, init_catalog, extract_messages

class CLImessageClient(object):
    def __init__(self):
        print("")

    def clearScreen(self):
        if os.name == 'nt':
            _ = os.system('cls') 
        else: 
            _ = os.system('clear') 

    def cleanMessages(self, message):
        cleanMessage = message
        messagesDictionary = self.textToDictionary(message)
        cleanMessage = self.dictionaryToText(messagesDictionary)
        return cleanMessage

    def addLanguage(self, listLanguages):
        language = ""
        listLanguages = listLanguages
        errors = 1
        while errors != 0:
            try:
                if errors == 1:
                    print("Which language do you wish to add? ")
                language = raw_input()
                if any(char.isdigit() for char in language):
                    raise Exception("Languages should have only letters")
                if language in listLanguages:
                    print("Language already exists, do you wish to add another language?\n0: No \n1:Yes, add another language")
                    errorsOpt = 0
                    while errorsOpt == 0:
                        try:
                            errors = int(raw_input("\nWhat do you choose?"))
                            if errors > 1 or errors <0:
                                raise Exception("Error: Invalid Option")
                            errorsOpt = 1
                        except Exception as e:
                            print(e)
                            print("Try again")
                            print("")
                    if errors == 1:
                        raise Exception("")
                errors = 0
            except Exception as e:
                print(e)
                print("")
                print("Try again")
                print("")
        return language

    def dictionaryToText(self, messagesDictionary):
        messagesDictionary = messagesDictionary
        idsList = sorted(messagesDictionary)
        repeatedIdsList = []
        fuzzyIdsList = []
        newString = ""
        repeatedString = ""
        fuzzyString = ""
        fuzzyQuantity = 0
        repeatedQuantity = 0
        for x in range(len(idsList)):
            if idsList[x] == "//Repeated":
                repeatedIdsList = sorted(messagesDictionary[idsList[x]])
                for y in range(len(repeatedIdsList)):
                    repeatedQuantity += 1
                    if messagesDictionary[idsList[x]][repeatedIdsList[y]]["Comments"] != "":
                        repeatedString += messagesDictionary[idsList[x]][repeatedIdsList[y]]["Comments"] + "\n"
                    repeatedString += "msgid \""
                    repeatedString += repeatedIdsList[y] + "\"\n"
                    repeatedString += "msgstr \""
                    repeatedString += messagesDictionary[idsList[x]][repeatedIdsList[y]]["msgstr"] + "\"\n\n"
            elif idsList[x] == "//Fuzzy":
                fuzzyIdsList = sorted(messagesDictionary[idsList[x]])
                for y in range(len(fuzzyIdsList)):
                    fuzzyQuantity += 1
                    if messagesDictionary[idsList[x]][fuzzyIdsList[y]]["Comments"] != "":
                        fuzzyString += messagesDictionary[idsList[x]][fuzzyIdsList[y]]["Comments"] + "\n"
                    fuzzyString += "#~ msgid \""
                    fuzzyString += fuzzyIdsList[y] + "\"\n"
                    fuzzyString += "#~ msgstr \""
                    fuzzyString += messagesDictionary[idsList[x]][fuzzyIdsList[y]]["msgstr"] + "\"\n\n"
            else:
                if messagesDictionary[idsList[x]]["Comments"] != "":
                    newString += messagesDictionary[idsList[x]]["Comments"] + "\n"
                newString += "msgid \""
                newString += idsList[x] + "\"\n"
                newString += "msgstr \""
                newString += messagesDictionary[idsList[x]]["msgstr"] + "\"\n\n"
        if self.option == 3 and repeatedQuantity > 0:
            newString += "\n############################################ Repeated Message Id's ############################################\n"
        newString += repeatedString
        if self.option == 3 and fuzzyQuantity > 0:
            newString += "\n############################################ Fuzzy Message Id's ############################################\n"
        newString += fuzzyString
        if self.option == 3 and repeatedQuantity > 0:
            newString += "############# Repeated Quantity: " + str(repeatedQuantity) + " #############\n"
        if self.option == 3 and fuzzyQuantity > 0:
            newString += "############# Fuzzy Quantity:    " + str(fuzzyQuantity) + " #############\n"
        return newString

    def textToDictionary(self, message):
        messageList = message.split("\n\n")
        messageDic = {}
        repeatedDic = {}
        fuzzyDic = {}
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
                if wholeLine == "":
                    pass
                else:
                    print("Unexpected error on " + wholeLine)
            if "#~" in msgidLine:
                index = message.index(msgidLine[3:])
                secondIndex = message.index(msgidLine)
                firstInstance = len(message[:index].split("\n"))
                secondInstance = len(message[:secondIndex].split("\n"))
                fuzzyDic[msgid] = {"Comments" : commentsLine, "msgstr" : msgstr, 
                    "Instance 1" : firstInstance,
                    "Instance 2" : secondInstance}
            elif msgid in messageDic:
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
        self.__fuzzy = len(fuzzyDic)
        messageDic["//Repeated"] = repeatedDic
        messageDic["//Fuzzy"] = fuzzyDic
        return messageDic

    def addMessage(self, messageDictionary, language):
        repeated = 0
        while repeated == 0:
            errors = 1
            while errors == 1:
                try:
                    newMsgid = raw_input("Write a message (a message in English that can be translated): ")
                    if any(char.isdigit() for char in newMsgid):
                        raise Exception("No numbers")
                    errors = 0
                except:
                    print("")
                    print("Message id's should not contain numbers")
                    print("Try again")
                    print("")
            errors = 1
            while errors == 1:
                try:
                    newMsgstr = raw_input("Write the translation of the message on " + language + ": ")
                    if any(char.isdigit() for char in newMsgstr):
                        raise Exception("No numbers")
                    errors = 0
                except:
                    print("Message translation should not contain numbers")
                    print("Try again")
            errors = 1
            while errors == 1:
                try:
                    newCommentsLine = raw_input("Write a comment on where it's gonna be used (can be left blank):")
                    errors = 0
                except:
                    print("Error on Comment")   
            if newCommentsLine != "":
                newCommentsLine = "#" + newCommentsLine
            if newMsgid in messageDictionary:
                print("That message id already exists")
                print("Want to try to add another Message?")
                errors = 1
                while errors == 1:
                    try:
                        inputRepeated = int(raw_input("Write 0 to try to add another message or 1 to return to the main menu"))
                        if inputRepeated < 0 or inputRepeated > 1:
                            raise Exception("Value under 0 or under 1")
                        repeated = inputRepeated
                        errors = 0
                    except: 
                        print("")
                        print("Error: Invalid option")
                        print("Try again")
                        print("")
            else:  
                messageDictionary[newMsgid] = {"Comments" : newCommentsLine, "msgstr" : newMsgstr}
                repeated = 1
        return messageDictionary

    def searchMessage(self, messageDictionary):
        specificMessage = ""
        error = 1
        msgError = 1
        while msgError == 1:
            error = 1
            while error == 1:
                try: 
                    if self.option == 2:
                        specificMessage = raw_input("Please write the message Id that you want to search for: ")
                    if self.option == 4:
                        specificMessage = raw_input("Please write the message Id that you want to delete: ")
                    if any(char.isdigit() for char in specificMessage):
                        raise Exception("Message id's does not contain numbers")
                    error = 0
                except Exception as e: 
                    print("")
                    print(e)
                    print("Try again")
                    print("")
            if specificMessage in messageDictionary:
                print("Message Id: " + specificMessage)
                print("Message Translation: " + messageDictionary[specificMessage]["msgstr"])
                print("Message Comments: " + messageDictionary[specificMessage]["Comments"])
                msgError = 0
                messageInfo = {specificMessage : messageDictionary[specificMessage]}
                return messageInfo
            else:
                print("That Message Id doesn't exist")
                error = 1
                while error == 1:
                    try:
                        msgError = int(raw_input("Do you wish to search another Message Id?\n0: No \n1: Yes\n"))
                        print("")
                        if msgError < 0 or msgError > 1:
                                raise Exception("Invalid Option")
                        error = 0
                    except Exception as e:
                        print("")
                        print("Error: Invalid option")
                        print("Try again")
                        print("")
                if msgError == 0:
                    return None
                
    def removeMessage(self, messageDictionary, especificMessage):
        messageDictionary = messageDictionary
        message = especificMessage
        messageId = message.keys()[0]
        messageStr = message[message.keys()[0]]["msgstr"]
        messageComments = message[message.keys()[0]]["Comments"]
        secure = 0
        while secure == 0:
            try:
                print("Are you sure you want to delete the record: \nMessage id: " + messageId)
                print("Translation: " + messageStr)
                print("Comments: " + messageComments)
                secure = input("\n")
                secure = int(raw_input("0: No\n1:Yes\n"))
                if secure > 1 or secure < 0:
                    raise Exception("Invalid Option")
                if secure == 0:
                    return messageDictionary
            except:
                print("")
                print("Error: Invalid option")
                print("Try again")
                print("")
        del messageDictionary[messageId]
        print("\nThe element has been succesfully deleted")
        return messageDictionary
        
class Menu(object):
    def __init__(self):
        self.language = "en"

    def listLanguages(self,pathLanguages):
        options = os.listdir(os.path.join(".", pathLanguages)) 
        return options

    def showLanguageMenu(self, listLanguages):
        print ("Which Language do you wish to change?:")
        for x in range(len(listLanguages)):
            languageMenu = str(x + 1) + ": " + listLanguages[x]
            print(languageMenu)
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
                print("")
                print("Error: Invalid option")
                print("Try again")
                print("")

    def showMenu(self, language):
        print ("Choose what would you like to do with the \"" + language + "\" Messages:")
        print ("1: Add a Message")
        print ("2: Look if a Message Id exists and see the Comments and Translation")
        print ("3: See all")
        print ("4: Delete a message (Message Id, Translation and Comments)")
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
                print("")
                print("Error: Invalid option")
                print("Try again")
                print("")

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

    def writefile(self, message, path):
        file = open(path)
        file.write(message)

    def compile(self, pathToCatalog):
        print("")
        path = os.path.join(pathToCatalog,"messages")
        args = []
        args.append("pybabel")
        args.append("compile")
        args.append("-i")
        args.append(path + ".po")
        args.append("-o")
        args.append(path + ".mo")
        self.CLI.run(args)
        print("")

    def extract(self, pathToCatalog):
        print("")
        path = os.path.join(pathToCatalog,"messages")
        args = []
        args.append("pybabel")
        args.append("extract")
        args.append(path + ".po")
        args.append("-o")
        args.append("messages.pot")
        self.CLI.run(args)
        print("")
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
    __messageDictionary = {}
    __repeatedDic = {}
    __repeated = 0
    CLI = CommandLineInterface()

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
                self.language = self.addLanguage(self.__listLanguages)
                self.__pathCatalog = self.buildPath("es")
                #self.extract(self.__pathCatalog)
                #self.__path = self.buildPath(self.language)
                #self.init(self.language, self.__path)
            elif self.optionLan != 0:
                while self.option != 0:
                    print("")
                    print("")
                    self.language = self.__listLanguages[self.optionLan -1]
                    self.__pathCatalog = self.buildPath(self.language)
                    self.__pathMessages = self.buildPathMessages(self.language)
                    self.__repeated = 0
                    self.__repeatedDic = {}
                    self.__messageDictionary = {}
                    self.__message = ""
                    self.showMenu(self.language)
                    self.__message = self.readfile(self.language, self.__pathMessages)
                    self.__message = self.cleanMessages(self.__message)
                    print("")
                    if self.option == 1:
                        self.__messageDictionary = self.textToDictionary(self.__message)
                        self.__messageDictionary = self.addMessage(self.__messageDictionary, self.language)
                        self.__message = self.dictionaryToText(self.__messageDictionary)
                        #check if correct
                        #compile
                        self.compile(self.__pathCatalog)
                        #self.writefile(self.__message, self.__pathMessages)
                    elif self.option == 2:
                        self.__messageDictionary = self.textToDictionary(self.__message)
                        self.searchMessage(self.__messageDictionary)
                    elif self.option == 3:
                        print(self.__message)
                    elif self.option == 4:
                        self.__messageDictionary = self.textToDictionary(self.__message)
                        toBeDeleted = self.searchMessage(self.__messageDictionary)
                        self.__messageDictionary = self.removeMessage(self.__messageDictionary, toBeDeleted)
                        self.__message = self.dictionaryToText(self.__messageDictionary)
                        #self.writefile(self.__message, self.__pathMessages)
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

