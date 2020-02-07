import os, time, argparse, sys, shutil, csv, ConfigParser
try:
    from babel.messages.frontend import CommandLineInterface
except:
    print("")
    print("Install Babel 2.8.0 before trying to run this program")
    print("")
    sys.exit(0)

try:
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
except Exception as e:
    print(e)
    print("config.ini file needed to run")
    sys.exit(0)
basePath = os.path.join(Config.get("PATHS", "catalogsDir"))
pathToPot = os.path.join(Config.get("PATHS", ".potFile"))

class CLImessageClient(object):
    def clearScreen(self):
        if os.name == 'nt':
            _ = os.system('cls') 
        else: 
            _ = os.system('clear') 

    def askIfConfident(self, message, option):
        try:
            if option == 2:
                print("Are you sure you want to modify the record: \nMessage id: " + message)
            elif option == 3:
                print("Are you sure you want to delete the record: \nMessage id: " + message)
            elif option == 4:
                print("Are you sure you want to delete the whole \"" + message + "\" language")
            confident = int(raw_input("0: No\n1: Yes\n:"))
            if confident > 1 or confident < 0:
                raise Exception("Invalid Option")
            if confident == 0:
                print("Action aborted successfully")
                return False
            return confident
        except:
            print("Invalid Option")
            print("")
            return False

