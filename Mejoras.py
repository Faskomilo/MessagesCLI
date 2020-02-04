import os, time, argparse, sys, shutil
try:
    from babel.messages.frontend import CommandLineInterface
except:
    print("")
    print("Install Babel before trying to run this program")
    print("")
    sys.exit(0)

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
            if self.option == 2:
                print("Are you sure you want to modify the record: \nMessage id: " + message)
            elif self.option == 3:
                print("Are you sure you want to delete the record: \nMessage id: " + message)
            elif self.option == 4:
                print("Are you sure you want to delete the whole \"" + message + "\" language")
            confident = int(raw_input("0: No\n1: Yes\n:"))
            if confident > 1 or confident < 0:
                raise Exception("Invalid Option")
            if confident == 0:
                print("Action aborted succesfully")
                return None
            return confident
        except:
            print("")
            print("Invalid Option")
            print("")
            return None

    def getDictionary(self, language):
        pathToLanguages = self.pathLanguages
        if language == "all":
            pathToMessages = self.pathToPot
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
                    helperList.append(x)
            if helper == len(firstMessages):
                print("")
                print("Every Message in the .pot file exists in " + secondLanguage)
                return None
            else:
                print("The catalog for the .pot file is larger than the " + secondLanguage + " catalog")
                for x in helperList:
                    print("")
                    print("Message id: " + x + " is on the .pot file catalog but not in the \"" + secondLanguage + "\" catalog")
        else:
            for x in secondMessages:
                firstHelper = helper
                for y in firstMessages:
                    if x == y:
                        helper += 1
                if firstHelper == helper:
                    helperList.append(x)
            print("")
            print("The catalog for " + secondLanguage + " is larger than the .pot file catalog")
            for x in helperList:
                print("")
                print("Message id: " + x + " is on " + secondLanguage + " catalog but not in the .pot file")

    def dictionaryToText(self, messagesDictionary):
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
                    newString += messagesDictionary[idsList[x]]["Comments"] + "\n"
                newString += "msgid \""
                newString += idsList[x] + "\"\n"
                newString += "msgstr \""
                newString += messagesDictionary[idsList[x]]["msgstr"] + "\"\n\n"
        if self.option == 1 and repeatedQuantity > 0:
            newString += "\n############################################ Repeated Message Id's ############################################\n"
        newString += repeatedString
        if self.option == 1 and obsoleteQuantity > 0:
            newString += "\n############################################ Obsolete Message Id's ############################################\n"
        newString += obsoleteString
        if self.option == 1 and repeatedQuantity > 0:
            newString += "############# Repeated Quantity: " + str(repeatedQuantity) + " #############\n"
        if self.option == 1 and obsoleteQuantity > 0:
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
            print("")
            return None
        if specificMessage in messageDictionary:
            print("#########  \"" + language + "\" Catalog  #########")
            print("Message Id: " + specificMessage)
            print("Message Translation: " + messageDictionary[specificMessage]["msgstr"])
            print("Message Comments: " + messageDictionary[specificMessage]["Comments"])
            print("")
            messageInfo = {specificMessage : messageDictionary[specificMessage]}
            return messageInfo
        else:
            print("That Message Id doesn't exist in the \"" + language + "\" Catalog")
            print("")
            return "Empty"
                
    def modifyMessage(self, messageDictionary, exMessage, newMessageId, comment, translation):
        messageDictionary = messageDictionary
        message = exMessage
        messageId = message.keys()[0]
        messageStr = message[message.keys()[0]]["msgstr"]
        messageComments = message[message.keys()[0]]["Comments"]
        newMessageId = newMessageId
        newMessageStr = translation
        newMessageComments = comment
        if self.option == 2:
            if newMessageId != "":
                try:
                    newMessageId = newMessageId
                    if any(char.isdigit() for char in newMessageId):
                        raise Exception("Message Id's should have only letters")
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
            del messageDictionary[messageId]
            messageDictionary[newMessageId] = {"Comments" : newMessageComments, "msgstr" : newMessageStr}
        elif self.option == 3:
            del messageDictionary[messageId]
            print("\nThe element has been succesfully deleted")
            print("")
        return messageDictionary

