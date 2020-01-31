import os, time, argparse, sys, shutil
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

    def askIfConfident(self, message):
        try:
            if self.option == 1:
                print("Are you sure you want to modify the record: \nMessage id: " + message)
            elif self.option == 2:
                print("Are you sure you want to delete the record: \nMessage id: " + message)
            elif self.option == 3:
                print("Are you sure you want to delete the whole " + message + " language")
            confident = int(raw_input("0: No\n1:Yes\n"))
            if confident > 1 or confident < 0:
                raise Exception("Invalid Option")
            if confident == 0:
                return None
        except:
            print("")
            print("Invalid Option")
            print("")
            return None

    def getDictionary(self, language):
        pathToLanguages = self.pathLanguages
        if language == "all":
            pathToPot = os.path.join(pathToLanguages, "messages.pot")
            pathToMessages = pathToPot
        else:
            pathToMessages = self.buildPathMessages(pathToLanguages, language)
        __message = self.readfile(pathToMessages)
        __message = self.cleanMessages(__message)
        __messageDictionary = self.textToDictionary(__message)
        return __messageDictionary

    def compareCatalogs(self, firstLanguage, secondLanguage):
        firstMessages = self.getDictionary(firstLanguage)
        secondMessages = self.getDictionary(secondLanguage)
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
                print("Every Message in the .pot file exists in " + secondLanguage)
                return None
            else:
                print("The catalog for the .pot file is larger than the " + secondLanguage + " catalog")
                for x in helperList:
                    print("Message id: " + x + " is on the .pot file catalog but not in the " + secondLanguage + " catalog")
        else:
            for x in secondMessages:
                firstHelper = helper
                for y in firstMessages:
                    if x == y:
                        helper += 1
                if firstHelper == helper:
                    helperList.append(x.keys())
            print("The catalog for " + secondLanguage + " is larger than the .pot file catalog")
            for x in helperList:
                print("Message id: " + x + " is on " + secondLanguage + " catalog but not in the .pot file")

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
        if any(char.isdigit() for char in specificMessage):
            print("Message id's does not contain numbers")
            return None
        if specificMessage in messageDictionary:
            print("Message Id: " + specificMessage)
            print("Message Translation: " + messageDictionary[specificMessage]["msgstr"])
            print("Message Comments: " + messageDictionary[specificMessage]["Comments"])
            print("")
            messageInfo = {specificMessage : messageDictionary[specificMessage]}
            return messageInfo
        else:
            print("That Message Id doesn't exist in the " + language + " Catalog")
            return None
                
    def modifyMessage(self, messageDictionary, especificMessage, comment, translation):
        messageDictionary = messageDictionary
        message = especificMessage
        messageId = message.keys()[0]
        messageStr = message[message.keys()[0]]["msgstr"]
        messageComments = message[message.keys()[0]]["Comments"]
        newMessageStr = translation
        newMessageComments = comment
        if self.option == 1:
            if newMessageStr == "":
                newMessageStr = messageStr
            else:
                try:
                    newMessageStr = newMessageStr
                    if any(char.isdigit() for char in newMessageStr):
                        raise Exception("Message Translations should have only letters")
                except:
                    print("")
                    print("Error: Message Translations should have only letters")
                    print("")
                    return None
            if newMessageComments == "":
                newMessageComments = messageComments
            else:
                try:
                    newMessageComments = newMessageComments
                except:
                    print("")
                    print("Error: Unknown Comment changes errors")
                    print("")
                    return None
            messageDictionary[messageId] = {"Comments" : newMessageComments, "msgstr" : newMessageStr}
        elif self.option == 2:
            del messageDictionary[messageId]
            print("\nThe element has been succesfully deleted")
        return messageDictionary

class PathHandler(object):
        def buildPathMessages(self, pathToLanguages, language):
            path = os.path.join("languages", language, "LC_MESSAGES", "messages.po")
            return path
        
        def buildPath(self, language):
            path = os.path.join("languages", language, "LC_MESSAGES")
            return path
        
        def listLanguages(self,pathLanguages):
            options = os.listdir(os.path.join(".", pathLanguages)) 
            return options
            
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
        args.append(pathToPot)
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

