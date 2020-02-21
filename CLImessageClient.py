import os, argparse, sys, shutil, csv, ConfigParser
try:
    from babel.messages.frontend import CommandLineInterface
except:
    print("")
    print("Install Babel 2.8.0 before trying to run this program")
    print("")
    sys.exit(0)

try:
    Config = ConfigParser.ConfigParser()
    if not os.path.isfile("config.ini"):
        raise Exception("config.ini not existant")
    Config.read("config.ini")
    basePath = Config.get("PATHS", "catalogsDir")
    pathToPot = Config.get("PATHS", ".potFile")
    poFile = Config.get("PATHS", "poFile")
    if not os.path.isfile(pathToPot):
        raise Exception("Invalid path to .potFile on config.ini")
    if not os.path.isdir(basePath):
        raise Exception("Invalid path to catalogsDir on config.ini")
except Exception as e:
    print(e)
    print("")
    print("Valid config.ini file needed to run")
    print("")
    sys.exit(0)

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
                raise Exception("** Invalid Option. **")
            if confident == 0:
                print("\"" + message + "\" adition aborted.")
                return False
            return confident
        except:
            print("** Invalid Option. **")
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
        if pathToMessages is not None:
            __message = self.FileManager.readfile(pathToMessages)
            __message = self.cleanMessages(__message)
            __messageDictionary = self.textToDictionary(__message)
            return __messageDictionary
        return None

    def compareCatalogs(self, firstLanguage, secondLanguage, pathLanguages, pathToPot, verbose):
        firstMessages = self.getDictionary(firstLanguage, pathLanguages, pathToPot)
        secondMessages = self.getDictionary(secondLanguage, pathLanguages, pathToPot)
        if firstLanguage is "all":
            firstLanguage = ".pot file"
        if secondLanguage is "all":
            secondLanguage = ".pot file"
        helper = 0
        helperList = []
        if firstMessages is not None and secondMessages is not None:
            if "//Repeated" in firstMessages:
                if len(secondMessages["//Repeated"]) > 0:
                    tmp = firstMessages["//Repeated"]
                    print("** Repeated quantity: " + str(len(tmp)) + " **")
                del firstMessages["//Repeated"]
            if "//Obsolete" in secondMessages:
                if len(secondMessages["//Obsolete"]) > 0:
                    tmp = firstMessages["//Obsolete"]
                    print("** Obsolete quantity: " + str(len(tmp)) + " **")
                del firstMessages["//Obsolete"]
            if len(firstMessages) >= len(secondMessages):
                for x in firstMessages:
                    firstHelper = helper
                    for y in secondMessages:
                        if x == y:
                            helper += 1
                    if firstHelper == helper:
                        helperList.append(x)
                if helper == len(firstMessages):
                    print("\"" + firstLanguage + "\" content in \"" + secondLanguage + "\" content.")
                    print("")
                    return True
                else:
                    print("** \"" + firstLanguage + "\" content is larger than \"" + secondLanguage + "\" content. **")
                    if verbose:
                        for x in helperList:
                            print("** \"" + x + "\" is on the \"" + firstLanguage + "\" but not in the \"" + secondLanguage + "\" catalog. **")
                            print("")
                    return False
            else:
                for x in secondMessages:
                    firstHelper = helper
                    for y in firstMessages:
                        if x == y:
                            helper += 1
                    if firstHelper == helper:
                        helperList.append(x)
                print("** \"" + secondLanguage + "\" content is larger than \"" + firstLanguage + "\" content. **")
                print("")
                if verbose:
                    for x in helperList:
                        print("** \"" + x + "\" is on \"" + secondLanguage + "\" catalog but not in the \"" + firstLanguage + "\" catalog. **")
                        print("")
                return False

    def dictionaryToText(self, messagesDictionary, option = 0):
        self.option = option
        self.messagesDictionary = messagesDictionary
        obsoleteQuantity = 0
        repeatedQuantity = 0
        newString = ""
        repeatedString = ""
        obsoleteString = ""
        if "//Repeated" in self.messagesDictionary:
            repeatedDic = messagesDictionary["//Repeated"]
            repeatedQuantity = len(repeatedDic)
            del self.messagesDictionary["//Repeated"]
            for x in repeatedDic:
                if repeatedDic[x]["Comments"] != "":
                    repeatedString += str(repeatedDic[x]["Comments"]) + "\n"
                repeatedString += "msgid \""
                repeatedString += str(x) + "\"\n"
                repeatedString += "msgstr \""
                repeatedString += str(repeatedDic[x]["msgstr"]) + "\"\n\n"
        if "//Obsolete" in self.messagesDictionary:
            obsoleteDic = messagesDictionary["//Obsolete"]
            del self.messagesDictionary["//Obsolete"]
            obsoleteQuantity = len(obsoleteDic)
            for x in obsoleteDic:
                if obsoleteDic[x]["Comments"] != "":
                    obsoleteString += str(obsoleteDic[x]["Comments"]) + "\n"
                obsoleteString += "#~ msgid \""
                obsoleteString += str(x) + "\"\n"
                obsoleteString += "#~ msgstr \""
                obsoleteString += str(obsoleteDic[x]["msgstr"]) + "\"\n\n"
        for x in self.messagesDictionary:
            if self.messagesDictionary[x]["Comments"] != "" and self.messagesDictionary[x]["Comments"] != None:
                if "#:" not in self.messagesDictionary[x]["Comments"]:
                    newString += "#: "
                newString += str(self.messagesDictionary[x]["Comments"]) + "\n"
            newString += "msgid \""
            newString += str(x) + "\"\n"
            newString += "msgstr \""
            newString += str(self.messagesDictionary[x]["msgstr"]) + "\"\n\n"
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

    def dictionaryToCSV(self, messagesDictionary, pathToFile):
        self.messages = messagesDictionary
        tmp = []
        try:
            if "//Repeated" in self.messages:
                    del self.messages["//Repeated"]
            if "//Obsolete" in self.messages:
                    del self.messages["//Obsolete"]
            for x in self.messages:
                tmp.append([x,self.messages[x]["msgstr"]])
            self.messages = tmp
            tmp = []
            with open(pathToFile, "w") as csvfile:
                header = ["msgid", "msgstr"]
                filewriter = csv.DictWriter(csvfile, fieldnames = header, extrasaction = "ignore", delimiter = ";")
                for x in self.messages:
                    if x[0] is not "":
                        filewriter.writerow({"msgid": x[0], "msgstr": x[1]})
        except Exception as e:
            print("** " + str(e) + " **")
            try:
                os.remove(pathToFile)
            except:
                pass
            return False
        return True

    def textToDictionary(self, message):
        messageList = message.split("\n\n")
        messageDic = {}
        repeatedDic = {}
        obsoleteDic = {}
        a = 0
        for x in messageList:
            a = a +1
            wholeLine = ""
            commentsLine = ""
            msgidLine = ""
            msgstrLine = ""
            msgid = ""
            msgstr = ""
            try:
                wholeLine = x
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
                    print("** Unexpected error on \"" + wholeLine + "\" **")
            if "#~" in msgidLine:
                index = message.index(msgidLine[3:])
                firstInstance = len(message[:index].split("\n"))
                obsoleteDic[msgid] = {"Comments" : commentsLine, "msgstr" : msgstr, 
                    "Line" : firstInstance}
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
            print("** The \"" +  newMessage + "\" Message Id already exists **")
            print("")
            return None
        else:  
            messageDictionary[newMsgid] = {"Comments" : Comment, "msgstr" : ""}
            return messageDictionary

    def searchMessage(self, message, messageDictionary, language, verbose):
        specificMessage = message
        if any(char.isdigit() for char in specificMessage):
            print("** Message id's does not contain numbers **")
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
            print("** \"" + message + "\" doesn't exist in the \"" + language + "\" Catalog **")
            print("")
                
    def modifyMessage(self, messageDictionary, exMessage, newMessageId, comment, translation, option):
        messageDictionary = messageDictionary
        message = exMessage
        messageId = message.keys()[0]
        messageStr = message[messageId]["msgstr"]
        messageComments = message[messageId]["Comments"]
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
                    print("** Error: Message Translations should have only letters. **")
                    print("")
                    return None
                if newMessageComments == "":
                    newMessageComments = messageComments
                else:
                    try:
                        newMessageComments = newMessageComments
                    except:
                        print("** Error: Unknown Comment changes errors **")
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
                            raise Exception("** Message Translations should have only letters **")
                    except:
                        print("** Error: Message Translations should have only letters **")
                        print("")
                        return None
                if newMessageComments == "":
                    newMessageComments = messageComments
                else:
                    try:
                        newMessageComments = newMessageComments
                    except:
                        print("** Error: Unknown Comment changes errors. **")
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
            path = os.path.join(self.buildPath(language), poFile + ".po")
            if not os.path.isfile(path):
                print("** \"" + language + "\" messages file (" + poFile + ".po) does not exist but Directory does exists **")
                return None
            return path
        
        def buildPath(self, language):
            return os.path.join(self.basePath, language, "LC_MESSAGES")
        
        def listLanguages(self,pathLanguages):
            return os.listdir(self.basePath)
            