class PathHandler(object):
        def __init__(self, basePath):
            self.buildPath = basePath

        def buildPathLanguage(self, pathToLanguages, language):
            path = os.path.join(self.buildLanguagePath(language), "messages.po")
            if os.path.isfile(path):
                return path 
        
        def buildLanguagePath(self, language):
            return os.path.join(self.buildPath, language, "LC_MESSAGES")
        
        def listLanguages(self,pathLanguages):
            return os.listdir(self.buildPath) 
            
class SpecificRecord(object):
    pass

class FileManager(CommandLineInterface):

    def getFile(self, path, content=None,mode='r', verbose=False):
        result = None
        with open(path,mode) as _file:
            if mode == 'r':
                result = _file.read()
            elif mode == 'w':
                _file.write(content)
                result = True
                if verbose:
                    print("Write succesfull on \"" + path + "\"") 
        return result

class babelManger(object):
    
    def __init__(self, pathToCatalog):
        self.pathToCatalog = pathToCatalog
        self.interface = CommandLineInterface()

    def compile(self, language):
        print("")
        path = os.path.join(self.pathToCatalog,"messages")
        babArgs = []
        babArgs.append("pybabel")
        babArgs.append("compile")
        babArgs.append("-i")
        babArgs.append(path + ".po")
        babArgs.append("-l")
        babArgs.append(language)
        babArgs.append("-o")
        babArgs.append(path + ".mo")
        try:
            self.interface.run(babArgs)
            print("Compile Completed")
        except:
            pass
        print("")

    def extract(self, pathToCatalog):
        print("")
        path = os.path.join(pathToCatalog,"messages")
        babArgs = []
        babArgs.append("pybabel")
        babArgs.append("extract")
        babArgs.append(path + ".po")
        babArgs.append("-o")
        babArgs.append("messages.pot")
        try:
            self.interface.run(babArgs)
            print("Extract to .pot Completed")
        except:
            pass
        print("")

    def init(self, newLanguage, pathToCatalog, pathToPot):
        print("")
        path = os.path.join(pathToCatalog,"messages.po")
        babArgs = []
        babArgs.append("pybabel")
        babArgs.append("init")
        babArgs.append("-l")
        babArgs.append(newLanguage)
        babArgs.append("-i")
        babArgs.append(pathToPot)
        babArgs.append("-o")
        babArgs.append(path)
        try:
            self.interface.run(babArgs)
            print("\"" + newLanguage + "\" Initialized Succesfully")
        except:
            pass
        print("")
    
    def update(self, pathToCatalog, pathToPot, language):
        print("")
        path = os.path.join(pathToCatalog,"messages.po")
        babArgs = []
        babArgs.append("pybabel")
        babArgs.append("update")
        babArgs.append("-i")
        babArgs.append(pathToPot)
        babArgs.append("-l")
        babArgs.append(language)
        babArgs.append("-o")
        babArgs.append(path)
        try:
            self.interface.run(babArgs)
            print("Update Completed")
        except:
            pass
        print("")