class CentralMechanism(object):
    def __init__(self):
        self.PathHandler = PathHandler(basePath)
        self.FileManager = FileManager()

    def cleanMessages(self, message):
        cleanMessage = message
        messagesDictionary = self.textToDictionary(message)
        cleanMessage = self.dictionaryToText(messagesDictionary)
        return cleanMessage

    def getDictionary(self, language, pathLanguages, pathToPot):
        pathToLanguages = pathLanguages
        if language == "all":
            pathToMessages = pathToPot
        else:
            pathToMessages = self.PathHandler.buildPathMessages(pathToLanguages, language)
        __message = self.FileManager.readfile(pathToMessages)
        __message = self.cleanMessages(__message)
        __messageDictionary = self.textToDictionary(__message)
        return __messageDictionary

    def compareCatalogs(self, firstLanguage, secondLanguage, pathLanguages, pathToPot):
        firstMessages = self.getDictionary(firstLanguage, pathLanguages, pathToPot)
        secondMessages = self.getDictionary(secondLanguage, pathLanguages, pathToPot)
        helper = 0
        helperList = []
        if len(firstMessages) >= len(secondMessages):
            for x in firstMessages:
                firstHelper = helper
                for y in secondMessages:
                    if x == y:
                        helper += 1
                if firstHelper == helper:
                    helperList.append(x)
            if helper == len(firstMessages):
                print("Every Message in the \"" + firstLanguage + "\" file exists in \"" + secondLanguage + "\"")
                print("")
                return None
            else:
                print("The catalog for the \"" + firstLanguage + "\" file is larger than the \"" + secondLanguage + "\" catalog")
                for x in helperList:
                    print("Message id: \"" + x + "\" is on the .pot file catalog but not in the \"" + secondLanguage + "\" catalog")
                    print("")
        else:
            for x in secondMessages:
                firstHelper = helper
                for y in firstMessages:
                    if x == y:
                        helper += 1
                if firstHelper == helper:
                    helperList.append(x)
            print("The catalog for \"" + secondLanguage + "\" is larger than the \"" + firstLanguage + "\" file catalog")
            print("")
            for x in helperList:
                print("Message id: \"" + x + "\" is on \"" + secondLanguage + "\" catalog but not in the \"" + firstLanguage + "\" file")
                print("")

    def dictionaryToText(self, messagesDictionary, option = 0):
        messagesDictionary = messagesDictionary
        idsList = sorted(messagesDictionary)
        repeatedIdsList = []
        obsoleteIdsList = []
        newString = ""
        repeatedString = ""
        obsoleteString = ""
        obsoleteQuantity = 0
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
            elif idsList[x] == "//Obsolete":
                obsoleteIdsList = sorted(messagesDictionary[idsList[x]])
                for y in range(len(obsoleteIdsList)):
                    obsoleteQuantity += 1
                    if messagesDictionary[idsList[x]][obsoleteIdsList[y]]["Comments"] != "":
                        obsoleteString += messagesDictionary[idsList[x]][obsoleteIdsList[y]]["Comments"] + "\n"
                    obsoleteString += "#~ msgid \""
                    obsoleteString += obsoleteIdsList[y] + "\"\n"
                    obsoleteString += "#~ msgstr \""
                    obsoleteString += messagesDictionary[idsList[x]][obsoleteIdsList[y]]["msgstr"] + "\"\n\n"
            else:
                if messagesDictionary[idsList[x]]["Comments"] != "" and messagesDictionary[idsList[x]]["Comments"] != None:
                    if "#:" not in messagesDictionary[idsList[x]]["Comments"]:
                        newString += "#: "
                    newString += messagesDictionary[idsList[x]]["Comments"] + "\n"
                newString += "msgid \""
                newString += idsList[x] + "\"\n"
                newString += "msgstr \""
                newString += messagesDictionary[idsList[x]]["msgstr"] + "\"\n\n"
        if option == 1 and repeatedQuantity > 0:
            newString += "\n############################################ Repeated Message Id's ############################################\n"
        newString += repeatedString
        if option == 1 and obsoleteQuantity > 0:
            newString += "\n############################################ Obsolete Message Id's ############################################\n"
        newString += obsoleteString
        if option == 1 and repeatedQuantity > 0:
            newString += "############# Repeated Quantity: " + str(repeatedQuantity) + " #############\n"
        if option == 1 and obsoleteQuantity > 0:
            newString += "############# Obsolete Quantity:    " + str(obsoleteQuantity) + " #############\n"
        return newString

    def textToDictionary(self, message):
        messageList = message.split("\n\n")
        messageDic = {}
        repeatedDic = {}
        obsoleteDic = {}
        a = 0
        for x in range(len(messageList)):
            a = a +1
            wholeLine = ""
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
                obsoleteDic[msgid] = {"Comments" : commentsLine, "msgstr" : msgstr, 
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
        self.__obsolete = len(obsoleteDic)
        messageDic["//Repeated"] = repeatedDic
        messageDic["//Obsolete"] = obsoleteDic
        return messageDic

    def addMessage(self, newMessage, newComment,messageDictionary):
        messageDictionary = messageDictionary
        newMsgid = newMessage
        Comment = newComment
        if newMsgid in messageDictionary:
            print("-- The \"" +  newMessage + "\" Message Id already exists")
            print("")
            return None
        else:  
            messageDictionary[newMsgid] = {"Comments" : Comment, "msgstr" : ""}
            return messageDictionary

    def searchMessage(self, message, messageDictionary, language, verbose):
        specificMessage = message
        if any(char.isdigit() for char in specificMessage):
            print("Message id's does not contain numbers")
            print("")
            return None
        if specificMessage in messageDictionary:
            if verbose:
                print("#########  \"" + language + "\" Catalog  #########")
                print("Message Id: " + specificMessage)
                print("Message Translation: " + messageDictionary[specificMessage]["msgstr"])
                print("Message Comments: " + messageDictionary[specificMessage]["Comments"])
                print("")
            messageInfo = {specificMessage : messageDictionary[specificMessage]}
            return messageInfo
        else:
            print("-- The \"" +  message + "\" Message Id doesn't exist in the \"" + language + "\" Catalog")
            print("")
            return "Empty"
                
    def modifyMessage(self, messageDictionary, exMessage, newMessageId, comment, translation, option):
        messageDictionary = messageDictionary
        message = exMessage
        messageId = message.keys()[0]
        messageStr = message[message.keys()[0]]["msgstr"]
        messageComments = message[message.keys()[0]]["Comments"]
        newMessageId = newMessageId
        newMessageStr = translation
        newMessageComments = comment
        if option == 2:
            if newMessageId != "":
                try:
                    newMessageId = newMessageId
                    if any(char.isdigit() for char in newMessageId):
                        raise Exception("Message Id's should have only letters")
                except:
                    print("Error: Message Translations should have only letters")
                    print("")
                    return None
                if newMessageComments == "":
                    newMessageComments = messageComments
                else:
                    try:
                        newMessageComments = newMessageComments
                    except:
                        print("Error: Unknown Comment changes errors")
                        print("")
                        return None                    
            else:
                newMessageId = messageId
                if newMessageStr == "":
                    newMessageStr = messageStr
                else:
                    try:
                        newMessageStr = newMessageStr
                        if any(char.isdigit() for char in newMessageStr):
                            raise Exception("Message Translations should have only letters")
                    except:
                        print("Error: Message Translations should have only letters")
                        print("")
                        return None
                if newMessageComments == "":
                    newMessageComments = messageComments
                else:
                    try:
                        newMessageComments = newMessageComments
                    except:
                        print("Error: Unknown Comment changes errors")
                        print("")
                        return None
            del messageDictionary[messageId]
            messageDictionary[newMessageId] = {"Comments" : newMessageComments, "msgstr" : newMessageStr}
        elif option == 3:
            del messageDictionary[messageId]
        return messageDictionary

class PathHandler(object):
        def __init__(self, basePath):
            self.basePath = basePath

        def buildPathMessages(self, pathToLanguages, language):
            path = os.path.join(self.buildPath(language), "messages.po")
            return path
        
        def buildPath(self, language):
            return os.path.join(self.basePath, language, "LC_MESSAGES")
        
        def listLanguages(self,pathLanguages):
            return os.listdir(self.basePath)
            
class BabelManager(CommandLineInterface):
    def compile(self, pathToCatalog, language, verbose):
        path = os.path.join(pathToCatalog,"messages")
        babArgs = []
        babArgs.append("pybabel")
        if not verbose:
            babArgs.append("-q")
        babArgs.append("compile")
        babArgs.append("-i")
        babArgs.append(path + ".po")
        babArgs.append("-l")
        babArgs.append(language)
        babArgs.append("-o")
        babArgs.append(path + ".mo")
        try:
            CommandLineInterface().run(babArgs)
            if verbose:
                print("Compile Completed")
                print("")
        except:
            pass

    def extract(self, pathToCatalog):
        path = os.path.join(pathToCatalog,"messages")
        babArgs = []
        babArgs.append("pybabel")
        babArgs.append("extract")
        babArgs.append(path + ".po")
        babArgs.append("-o")
        babArgs.append("messages.pot")
        try:
            CommandLineInterface().run(babArgs)
            print("Extract to .pot Completed")
            print("")
        except:
            pass

    def init(self, newLanguage, pathToCatalog, pathToPot, verbose):
        path = os.path.join(pathToCatalog,"messages.po")
        babArgs = []
        babArgs.append("pybabel")
        if verbose:
            babArgs.append("-q")
        babArgs.append("init")
        babArgs.append("-l")
        babArgs.append(newLanguage)
        babArgs.append("-i")
        babArgs.append(pathToPot)
        babArgs.append("-o")
        babArgs.append(path)
        try:
            CommandLineInterface().run(babArgs)
            if verbose:
                print("\"" + newLanguage + "\" Initialized successfully")
                print("")
        except:
            pass
    
    def update(self, pathToCatalog, pathToPot, language, verbose):
        path = os.path.join(pathToCatalog,"messages.po")
        babArgs = []
        babArgs.append("pybabel")
        if not verbose:
            babArgs.append("-q")
        babArgs.append("update")
        babArgs.append("-i")
        babArgs.append(pathToPot)
        babArgs.append("-l")
        babArgs.append(language)
        babArgs.append("-o")
        babArgs.append(path)
        try:
            CommandLineInterface().run(babArgs)
            if verbose:
                print("Update Completed")
                print("")
        except:
            pass

class FileManager(object):

    def readfile(self, path):
        messages = open(path).read()
        return messages

    def writefile(self, message, path, verbose):
        file = open(path, "w")
        file.write(message)
        if verbose:
            print("Successful write on \"" + path + "\"") 

class Core(object):
    pathLanguages = ""
    language = ""
    __pathCatalog = ""
    pathToPot = ""
    __pathMessages = ""
    __message = ""
    __messageDictionary = {}
    __repeated = 0
    option = 0

    def __init__(self, basePath, pathToPot):
        self.pathLanguages = basePath
        self.pathToPot = pathToPot
        self.PathHandler = PathHandler(basePath)
        self.CLImessageClient = CLImessageClient()
        self.FileManager = FileManager()
        self.BabelManager = BabelManager()
        self.CentralMechanism = CentralMechanism()

    def verifyCatalogs(self, args):
        pathLanguages = self.pathLanguages
        allLanguages = self.PathHandler.listLanguages(pathLanguages)
        for x in allLanguages:
            print("#########  " + x + " Catalog  #########")
            self.CentralMechanism.compareCatalogs("all", x, pathLanguages, self.pathToPot)
            print("")

    def searchMessageInCatalogs(self, args):
        message = args.messageId.split("\"")[0]
        language = args.exLan
        pathLanguages = self.pathLanguages
        __message = message
        __messageDictionary = {}
        allLanguages = [language]
        if language == "all":
            allLanguages = self.PathHandler.listLanguages(pathLanguages)
        for x in range(len(allLanguages)):
            language = allLanguages[x]
            __messageDictionary = self.CentralMechanism.getDictionary(language, self.pathLanguages, self.pathToPot)
            help = self.CentralMechanism.searchMessage(message ,__messageDictionary, language, True)
            print("")
            if help == None:
                break
        __message = ""
        __messageDictionary = {} 
    
    def addLanguageCatalog(self, args):
        language = args.newLan
        pathLanguages = self.pathLanguages
        allLanguages = self.PathHandler.listLanguages(pathLanguages)
        verbose = args.Verbose
        if language not in allLanguages:
            pathToPot = self.pathToPot
            pathToCatalog = self.PathHandler.buildPath(language)
            self.BabelManager.init(language,pathToCatalog,pathToPot, verbose)
            self.BabelManager.compile(pathToCatalog, language, verbose)
            print("-- Language \"" + language + "\" added successfully")
        else:
            print("The \"" + language + "\" language already exists.")
            print("")

    def addMessageToCatalogs(self, args):
        newMessage = args.messageId
        newComment = args.Comment
        verbose = args.Verbose
        pathLanguages = self.pathLanguages
        pathToPot = self.pathToPot
        allLanguages = self.PathHandler.listLanguages(pathLanguages)
        __message = ""
        __messageDictionary = {}
        __messageDictionary = self.CentralMechanism.getDictionary("all", self.pathLanguages, self.pathToPot)
        __messageDictionary = self.CentralMechanism.addMessage(newMessage, newComment, __messageDictionary)
        if __messageDictionary != None:
            __message = self.CentralMechanism.dictionaryToText(__messageDictionary)
            self.FileManager.writefile(__message, pathToPot, verbose)
            print("-- Message \"" + newMessage + "\" added successfully")
            for x in range(len(allLanguages)):
                __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                self.BabelManager.update(__pathToCatalog, pathToPot, allLanguages[x], verbose)
                self.BabelManager.compile(__pathToCatalog, allLanguages[x], verbose)  
        __message = ""
        __messageDictionary = {} 
        
    def modifyMessageInCatalog(self, args):
        language = args.exLan
        exMessage = args.exMessageId.split("\"")[0]
        verbose = args.Verbose
        try:
            newMessageId = args.messageId.split("\"")[0]
        except:
            newMessageId = ""
        try:
            translation = args.Translation.split("\"")[0]
        except:
            translation = ""
        try:
            comment = args.Comment.split("\"")[0]
        except:
            comment = ""
        self.option = 2
        pathLanguages = self.pathLanguages
        pathToPot = self.pathToPot
        allLanguages = self.PathHandler.listLanguages(pathLanguages)
        __messageDictionary = self.CentralMechanism.getDictionary(language, self.pathLanguages, self.pathToPot)
        toBeModified = self.CentralMechanism.searchMessage(exMessage, __messageDictionary, language, verbose)
        ask = args.force
        if toBeModified != None and toBeModified != "Empty" and ask == False:
            ask = self.CLImessageClient.askIfConfident(exMessage, self.option)
        if ask != False:
            __messageDictionary = self.CentralMechanism.modifyMessage(__messageDictionary, toBeModified, newMessageId, comment, translation, self.option)
            __message = self.CentralMechanism.dictionaryToText(__messageDictionary)
            if language != "all":
                __pathToCatalog = os.path.join(pathLanguages, language, "LC_MESSAGES")
                __pathMessages = os.path.join(__pathToCatalog, "messages.po")
                self.FileManager.writefile(__message, __pathMessages, verbose)
                print("-- Message modified successfully on \""+ language +"\" file")
                self.BabelManager.compile(__pathToCatalog, language, verbose)
            else:
                self.FileManager.writefile(__message, pathToPot, verbose)
                print("-- Message modified successfully on .pot file")
                for x in range(len(allLanguages)):
                    __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                    self.BabelManager.update(__pathToCatalog, pathToPot, allLanguages[x], verbose)
                    self.BabelManager.compile(__pathToCatalog, allLanguages[x], verbose)
                
    def deleteMessageInCatalogs(self, args):
        language = "all"
        message = args.messageId.split("\"")[0]
        verbose = args.Verbose
        self.option = 3
        pathLanguages = self.pathLanguages
        pathToPot = self.pathToPot
        allLanguages = self.PathHandler.listLanguages(pathLanguages)
        __messageDictionary = self.CentralMechanism.getDictionary(language, self.pathLanguages, self.pathToPot)
        toBeDeleted = self.CentralMechanism.searchMessage(message, __messageDictionary, language, verbose)
        ask = args.force
        if toBeDeleted != None and toBeDeleted != "Empty" and ask == False:
            ask = self.CLImessageClient.askIfConfident(message, self.option)
        if ask != False:
            if toBeDeleted != None:
                __messageDictionary = self.CentralMechanism.modifyMessage(__messageDictionary, toBeDeleted, "", "", "", self.option)
                __message = self.CentralMechanism.dictionaryToText(__messageDictionary)
                self.FileManager.writefile(__message, pathToPot, verbose)
                print("-- Message \"" + message + "\" deleted successfully")
                for x in range(len(allLanguages)):
                    __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                    self.BabelManager.update(__pathToCatalog, pathToPot, allLanguages[x], verbose)
                    self.BabelManager.compile(__pathToCatalog, allLanguages[x], verbose)
            
    def deleteLanguageCatalog(self, args):
        language = args.exLan
        self.option = 4
        pathLanguages = self.pathLanguages
        ask = args.force
        if ask == False:
            ask = self.CLImessageClient.askIfConfident(language, self.option)
        if ask != False:
            pathLanguage = os.path.join(pathLanguages, language)
            shutil.rmtree(pathLanguage)
            print("-- The deletion of the \"" + language + "\" language was successful")

    def addTranslations(self,args):
        print(args)
        language = args.exLan
        translationPath = args.File
        verbose = args.Verbose
        if args.File != (None or False) and args.Stdin:
            print("Error, only one option between File and Stdin can be used")
            sys.exit()
        __lanDictionary = self.CentralMechanism.getDictionary(language, self.pathLanguages, self.pathToPot)
        if args.File != (None or False):
            try:
                __translations = csv.reader(open(translationPath), delimiter=',')
            except: 
                print("The path:\"" + translationPath + "\"doesn't lead to a language translations")
                print("")
                return None
            __translationsDictionary = [x for x in __translations]
        elif args.Stdin:
            __translations = sys.stdin.readlines()
            __translationsDictionary = [x[:-1].split(",") for x in __translations]
        notUsedDic = {}
        notExistingList = []
        for x in __translationsDictionary: 
            translation = x[1]
            if x[0] in __lanDictionary:
                if translation != "":
                    __lanDictionary[x[0]]["msgstr"] = translation
                else:
                    notUsedDic[x] = x
            else:
                notExistingList.append(translation)
        notUsedDic = __lanDictionary
        if verbose:
            if notUsedDic != {}:
                print("The next dictionary contains the elements that didn't get a translation")
                notUsed = self.CentralMechanism.dictionaryToText(__lanDictionary)
                print(notUsed)
                print("")
            if notExistingList != []:
                print("The next list contains the elements that didn't exist on the selected language")
                print(notExistingList)
                print("")
        print("Elements that didn't get a translation: " + str(len(notUsedDic)))
        print("Elements that didn't exist in the selected language: " + str(len(notExistingList)))
        print("")
        messages = self.CentralMechanism.dictionaryToText(__lanDictionary)
        pathLanguages = self.pathLanguages
        __pathToCatalog = os.path.join(pathLanguages, language, "LC_MESSAGES")
        __pathMessages = os.path.join(__pathToCatalog, "messages.po")
        self.FileManager.writefile(messages, __pathMessages, verbose)
        print("Translations added succesfully")
        print("")

class Runner(object):
    def __init__(self, basePath, pathToPot):
        self.pathLanguages = basePath
        self.PathHandler = PathHandler(basePath)
        self.Core = Core(self.pathLanguages, pathToPot)
        self.CLI(sys.argv)
    
    def CLI(self, args):
        options = ["aL","aM", "s", "mM", "v", "dM", "dL", "h", "aT"]
        optionsLong = ["addLanguage","addMessage", "search", "modifyMessage", "verify", "deleteMessage", "deleteCatalog", "--help", "addTranslations"]
        languages = self.PathHandler.listLanguages(self.pathLanguages)
        languages.append("all")

        option = []
        argsL = args

        self.__pathCatalog = ""
        self.__pathMessages = ""
        if len(argsL) < 2:
            print("No argument recieved, exiting. See --help if needed.")
            print("")
        else:
            for x in options:
                if argsL[1] == x:
                    option.append(x)
            if len(option) == 0:
                for x in range(len(optionsLong)):
                    if argsL[1] == optionsLong[x]:
                        optionShort = options[x]
                        option.append(optionShort)
                        argsL[1] = optionShort
            if len(option) == 0:
                print("No valid first argument given, see --help if needed.")
                print("")
            elif len(option) > 1:
                print("Too many actions, just one per run allowed, see --help if needed.")
                print("")
            else:
                parser = argparse.ArgumentParser(prog=argsL[0], description="Options for management of .po catalogs")
                del argsL[0]
                subparsers = parser.add_subparsers(title="Accepted commands", description="Available Options")

                parser_v = subparsers.add_parser("v",help = "verify:\n Allows to verify that every Language Catalog has the same Message Id's")
                parser_v.set_defaults(func=self.Core.verifyCatalogs)

                parser_s = subparsers.add_parser("s",help = "search:\n Allows to search a message through a Message Id, result is either if exists and if a language is selected also shows its Comments and Translation")
                parser_s.add_argument("messageId", metavar="Message_Id")
                parser_s.add_argument("exLan", choices=languages, nargs='?',  default = "all",  metavar="Language", help="Language to search in, for all languages: all")
                parser_s.set_defaults(func=self.Core.searchMessageInCatalogs)

                parser_aL = subparsers.add_parser("aL",help = "addLanguage:\n Allows to add a new language with the Message Id's already added")
                parser_aL.add_argument("newLan", metavar="New_Language", help="Language to be added")
                parser_aL.add_argument("-V","--Verbose", action='store_true', help = "Show as much of the process")
                parser_aL.set_defaults(func=self.Core.addLanguageCatalog)

                parser_aM = subparsers.add_parser("aM",help = "addMessage:\n Allows to add a message, either to one language or all")
                parser_aM.add_argument("messageId", metavar="New_Message_Id", help="The Message Id should go wrapped in quotation marks")
                parser_aM.add_argument("-C","--Comment", metavar="Message_Comment", help="The Message Comment should go wrapped in quotation marks")
                parser_aM.add_argument("-V","--Verbose", action='store_true', help = "Show as much of the process")
                parser_aM.set_defaults(func=self.Core.addMessageToCatalogs)

                parser_mM = subparsers.add_parser("mM",help = "modifyMessage:\n Allows to modify a Message Id, and if a language is selected then allow to modify Comment and/or Translation")
                parser_mM.add_argument("exMessageId", metavar="Message_Id", help="The Message Id should be wrapped wrapped in quotation marks and it's Caps Sensitive")
                if(("all" in argsL) or "-h" in argsL or "--help" in argsL):
                    parser_mM.add_argument("messageId", metavar="New_Message_Id", help="The New message Id should be wrapped in quotation marks, only allowed to be used when applied to all languages")
                parser_mM.add_argument("-C","--Comment", metavar="Message_Comment", help="The Message Comment should go wrapped in quotation marks, only allowed to be used when applied to a certain language")
                if(("all" not in argsL) or "-h" in argsL or "--help" in argsL):
                    parser_mM.add_argument("-T","--Translation", metavar="Message_Translation", help="The Message Translation should go wrapped in quotation marks, only allowed to be used when applied to only one language")
                parser_mM.add_argument("exLan", choices=languages, metavar="Language", help= "Language to search in, for changes on Translation use ")
                parser_mM.add_argument("-f","--force", action='store_true', help = "Force the action, no questions asked")
                parser_mM.add_argument("-V","--Verbose", action='store_true', help = "Show as much of the process")
                parser_mM.set_defaults(func=self.Core.modifyMessageInCatalog)

                parser_dM = subparsers.add_parser("dM",help = "deleteMessage:\n Allow to delete a Message Id in all catalogs or if language provided only in said language")
                parser_dM.add_argument("messageId", metavar="Message_Id", help = "Message Id to be deleted")
                parser_dM.add_argument("-f","--force", action='store_true', help = "Force the action, no questions asked")
                parser_dM.add_argument("-V","--Verbose", action='store_true', help = "Show as much of the process")
                parser_dM.set_defaults(func=self.Core.deleteMessageInCatalogs)

                parser_dL = subparsers.add_parser("dL", help = "deleteCatalog:\n Allows to delete a whole Language's Message Catalog")
                parser_dL.add_argument("exLan", choices=languages, metavar="Language", help= "Language to delete its Catalog")
                parser_dL.add_argument("-f","--force", action='store_true', help = "Force the action, no questions asked")
                parser_dL.add_argument("-V","--Verbose", action='store_true', help = "Show as much of the process")
                parser_dL.set_defaults(func=self.Core.deleteLanguageCatalog)

                parser_aT = subparsers.add_parser("aT",help = "addTranslations:\n Allows to allow a massive catalog of translations to an initiated Catalog")
                parser_aT.add_argument("exLan", choices=languages, metavar="Language", help= "Language to add Translations to its Catalog")
                parser_aT.add_argument("-F","--File", nargs='?',  default = False, help = "Expect a file path")
                parser_aT.add_argument("-S","--Stdin", action='store_true', help = "Expect a Standard Input before")
                parser_aT.add_argument("-V","--Verbose", action='store_true', help = "Show the whole list of messages not updated and not used")
                parser_aT.set_defaults(func=self.Core.addTranslations)
                
                print("")
                arguments = parser.parse_args(argsL)
                arguments.func(arguments)
                print("")      

if __name__ == "__main__":
    Runner(basePath, pathToPot)