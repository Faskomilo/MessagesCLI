import os

class CLImessageClient:
    pathLanguages = os.path.join("languages")
    option = ""

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
        line = messageList[0]
        messageMatrix[0][0] = line[:line.index("\nmsgid")]
        messageMatrix[0][1] = line[line.index("ms"):line.index("\nmsgstr")]
        messageMatrix[0][2] = line[line.index("msgstr"):]
        return messageMatrix

    def message (self):
        
        return 0
        
        


run = CLImessageClient()
print(run.toList(run.readfile("es")))