class Runner(CLImessageClient,PathHandler,SpecificRecord,FileManager):
    pathLanguages = ""
    language = ""
    __pathCatalog = ""
    pathToPot = ""
    __pathMessages = ""
    optionLan = 0
    __message = ""
    __messageDictionary = {}
    __repeatedDic = {}
    __repeated = 0
    option = 0


    def __init__(self, languages,pot):
        self.pathLanguages = languages
        self.pathToPot = pot
        self.pathHandler = PathHandler(self.pathLanguages)
        self.CLI(sys.argv)
    
    def CLI(self, args):
        options = ["aL","aM", "s", "mM", "v", "dM", "dL", "h", "aT"]
        optionsLong = ["addLanguage","addMessage", "search", "modifyMessage", "verify", "deleteMessage", "deleteCatalog", "--help", "addTranslations"]
        languages = self.listLanguages(self.pathLanguages)
        languages.append("all")

        option = []
        argsL = args

        self.__pathCatalog = ""
        self.__pathMessages = ""
   
        for x in options:
            if argsL[1] == x:
                option.append(x)
        if not option:
            for item in optionsLong:
                if argsL[1] == item:
                    optionShort = options[x]
                    option.append(optionShort)
                    argsL[0] = optionShort
        if len(option) == 0:
            print("No valid first argument given, see --help if needed.")
            print("")
        elif len(option) > 1:
            print("Too many actions, just one per run allowed, see --help if needed.")
            print("")
        else:
            parser = argparse.ArgumentParser(prog=argsL[0], description="Options for management of .po catalogs")
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
            parser_mM.add_argument("exMessageId", metavar="Message_Id")
            if(("all" in argsL) or "-h" in argsL or "--help" in argsL):
                parser_mM.add_argument("messageId", metavar="New_Message_Id", help="The New message Id should be wrapped wrapped in quotation marks, only allowed to be used when applied to all languages")
            parser_mM.add_argument("-C","--Comment", metavar="Message_Comment", help="The Message Comment should go wrapped in quotation marks")
            parser_mM.add_argument("exLan", choices=languages, metavar="Language", help= "Language to search in, for changes on Translation use ")
            if(("all" not in argsL) or "-h" in argsL or "--help" in argsL):
                parser_mM.add_argument("-T","--Translation", metavar="Message_Translation", help="The Message Translation should go wrapped in quotation marks")
            parser_mM.set_defaults(func=self.modifyMessageInCatalog)

            parser_dM = subparsers.add_parser("dM",help = "deleteMessage:    Allow to delete a Message Id in all catalogs or if language provided only in said language")
            parser_dM.add_argument("messageId", metavar="Message_Id", help = "Message Id to be deleted")
            parser_dM.set_defaults(func=self.deleteMessageInCatalogs)

            parser_dL = subparsers.add_parser("dL",help = "deleteCatalog:    Allows to delete a whole Language's Message Catalog")
            parser_dL.add_argument("exLan", choices=languages, metavar="Language", help= "Language to delete its Catalog")
            parser_dL.set_defaults(func=self.deleteLanguageCatalog)

            parser_aT = subparsers.add_parser("aT",help = "addTranslations:    Allows to allow a massive catalog of translations to an initiated Catalog")
            parser_aT.add_argument("exLan", choices=languages, metavar="Language", help= "Language to add Translations to its Catalog")
            parser_aT.add_argument("pathToTrans", metavar="Translations_File", help= "Catalog of Translations")                
            parser_aT.set_defaults(func=self.addTranslations)

            arguments = parser.parse_args(argsL)
            arguments.func(arguments)

    def verifyCatalogs(self, args):
        pathLanguages = self.pathLanguages
        allLanguages = self.listLanguages(pathLanguages)
        for x in allLanguages:
            print("#########  " + x + " Catalog  #########")
            self.compareCatalogs("all", x)
            print("")
            print("")

    def searchMessageInCatalogs(self, args):
        message = args.messageId.split("\"")[0]
        language = args.exLan
        pathLanguages = self.pathLanguages
        __message = message
        __messageDictionary = {}
        allLanguages = [language]
        if language == "all":
            allLanguages = self.listLanguages(pathLanguages)
        for x in range(len(allLanguages)):
            language = allLanguages[x]
            __messageDictionary = self.getDictionary(language)
            help = self.searchMessage(message ,__messageDictionary, language)
            print("")
            if help == None:
                break
        __message = ""
        __messageDictionary = {} 
    
    def addLanguageCatalog(self, args):
        language = args.newLan
        pathToPot = self.pathToPot
        pathToCatalog = self.buildPath(language)
        self.init(language,pathToCatalog,pathToPot)
        self.compile(pathToCatalog, language)

    def addMessageToCatalogs(self, args):
        newMessage = args.messageId
        newComment = args.Comment
        pathLanguages = self.pathLanguages
        pathToPot = self.pathToPot
        allLanguages = self.listLanguages(pathLanguages)
        __message = ""
        __messageDictionary = {}
        __messageDictionary = self.getDictionary("all")
        __messageDictionary = self.addMessage(newMessage, newComment, __messageDictionary)
        if __messageDictionary != None:
            __message = self.dictionaryToText(__messageDictionary)
            self.writefile(__message, pathToPot)
            for x in range(len(allLanguages)):
                __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                self.update(__pathToCatalog, pathToPot, allLanguages[x])
                self.compile(__pathToCatalog, allLanguages[x])  
        __message = ""
        __messageDictionary = {} 
        
    def modifyMessageInCatalog(self, args):
        language = args.exLan
        exMessage = args.exMessageId.split("\"")[0]
        try:
            newMessageId = args.messageId.split("\"")[0]
        except AttributeError:
            newMessageId = ""
        try:
            translation = args.Translation.split("\"")[0]
        except AttributeError:
            translation = ""
        try:
            comment = args.Comment.split("\"")[0]
        except AttributeError:
            comment = ""
        self.option = 2
        pathLanguages = self.pathLanguages
        pathToPot = self.pathToPot
        allLanguages = self.listLanguages(pathLanguages)
        __messageDictionary = self.getDictionary(language)
        toBeModified = self.searchMessage(exMessage, __messageDictionary, language)
        ask = None 
        if toBeModified != None and toBeModified != "Empty":
            ask = self.askIfConfident(exMessage)
        if ask != None:
            __messageDictionary = self.modifyMessage(__messageDictionary, toBeModified, newMessageId, comment, translation)
            __message = self.dictionaryToText(__messageDictionary)
            if language != "all":
                __pathToCatalog = os.path.join(pathLanguages, language, "LC_MESSAGES")
                __pathMessages = os.path.join(__pathToCatalog, "messages.po")
                self.writefile(__message, __pathMessages)
                self.compile(__pathToCatalog, language)
            else:
                self.writefile(__message, pathToPot)
                for x in range(len(allLanguages)):
                    __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                    self.update(__pathToCatalog, pathToPot, allLanguages[x])
                    self.compile(__pathToCatalog, allLanguages[x])
                
    def deleteMessageInCatalogs(self, args):
        language = "all"
        message = args.messageId.split("\"")[0]
        self.option = 3
        pathLanguages = self.pathLanguages
        pathToPot = self.pathToPot
        allLanguages = self.listLanguages(pathLanguages)
        __messageDictionary = self.getDictionary(language)
        toBeDeleted = self.searchMessage(message, __messageDictionary, language)
        ask = None 
        if toBeDeleted != None and toBeDeleted != "Empty":
            ask = self.askIfConfident(message)
        if ask != None:
            if toBeDeleted != None:
                __messageDictionary = self.modifyMessage(__messageDictionary, toBeDeleted, "", "", "")
                __message = self.dictionaryToText(__messageDictionary)
                self.writefile(__message, pathToPot)
                for x in range(len(allLanguages)):
                    __pathToCatalog = os.path.join(pathLanguages, allLanguages[x], "LC_MESSAGES")
                    self.update(__pathToCatalog, pathToPot, allLanguages[x])
                    self.compile(__pathToCatalog, allLanguages[x])
            
    def deleteLanguageCatalog(self, args):
        language = args.exLan
        self.option = 4
        pathLanguages = self.pathLanguages
        ask = self.askIfConfident(language)
        if ask != None:
            pathLanguage = os.path.join(pathLanguages, language)
            shutil.rmtree(pathLanguage)
            print("The deletion of the " + language + " language was succesful")
            print("")

    def addTranslations(self,args):
        language = args.exLan
        translationPath = args.pathToTrans
        __lanDictionary = self.getDictionary(language)
        try:
            __translations = self.readfile(translationPath)
        except: 
            print("")
            print("path doesn't lead to a language translations")
            return None
        __translationsDictionary = self.textToDictionary(__translations)
        notUsedDic = {}
        notExistingList = []
        for x in __translationsDictionary: 
            print x
            if x != "//Repeated" and x != "//Obsolete":
                translation = __translationsDictionary[x]["msgstr"]
                if x in __lanDictionary:
                    if translation != "":
                        __lanDictionary[x]["msgstr"] = translation
                    else:
                        notUsedDic[x] = __translationsDictionary[x] 
                else:
                    notExistingList.append(translation)
        notUsedDic = __lanDictionary
        if notUsedDic != {}:
            print("The next dictionary contains the elements that didn't got a translation")
            print(notUsedDic)
            print("")
        if notExistingList != []:
            print("The next list contains the elements that didn't exist on the selected language")
            print(notExistingList)
            print("")
        print("")
        messages = self.dictionaryToText(__lanDictionary)
        pathLanguages = self.pathLanguages
        __pathToCatalog = os.path.join(pathLanguages, language, "LC_MESSAGES")
        __pathMessages = os.path.join(__pathToCatalog, "messages.po")
        self.writefile(messages, __pathMessages)
        print("Translations added")
        print("")

if __name__ == "__main__":
    language = os.path.join(".","languages")
    potPath = os.path.join("..","messages.pot")
    if len(sys.argv) > 1:
        Runner(language, potPath)
    else:
        print("No argument recieved, exiting. See --help if needed.")
        print("")
    
    

