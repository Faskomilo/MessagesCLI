import os

class CLImessageClient(object):
    pathLanguages = os.path.join("languages")
    option = ""

    def __init__(self, ):
        print("")

    def readfile(self, language):
        path = os.path.join("languages", language, "LC_MESSAGES", "messages.po")
        messages = open(path).read()
        return messages

    def languages(self):
        options = os.listdir(os.path.join(".", self.pathLanguages)) 
        return options

    def choose(self):
        print "Escoja una opcion:"
        print "1"

    def toList(self, message):
        messageList = message.split("\n\n")
        messageMatrix = [[0 for x in range(3)] for y in range(len(messageList))]
        a = 0
        for x in range(len(messageList)):
            line = ""
            try:
                if x == 0:
                    line = messageList[x]
                    messageMatrix[0][0] = line[:line.index("\nmsgid")]
                    messageMatrix[0][1] = line[line.index("ms"):line.index("\nmsgstr")]
                    messageMatrix[0][2] = line[line.index("msgstr"):]
                else: 
                    line = messageList[x]
                    messageMatrix[x][0] = line[:line.index("\nmsgid")]
                    messageMatrix[x][1] = line[line.index("msgid"):line.index("\nmsgstr")]
                    messageMatrix[x][2] = line[line.index("msgstr"):]
            except Exception:
                print(a)
                print(line)
            a = a +1 
        return messageMatrix

    def message (self):
        
        return 0
        
        


run = CLImessageClient()
run.toList(run.readfile("es"))
#print(run.toList(run.readfile("es")))