class BabelManager(CommandLineInterface):
    def compile(self, pathToCatalog, language, verbose):
        path = os.path.join(pathToCatalog,poFile)
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
                print("\""+ language + "\" compiled correctly")
                print("")
            return True
        except:
            print("** \"" + language + "\" messages file (" + poFile + ".po) does not exist but Directory does exists **")
            return None

    def init(self, newLanguage, pathToCatalog, pathToPot, verbose):
        path = os.path.join(pathToCatalog,poFile + ".po")
        babArgs = []
        babArgs.append("pybabel")
        if not verbose:
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
                print("\"" + newLanguage + "\" initialized successfully")
                print("")
            return True
        except:
            print("** Unknown language/locale **")
            return None
    
    def update(self, pathToCatalog, pathToPot, language, verbose):
        path = os.path.join(pathToCatalog,poFile + ".po")
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
                print("\"" + language + "\" updated correctly")
                print("")
            return True
        except:
            print("** \"" + language + "\" messages file (" + poFile + ".po) does not exist but Directory does exists **")
            return None

class FileManager(object):

    def readfile(self, path):
        messages = open(path).read()
        return messages

    def writefile(self, message, path, verbose):
        file = open(path, "w")
        file.write(message)
        if verbose:
            print("\"" + path + "\" succesfully written") 