class Runner(PathHandler,SpecificRecord,FileManager):
    pathLanguages = ""
    language = ""
    __pathCatalog = ""
    __pathMessages = ""
    optionLan = 0
    __message = ""
    __messageDictionary = {}
    __repeatedDic = {}
    __repeated = 0
    option = 0

    def __init__(self):
        self.pathLanguages = os.path.join(".","languages")
        self.CLI(sys.argv)
    
    def CLI(self, args):
        options = ["aL","aM", "s", "mM", "v", "dM", "dL", "h"]
        optionsLong = ["addLanguage","addMessage", "search", "modifyMessage", "verify", "deleteMessage", "deleteCatalog", "help"]
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

                parser_v = subparsers.add_parser("v",help = "verify:          Allows to verify that every Language Catalog has the same Message Id's")
                parser_v.set_defaults(func=self.verifyCatalogs)

                parser_s = subparsers.add_parser("s",help = "search:           Allows to search a message through a Message Id, result is either if exists and if a language is selected also shows its Comments and Translation")
                parser_s.add_argument("messageId", metavar="Message_Id")
                parser_s.add_argument("exLan", choices=languages, nargs='?',  default = "all",  metavar="Language", help="Language to search in, for all languages: all")
                parser_s.set_defaults(func=self.searchMessageInCatalogs)

                parser_aL = subparsers.add_parser("aL",help = "addLanguage:      Allows to add a new language with the Message Id's already added")
                parser_aL.add_argument("newLan", metavar="New_Language", help="Language to be added")
                parser_aL.set_defaults(func=self.addLanguageCatalog)

                parser_aM = subparsers.add_parser("aM",help = "addMessage:       Allows to add a message, either to one language or all")
                parser_aM.add_argument("messageId", metavar="New_Message_Id", help="The Message Id should go wrapped in quotation marks")
                parser_aM.add_argument("-C","--Comment", metavar="Message_Comment", help="The Message Comment should go wrapped in quotation marks")
                parser_aM.set_defaults(func=self.addMessageToCatalogs)

                parser_mM = subparsers.add_parser("mM",help = "modifyMessage:    Allows to modify a Message Id, and if a language is selected then allow to modify Comment and/or Translation")
                parser_mM.add_argument("messageId", metavar="Message_Id")
                parser_mM.add_argument("-C","--Comment", metavar="Message_Comment", help="The Message Comment should go wrapped in quotation marks")
                parser_mM.add_argument("exLan", choices=languages, nargs='?',   default = "all", metavar="Language", help= "Language to search in, for changes on Translation use ")
                print(len(args))
                if(("all" not in argsL) or "-h" in argsL or "--help" in argsL):
                    parser_mM.add_argument("-T","--Translation", metavar="Message_Translation", help="The Message Translation should go wrapped in quotation marks")
                parser_mM.set_defaults(func=self.modifyMessageInCatalog)

                parser_dM = subparsers.add_parser("dM",help = "deleteMessage:    Allow to delete a Message Id in all catalogs or if language provided only in said language")
                parser_dM.add_argument("messageId", metavar="Message_Id", help = "Message Id to be deleted")
                parser_dM.set_defaults(func=self.deleteMessageInCatalogs)

                parser_dL = subparsers.add_parser("dL",help = "deleteCatalog:    Allows to delete a whole Language's Message Catalog")
                parser_dL.add_argument("exLan", choices=languages, metavar="Language", help= "Language to delete its Catalog")
                parser_dL.set_defaults(func=self.deleteLanguageCatalog)

                arguments = parser.parse_args(argsL)
                arguments.func(arguments)
                print(arguments)

    def verifyCatalogs(self, args):
        pathLanguages = self.pathLanguages
        allLanguages = self.listLanguages(pathLanguages)
        for x in allLanguages:
            print("#########  " + x + "Catalog  #########")
            self.compareCatalogs("all", x)
            print("")
            print("")

    def searchMessageInCatalogs(self, args):
        message = args.messageId
        language = args.language
        pathLanguages = self.pathLanguages
        __message = message
        __messageDictionary = {}
        allLanguages = [language]
        if language == "all":
            allLanguages = self.listLanguages(pathLanguages)
        for x in range(len(allLanguages)):
            language = allLanguages[x]
            __messageDictionary = self.getDictionary(language)
            self.searchMessage(message ,__messageDictionary, language)
            print("")
        __message = message
        __messageDictionary = {} 
    
    def addLanguageCatalog(self, args):
        language = args.newLan
        pathLanguages = self.pathLanguages
        pathToPot = os.path.join(pathLanguages, "messages.pot")
        pathToCatalog = self.buildPath(language)
        self.init(language,pathToCatalog,pathToPot)
        self.compile(pathToCatalog)

    def addMessageToCatalogs(self, args):
        newMessage = args.messageId
        newComment = args.Comment
        pathLanguages = self.pathLanguages
        pathToPot = os.path.join(pathLanguages, "messages.pot")
        allLanguages = self.listLanguages(pathLanguages)
        __message = ""
        __messageDictionary = {}
        __messageDictionary = self.getDictionary("all")
        __messageDictionary = self.addMessage(newMessage, __messageDictionary, newComment)
        if __messageDictionary != None:
            __message = self.dictionaryToText(__messageDictionary)
            self.writefile(__message, pathToPot)
            for x in range(len(allLanguages)):
                __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                self.update(__pathToCatalog, pathToPot)
                self.compile(__pathToCatalog)  
        __message = ""
        __messageDictionary = {} 
        
    def modifyMessageInCatalog(self, args):
        language = args.exLan
        message = args.messageId
        translation = args.Translation
        comment = args.Comment
        self.option = 1
        pathLanguages = self.pathLanguages
        pathToPot = os.path.join(pathLanguages, "messages.pot")
        allLanguages = self.listLanguages(pathLanguages)
        __messageDictionary = self.getDictionary(language)
        toBeModified = self.searchMessage(message, __messageDictionary, language)
        ask = None 
        if toBeModified != None:
            ask = self.askIfConfident(message)
        if ask != None:
            __messageDictionary = self.modifyMessage(__messageDictionary, toBeModified, comment, translation)
            __message = self.dictionaryToText(__messageDictionary)
            if language != "all":
                __pathToCatalog = os.path.join(pathLanguages, allLanguages[0], "LC_MESSAGES")
                __pathMessages = os.path.join(__pathToCatalog, "messages.po")
                self.writefile(__message, __pathMessages)
                self.compile(__pathToCatalog)
            else:
                self.writefile(__message, pathToPot)
                for x in range(len(allLanguages)):
                    __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                    self.update(__pathToCatalog, pathToPot)
                    self.compile(__pathToCatalog)
                
    def deleteMessageInCatalogs(self, args):
        language = "all"
        message = args.messageId
        self.option = 2
        pathLanguages = self.pathLanguages
        pathToPot = os.path.join(pathLanguages, "messages.pot")
        allLanguages = self.listLanguages(pathLanguages)
        __messageDictionary = self.getDictionary(language)
        toBeDeleted = self.searchMessage(message, __messageDictionary, language)
        ask = None 
        if toBeDeleted != None:
            ask = self.askIfConfident(message)
        if ask != None:
            if toBeDeleted != None:
                __messageDictionary = self.modifyMessage(__messageDictionary, toBeDeleted, "", "")
                __message = self.dictionaryToText(__messageDictionary)
                self.writefile(__message, pathToPot)
                for x in range(len(allLanguages)):
                    __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                    self.update(__pathToCatalog, pathToPot)
                    self.compile(__pathToCatalog)
            
    def deleteLanguageCatalog(self, args):
        language = args.exLan
        self.option = 3
        pathLanguages = self.pathLanguages
        ask = self.askIfConfident(language)
        if ask != None:
            pathLanguage = os.path.join(pathLanguages, language)
            shutil.rmtree(pathLanguage)
            print("The deletion of the " + language + " language was succesful")
            print("")

    def addTranslations(self):
        pass
    
            #parser.add_argument("-l", "--language", dest = "exLan")
        #https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
        #https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
        #https://docs.python.org/3/library/argparse.html
        #https://stackoverflow.com/questions/304883/what-do-i-use-on-linux-to-make-a-python-program-executable

if __name__ == "__main__":
    Runner()

