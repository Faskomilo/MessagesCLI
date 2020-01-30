import os, time, argparse, sys
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

    def compareCatalogs(self, firstLanguage, secondLanguage):
        firstMessages = self.readfile(firstLanguage, self.__pathMessages)
        firstMessages = self.cleanMessages(firstMessages)
        firstMessages = self.textToDictionary(firstMessages)
        secondMessages = self.readfile(secondLanguage, self.__pathMessages)
        secondMessages = self.cleanMessages(secondMessages)
        secondMessages = self.textToDictionary(secondMessages)
        helper = 0
        helperList = []
        if len(firstMessages) >= len(secondMessages):
            for x in firstMessages:
                firstHelper = helper
                for y in secondMessages:
                    if x == y:
                        helper += 1
                if firstHelper == helper:
                    helperList.append(x.keys())
            if helper == len(firstMessages):
                print("Every Message in " + firstLanguage + " exists in " + secondLanguage)
                return None
            else:
                print("The catalog for " + firstLanguage + " is larger than the " + secondLanguage + " catalog")
                for x in helperList:
                    print("Message id: " + x + " is on " + firstLanguage + " catalog but not in the " + secondLanguage + " catalog")
        else:
            for x in secondMessages:
                firstHelper = helper
                for y in firstMessages:
                    if x == y:
                        helper += 1
                if firstHelper == helper:
                    helperList.append(x.keys())
            
            print("The catalog for " + secondLanguage + " is larger than the " + firstLanguage + " catalog")
            for x in helperList:
                print("Message id: " + x + " is on " + secondLanguage + " catalog but not in the " + firstLanguage + " catalog")

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
        if self.option == 1 and repeatedQuantity > 0:
            newString += "\n############################################ Repeated Message Id's ############################################\n"
        newString += repeatedString
        if self.option == 1 and fuzzyQuantity > 0:
            newString += "\n############################################ Obsolete Message Id's ############################################\n"
        newString += fuzzyString
        if self.option == 1 and repeatedQuantity > 0:
            newString += "############# Repeated Quantity: " + str(repeatedQuantity) + " #############\n"
        if self.option == 1 and fuzzyQuantity > 0:
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

    def addMessage(self, newMessage, newComment,messageDictionary):
        messageDictionary = messageDictionary
        newMsgid = newMessage
        Comment = newComment
        if newMsgid in messageDictionary:
            print("That Message Id already exists")
            print("")
            return None
        else:  
            messageDictionary[newMsgid] = {"Comments" : Comment, "msgstr" : ""}
        return messageDictionary

    def searchMessage(self, message, messageDictionary, language):
        specificMessage = message
        msgError = 1
        while msgError == 1:
            if any(char.isdigit() for char in specificMessage):
                raise Exception("Message id's does not contain numbers")
            if specificMessage in messageDictionary:
                print("Message Id: " + specificMessage)
                print("Message Translation: " + messageDictionary[specificMessage]["msgstr"])
                print("Message Comments: " + messageDictionary[specificMessage]["Comments"])
                print("")
                msgError = 0
                messageInfo = {specificMessage : messageDictionary[specificMessage]}
                return messageInfo
            else:
                print("That Message Id doesn't exist in the " + language + " Catalog")
                return None
                
    def modifyMessage(self, messageDictionary, especificMessage):
        messageDictionary = messageDictionary
        message = especificMessage
        messageId = message.keys()[0]
        messageStr = message[message.keys()[0]]["msgstr"]
        messageComments = message[message.keys()[0]]["Comments"]
        newMessageId = ""
        newMessageStr = ""
        newMessageComments = ""
        confident = 0
        while confident == 0:
            try:
                if self.option == 4:
                    print("Are you sure you want to modify the record: \nMessage id: " + messageId)
                elif self.option == 6:
                    print("Are you sure you want to delete the record: \nMessage id: " + messageId)
                print("Translation: " + messageStr)
                print("Comments: " + messageComments)
                confident = int(raw_input("0: No\n1:Yes\n"))
                if confident > 1 or confident < 0:
                    raise Exception("Invalid Option")
                if confident == 0:
                    return messageDictionary
            except:
                print("")
                print("Error: Invalid option")
                print("Try again")
                print("")
        if self.option == 4:
            error = 1
            while error == 1:
                try:
                    error = int(raw_input("Do you wish to change the Message Id: \n" + messageId + "\n?\n0: No\n1: Yes\n"))
                    if error < 0 or error > 1:
                        raise Exception("Value under 0 or under 1")
                    print("")
                    if error == 1:
                        while error == 1:
                            try:
                                newMessageId = raw_input("Write the new Message Id: ")
                                if any(char.isdigit() for char in newMessageId):
                                    raise Exception("Message Id's should have only letters")
                                error = 0
                            except:
                                print("")
                                print("Error: Message Id's should have only letters")
                                print("Try again")
                                print("")
                    else:
                        newMessageId = messageId
                except: 
                    print("")
                    print("Error: Invalid option")
                    print("Try again")
                    print("")
            error = 1
            while error == 1:
                try:
                    error = int(raw_input("Do you wish to change the Message Translation: \n" + messageStr + "\n?\n0: No\n1: Yes\n"))
                    if error < 0 or error > 1:
                        raise Exception("Value under 0 or under 1")
                    print("")
                    if error == 1:
                        while error == 1:
                            try:
                                newMessageStr = raw_input("Write the new Message Translation: ")
                                if any(char.isdigit() for char in newMessageStr):
                                    raise Exception("Message Translations should have only letters")
                                error = 0
                            except:
                                print("")
                                print("Error: Message Translations should have only letters")
                                print("Try again")
                                print("")
                    else:
                        newMessageStr = messageStr
                except: 
                    print("")
                    print("Error: Invalid option")
                    print("Try again")
                    print("")
            error = 1
            while error == 1:
                try:
                    error = int(raw_input("Do you wish to change the Message Comments: \n" + messageComments + "\n?\n0: No\n1: Yes\n"))
                    if error < 0 or error > 1:
                        raise Exception("Value under 0 or under 1")
                    print("")
                    if error == 1:
                        while error == 1:
                            try:
                                newMessageComments = raw_input("Write the new Message Comments: ")
                            except:
                                print("")
                                print("Error: Unknown Comment changes errors")
                                print("Try again")
                                print("")
                    else:
                        newMessageComments = messageComments
                except: 
                    print("")
                    print("Error: Invalid option")
                    print("Try again")
                    print("")
            messageDictionary[newMessageId] = {"Comments" : newMessageComments, "msgstr" : newMessageStr}
            del messageDictionary[messageId]
        elif self.option == 6:
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
        print ("1: See all")
        print ("2: Add a Message")
        print ("3: Look if a Message Id exists and see the Comments and Translation")
        print ("4: Modify a Message (Message Id, Translation or Comments)")
        print ("5: Compare the Message Catalog to another Message Catalog")
        print ("6: Delete a message (Message Id, Translation and Comments)")
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
            path = os.path.join("languages", language, "LC_MESSAGES", "messages.pot")
            return path
        
        def buildPath(self, language):
            path = os.path.join("languages", language, "LC_MESSAGES")
            return path
            