class Core(object):
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
        verbose = args.Verbose
        for x in allLanguages:
            print("#########  " + x + " Catalog  #########")
            self.CentralMechanism.compareCatalogs("all", x, pathLanguages, self.pathToPot, verbose)
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
            allLanguages.append("all")
        for x in allLanguages:
            language = x
            __messageDictionary = self.CentralMechanism.getDictionary(language, self.pathLanguages, self.pathToPot)
            if __messageDictionary is not None:
                search = self.CentralMechanism.searchMessage(__message, __messageDictionary, language, True)
                if search is None:
                    sys.exit()

    def addLanguageCatalog(self, args):
        language = args.newLan
        pathLanguages = self.pathLanguages
        allLanguages = self.PathHandler.listLanguages(pathLanguages)
        verbose = args.Verbose
        if language not in allLanguages:
            pathToPot = self.pathToPot
            pathToCatalog = self.PathHandler.buildPath(language)
            init = self.BabelManager.init(language,pathToCatalog,pathToPot, verbose)
            if init is not None:
                compiled = self.BabelManager.compile(pathToCatalog, language, verbose)
                if compiled is not None:
                    print("\"" + language + "\" added and initiallized successfully")
        else:
            print("** \"" + language + "\" language already exists **")
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
        if __messageDictionary is not None:
            __messageDictionary = self.CentralMechanism.addMessage(newMessage, newComment, __messageDictionary)
            if __messageDictionary != None:
                __message = self.CentralMechanism.dictionaryToText(__messageDictionary)
                self.FileManager.writefile(__message, pathToPot, verbose)
                print("\"" + newMessage + "\" added successfully")
                for x in allLanguages:
                    __pathToCatalog = os.path.join(pathLanguages, x, "LC_MESSAGES")
                    updated = self.BabelManager.update(__pathToCatalog, pathToPot, x, verbose)
                    if updated is not None:
                        self.BabelManager.compile(__pathToCatalog, x, verbose)
        
    def modifyMessageInCatalog(self, args):
        language = args.exLan
        exMessage = args.exMessageId.split("\"")[0]
        verbose = args.Verbose
        try:
            newMessageId = args.MessageId.split("\"")[0]
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
        if __messageDictionary is not None:
            toBeModified = self.CentralMechanism.searchMessage(exMessage, __messageDictionary, language, verbose)
            ask = args.force
            if toBeModified != None and ask == False:
                ask = self.CLImessageClient.askIfConfident(exMessage, self.option)
            if ask != False and toBeModified is not None:
                __messageDictionary = self.CentralMechanism.modifyMessage(__messageDictionary, toBeModified, newMessageId, comment, translation, self.option)
                if __messageDictionary is not None:
                    __message = self.CentralMechanism.dictionaryToText(__messageDictionary)
                    if language != "all":
                        __pathToCatalog = os.path.join(pathLanguages, language, "LC_MESSAGES")
                        __pathMessages = os.path.join(__pathToCatalog, poFile + ".po")
                        self.FileManager.writefile(__message, __pathMessages, verbose)
                        print("\"" + exMessage + "\" modified successfully on \""+ language +"\" file")
                        self.BabelManager.compile(__pathToCatalog, language, verbose)
                    else:
                        self.FileManager.writefile(__message, pathToPot, verbose)
                        if newMessageId is not "":
                            exMessage = newMessageId
                        print("\"" + exMessage + "\" modified successfully on .pot file")
                        for x in allLanguages:
                            __pathToCatalog = os.path.join(pathLanguages, x, "LC_MESSAGES")
                            updated = self.BabelManager.update(__pathToCatalog, pathToPot, x, verbose)
                            if updated is not None: 
                                self.BabelManager.compile(__pathToCatalog, x, verbose)
                
    def deleteMessageInCatalogs(self, args):
        language = "all"
        message = args.messageId.split("\"")[0]
        verbose = args.Verbose
        self.option = 3
        pathLanguages = self.pathLanguages
        pathToPot = self.pathToPot
        allLanguages = self.PathHandler.listLanguages(pathLanguages)
        __messageDictionary = self.CentralMechanism.getDictionary(language, self.pathLanguages, self.pathToPot)
        if __messageDictionary is not None:
            toBeDeleted = self.CentralMechanism.searchMessage(message, __messageDictionary, language, verbose)
            ask = args.force
            if toBeDeleted != None and ask == False:
                ask = self.CLImessageClient.askIfConfident(message, self.option)
            if ask != False:
                if toBeDeleted != None:
                    __messageDictionary = self.CentralMechanism.modifyMessage(__messageDictionary, toBeDeleted, "", "", "", self.option)
                    if __messageDictionary is not None:
                        __message = self.CentralMechanism.dictionaryToText(__messageDictionary)
                        self.FileManager.writefile(__message, pathToPot, verbose)
                        print("\"" + message + "\" deleted successfully")
                        for x in allLanguages:
                            __pathToCatalog = os.path.join(pathLanguages, x, "LC_MESSAGES")
                            updated = self.BabelManager.update(__pathToCatalog, pathToPot, x, verbose)
                            if updated is not None: 
                                self.BabelManager.compile(__pathToCatalog, x, verbose)

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
            print("\"" + language + "\" language deleted successfuly")

    def addTranslations(self,args):
        language = args.exLan
        translationPath = args.File
        verbose = args.Verbose
        if args.File is not None and args.Stdin:
            print("** Error, only one option between File and Stdin can be used. **")
            sys.exit()
        __lanDictionary = self.CentralMechanism.getDictionary(language, self.pathLanguages, self.pathToPot)
        if __lanDictionary is not None:
            if args.File is not None or args.Stdin:
                if args.File is not None:
                    try:
                        header = ["msgid", "msgstr"]
                        __translations = csv.DictReader(open(translationPath), fieldnames = header, delimiter = ";")
                    except Exception as e: 
                        print (str(e))
                        print("** \"" + translationPath + "\"doesn't lead to a valid translations file **")
                        print("")
                        return None
                    __translationsList = [[x["msgid"],x["msgstr"]] for x in __translations]
                elif args.Stdin:
                    __translations = sys.stdin.readlines()
                    __translationsList = []
                    for x in __translations:
                        try:
                            __translationsList.append([x[:x.index(";")],x[x.index(";")+1:]])
                        except:
                            print("** \"" + x + "\" not added")
                            print("** Error, for adding translations through StdIn, Messages Id's and Messages String's should be separated through a semi colon (\";\") **")
                notExistingList = []
                for x in __translationsList:
                    msgid = x[0].replace("\r", "")
                    try:
                        translation = x[1].replace("\r", "")
                    except:
                        translation = x[1]
                    if __lanDictionary[msgid]:
                        __lanDictionary[msgid]["msgstr"] = translation
                    else:
                        notExistingList.append(translation)
                if verbose:
                    if notExistingList != []:
                        print("The next list contains the elements that didn't exist on the selected language")
                        print(notExistingList)
                        print("")
                print("Elements that didn't exist in the selected language: " + str(len(notExistingList)))
                print("")
                messages = self.CentralMechanism.dictionaryToText(__lanDictionary)
                pathLanguages = self.pathLanguages
                __pathToCatalog = os.path.join(pathLanguages, language, "LC_MESSAGES")
                __pathMessages = os.path.join(__pathToCatalog, poFile + ".po")
                self.FileManager.writefile(messages, __pathMessages, verbose)
                compiled = self.BabelManager.compile(__pathToCatalog,language,verbose)
                if compiled is not None:
                    print("Translations added succesfully")
                    print("")
            else:
                print("** Error, no option for input selected, see \"aT --help\" for further reference **")
                print("")
    
    def extractCSV(self, args):
        language = args.exLan
        pathToFile = os.path.join(".", language + args.File)
        __lanDictionary = self.CentralMechanism.getDictionary(language, self.pathLanguages, self.pathToPot)
        if __lanDictionary is not None:
            __csvFormated = self.CentralMechanism.dictionaryToCSV(__lanDictionary, pathToFile)
            if __csvFormated is True:
                print(pathToFile + " created correctly")
                print("")
            else:
                print("Couldn't create cvs")
                print("")

class Runner(object):
    def __init__(self, basePath, pathToPot):
        self.pathLanguages = basePath
        self.PathHandler = PathHandler(basePath)
        self.Core = Core(self.pathLanguages, pathToPot)
        self.CLI(sys.argv)
    
    def CLI(self, args):
        languages = self.PathHandler.listLanguages(self.pathLanguages)
        languages.append("all")
        argsL = args

        if len(argsL) < 2:
            print("** No argument recieved, exiting. See --help if needed. **")
            print("")
        else:
            parser = argparse.ArgumentParser(prog=argsL[0], description="Options for management of .po catalogs")
            subparsers = parser.add_subparsers(metavar= "{command}", title="Available Commands", description="Each should be used with their respective sub-subcommands. Use \"" + argsL[0] + " {option} -h\" to see the individual use of each")

            parser_V = subparsers.add_parser("V", description="Verify the integrity of the catalogs against the .pot file" ,help = "Verify:  Allows to verify that every Language Catalog has the same Message Id's")
            parser_V.add_argument("-v","--Verbose", action='store_true', help = "Show all the messages that do not exist in the pot file")
            parser_V.set_defaults(func=self.Core.verifyCatalogs)

            parser_S = subparsers.add_parser("S",help = "Search:  Allows to search a message through a Message Id, result is either if exists and if a language is selected also shows its Comments and Translation")
            parser_S.add_argument("messageId", metavar="Message_Id")
            parser_S.add_argument("exLan", choices=languages, nargs='?',  default = "all",  metavar="Language", help="Language to search in, for all languages: all")
            parser_S.set_defaults(func=self.Core.searchMessageInCatalogs)

            parser_aL = subparsers.add_parser("aL",help = "Add Language:  Allows to add a new language with the Message Id's already added")
            parser_aL.add_argument("newLan", metavar="New_Language", help="Language to be added")
            parser_aL.add_argument("-v","--Verbose", action='store_true', help = "Show as much of the process")
            parser_aL.set_defaults(func=self.Core.addLanguageCatalog)

            parser_aM = subparsers.add_parser("aM",help = "Add Message:  Allows to add a message, either to one language or all")
            parser_aM.add_argument("messageId", metavar="New_Message_Id", help="The Message Id should go wrapped in quotation marks")
            parser_aM.add_argument("-C","--Comment", metavar="Message_Comment", help="The Message Comment should go wrapped in quotation marks")
            parser_aM.add_argument("-v","--Verbose", action='store_true', help = "Show as much of the process")
            parser_aM.set_defaults(func=self.Core.addMessageToCatalogs)

            parser_mM = subparsers.add_parser("mM",help = "Modify Message:  Allows to modify a Message Id, and if a language is selected then allow to modify Comment and/or Translation")
            parser_mM.add_argument("exMessageId", metavar="Message_Id", help="The Message Id should be wrapped wrapped in quotation marks and it's Caps Sensitive")
            group_mM = parser_mM.add_mutually_exclusive_group(required = True)
            group_mM.add_argument("-M", "--MessageId", metavar="New_Message_Id", help="The New message Id should be wrapped in quotation marks, only allowed to be used when applied to all languages")
            group_mM.add_argument("-T","--Translation", metavar="Message_Translation", help="The Message Translation should go wrapped in quotation marks, only allowed to be used when applied to only one language")
            parser_mM.add_argument("-C","--Comment", metavar="Message_Comment", help="The Message Comment should go wrapped in quotation marks, only allowed to be used when applied to a certain language")
            if (argsL[1] == "mM") and "-M" in argsL:
                parser_mM.add_argument("exLan", choices=["all"], nargs="?", default= "all", metavar="Language", help= "Language in which the change will be made")
            elif argsL[1] == "mM":
                languages.pop()
                parser_mM.add_argument("exLan", choices=languages, metavar="Language", help= "Language in which the change will be made in, in case the change is the Message Id only \"all\" is permited")
            parser_mM.add_argument("-f","--force", action='store_true', help = "Force the action, no questions asked")
            parser_mM.add_argument("-v","--Verbose", action='store_true', help = "Show as much of the process")
            parser_mM.set_defaults(func=self.Core.modifyMessageInCatalog)

            parser_dM = subparsers.add_parser("dM",help = "Delete Message:  Allow to delete a Message Id in all catalogs or if language provided only in said language")
            parser_dM.add_argument("messageId", metavar="Message_Id", help = "Message Id to be deleted")
            parser_dM.add_argument("-f","--force", action='store_true', help = "Force the action, no questions asked")
            parser_dM.add_argument("-v","--Verbose", action='store_true', help = "Show as much of the process")
            parser_dM.set_defaults(func=self.Core.deleteMessageInCatalogs)

            parser_dL = subparsers.add_parser("dL", help = "Delete Catalog:  Allows to delete a whole Language's Message Catalog")
            parser_dL.add_argument("exLan", choices=languages, metavar="Language", help= "Language to delete its Catalog")
            parser_dL.add_argument("-f","--force", action='store_true', help = "Force the action, no questions asked")
            parser_dL.add_argument("-v","--Verbose", action='store_true', help = "Show as much of the process")
            parser_dL.set_defaults(func=self.Core.deleteLanguageCatalog)

            parser_aT = subparsers.add_parser("aT",help = "Add Translations:  Allows to allow a massive catalog of translations to an initiated Catalog")
            if argsL[1] is "aT":
                languages.pop()
            parser_aT.add_argument("exLan", choices=languages, metavar="Language", help= "Language to add Translations to its Catalog")
            group_aT = parser_aT.add_mutually_exclusive_group(required=True)
            group_aT.add_argument("-F","--File", help = "Expect a file path")
            group_aT.add_argument("-S","--Stdin", action='store_true', help = "Expect a Standard Input before")
            parser_aT.add_argument("-v","--Verbose", action='store_true', help = "Show the whole list of messages not updated and not used")
            parser_aT.set_defaults(func=self.Core.addTranslations)

            parser_xCSV = subparsers.add_parser("xCSV", help = "")
            parser_xCSV.add_argument("exLan", choices=languages, metavar="Language", help= "Language to add Translations to its Catalog")
            parser_xCSV.add_argument("-F","--File", nargs='?',  default = "translations.csv", help = "Path for csv creation, default is: \"" + os.path.join(".","\"language\"translations.csv") + "\"")
            parser_xCSV.set_defaults(func=self.Core.extractCSV)

            del argsL[0]
            print("")
            arguments = parser.parse_args(argsL)
            arguments.func(arguments)
            print("")      
            
if __name__ == "__main__":
    Runner(basePath, pathToPot)