class SpecificRecord(object):
    pass

class FileManager(CLImessageClient):
    CLI = CommandLineInterface()

    def readfile(self, path):
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

    def init(self, newLanguage, pathToCatalog, pathToPot):
        print("")
        path = os.path.join(pathToCatalog,"messages.po")
        args = []
        args.append("pybabel")
        args.append("init")
        args.append("-l")
        args.append(newLanguage)
        args.append("-i")
        args.append(pathtoPot)
        args.append("-o")
        args.append(path)
        self.CLI.run(args)
        print("")
    
    def update(self, pathToCatalog, pathToPot):
        print("")
        path = os.path.join(pathToCatalog,"messages.po")
        args = []
        args.append("pybabel")
        args.append("update")
        args.append("-i")
        args.append(path)
        args.append("-o")
        args.append(pathToPot)
        self.CLI.run(args)
        print("")

class Runner(Menu,PathHandler,SpecificRecord,FileManager):
    pathLanguages = ""
    language = ""
    __pathCatalog = ""
    __pathMessages = ""
    optionLan = 0
    __message = ""
    __messageDictionary = {}
    __repeatedDic = {}
    __repeated = 0

    def __init__(self):
        self.pathLanguages = os.path.join(".","languages")
        self.CLI(sys.argv)
    
    def CLI(self, args):
        options = ["aL","aM", "s", "mM", "c", "dM", "dL", "h"]
        optionsLong = ["addLanguage","addMessage", "search", "modifyMessage", "check", "deleteMessage", "deleteCatalog", "help"]
        languages = self.listLanguages(self.pathLanguages)
        languages.append("all")

        option = []
        argsL = args

        self.__pathCatalog = ""
        self.__pathMessages = ""
        if len(argsL) < 2:
            print("No argument recieved, exiting. See --help if needed.")
        else:
            for x in options:
                if argsL[1] == x:
                    option.append(x)
            if len(option) == 0:
                for x in range(len(optionsLong)):
                    if argsL[1] == optionsLong[x]:
                        optionShort = options[x]
                        option.append(optionShort)
                        argsL[0] = optionShort
            if len(option) == 0:
                print("No valid first argument given, see --help if needed.")
            elif len(option) > 1:
                print("Too many actions, just one per run allowed, see --help if needed.")
            else:
                parser = argparse.ArgumentParser(prog="MsgManager", description="Options for management of .po catalogs")
                parser.add_argument("CLImessageClient.py")
                subparsers = parser.add_subparsers(title="Accepted commands", description="Available Options")

                parser_c = subparsers.add_parser("c",help = "check:          Allows to verify that every Language Catalog has the same Message Id's")
                #parser_c.set_defaults(func=self.addMessage)

                parser_s = subparsers.add_parser("s",help = "search:           Allows to search a message through a Message Id, result is either if exists and if a language is selected also shows its Comments and Translation")
                parser_s.add_argument("messageId", metavar="Message_Id")
                parser_s.add_argument("exLan", choices=languages, nargs='?',  default = "all",  metavar="Language", help="Language to search in, for all languages: all")
                #parser_s.set_defaults(func=self.searchMessage)

                parser_aL = subparsers.add_parser("aL",help = "addLanguage:      Allows to add a new language with the Message Id's already added")
                parser_aL.add_argument("newLan", metavar="New_Language", help="Language to be added")
                #parser_aL.set_defaults(func=self.addLanguage)

                parser_aM = subparsers.add_parser("aM",help = "addMessage:       Allows to add a message, either to one language or all")
                parser_aM.add_argument("messageId", metavar="New_Message_Id", help="The Message Id should go wrapped in quotation marks")
                #parser_aM.set_defaults(func=self.addMessage)

                parser_mM = subparsers.add_parser("mM",help = "modifyMessage:    Allows to modify a Message Id, and if a language is selected then allow to modify Comment and/or Translation")
                parser_mM.add_argument("messageId", metavar="Message_Id")
                parser_mM.add_argument("-C","--Comment", metavar="Message_Comment", help="The Message Comment should go wrapped in quotation marks")
                parser_mM.add_argument("exLan", choices=languages, nargs='?',   default = "all", metavar="Language", help= "Language to search in, for changes on Translation use ")
                if((len(args) > 3 and argsL[1] == "mM" and argsL[3] != "all") or "-h" in argsL or "--help" in argsL):
                    parser_mM.add_argument("-T","--Translation", metavar="Message_Translation", help="The Message Translation should go wrapped in quotation marks")
                
                #parser_mM.set_defaults(func=self.modify)

                parser_dM = subparsers.add_parser("dM",help = "deleteMessage:    Allow to delete a Message Id in all catalogs or if language provided only in said language")
                parser_dM.add_argument("messageId", metavar="Message_Id", help = "Message Id to be deleted")
                #parser_dM.set_defaults(func=self.modify)

                parser_dL = subparsers.add_parser("dL",help = "deleteCatalog:    Allows to delete a whole Language's Message Catalog")
                parser_dL.add_argument("exLan", choices=languages, metavar="Language", help= "Language to delete its Catalog")
                #parser_dL.set_defaults(func=self.modify)

                arguments = parser.parse_args(argsL)
                #arguments.__new__(hola = "as")
                print(arguments)

    def checkCatalogs(self):
        pass

    def searchMessageInCatalogs(self, message, language):
        pathLanguages = self.pathLanguages
        __message = message
        __messageDictionary = {}
        allLanguages = [language]
        if language == "all":
            allLanguages = self.listLanguages(pathLanguages)
        for x in range(len(allLanguages)):
            language = allLanguages[x]
            pathMessages = os.path.join(pathLanguages, language, "LC_MESSAGES", "messages.po")
            __message = self.readfile(pathMessages)
            __message = self.cleanMessages(__message)
            __messageDictionary = self.textToDictionary(__message)
            self.searchMessage(message ,__messageDictionary, language)
            print("")
        __message = message
        __messageDictionary = {} 
    
    def addLanguageCatalog(self, language):
        self.pathLanguages
        self.language = self.addLanguage(self.__listLanguages)
        self.__pathCatalog = self.buildPath("es")
        #self.extract(self.__pathCatalog)
        self.__path = self.buildPath(self.language)
        self.init(self.language, self.__path)
    
    def addMessageToCatalogs(self, newMessage, newComment):
        pathLanguages = self.pathLanguages
        pathToPot = os.path.join(pathLanguages, "messages.pot")
        allLanguages = self.listLanguages(pathLanguages)
        __message = ""
        __messageDictionary = {}
        __message = self.readfile(pathToPot)
        __message = self.cleanMessages(__message)
        __messageDictionary = self.textToDictionary(__message)
        __messageDictionary = self.addMessage(newMessage, __messageDictionary, newComment)
        if __messageDictionary != None:
            __message = self.dictionaryToText(__messageDictionary)
            self.writefile(__message, pathToPot)
            for x in range(len(allLanguages)):
                pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                self.update(pathToCatalog, pathToPot)
                self.compile(self.__pathCatalog)  
        __message = ""
        __messageDictionary = {} 
        
    
    def modifyMessageInCatalog(self):
        pass
    
    def deleteMessageInCAtalogs(self):
        pass

    def deleteLanguageCatalog(self):
        pass

    def addTranslations(self):
        pass
    
            #parser.add_argument("-l", "--language", dest = "exLan")
        #https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
        #https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
        #https://docs.python.org/3/library/argparse.html
        #https://stackoverflow.com/questions/304883/what-do-i-use-on-linux-to-make-a-python-program-executable

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
            if self.optionLan == 100:                          #Add new language
                self.clearScreen()
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
                    self.__message = self.readfile(self.__pathMessages)
                    self.__message = self.cleanMessages(self.__message)
                    print("")
                    if self.option == 1:                       #See all messages
                        print(self.__message)
                    elif self.option == 2:                     #Add new message
                        self.__messageDictionary = self.textToDictionary(self.__message)
                        self.__messageDictionary = self.addMessage(self.__messageDictionary, self.language)
                        self.__message = self.dictionaryToText(self.__messageDictionary)
                        print(self.__message)
                        #check if correct
                        self.writefile(self.__message, self.__pathMessages)
                        self.compile(self.__pathCatalog)
                    elif self.option == 4:                      #Modify a message
                        self.__messageDictionary = self.textToDictionary(self.__message)
                        toBeModified = self.searchMessage(self.__messageDictionary)
                        if toBeModified != None:
                            self.__messageDictionary = self.modifyMessage(self.__messageDictionary, toBeModified)
                            self.__message = self.dictionaryToText(self.__messageDictionary)
                            self.writefile(self.__message, self.__pathMessages)
                            self.compile(self.__pathCatalog)
                    elif self.option == 5:                      #Compare the message Catalog
                        self.compareCatalogs(self.language, "en")
                    elif self.option == 6:                      #Delete a Message
                        self.__messageDictionary = self.textToDictionary(self.__message)
                        toBeDeleted = self.searchMessage(self.__messageDictionary)
                        if toBeDeleted != None:
                            self.__messageDictionary = self.modifyMessage(self.__messageDictionary, toBeDeleted)
                            self.__message = self.dictionaryToText(self.__messageDictionary)
                            self.writefile(self.__message, self.__pathMessages)
                            self.compile(self.__pathCatalog)
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

