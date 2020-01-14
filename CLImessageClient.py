import os
from babel.messages.catalog import Catalog
from babel.messages.extract import DEFAULT_KEYWORDS, DEFAULT_MAPPING, check_and_call_extract_file, extract_from_dir
#from babel.messages.mofile import write_mo, read_mo
from babel.messages.pofile import read_po, write_po

class CLImessageClient:
    pathLanguages = os.path.join("languages")
    option = ""

    def readfile(self, language):
        path = os.path.join("languages", language, "LC_MESSAGES", "messages.po")
        messages = read_po(open(path),language)
        return messages._messages

    def languages(self):
        options = os.listdir(os.path.join(".", self.pathLanguages)) 
        return options

    def choose(self):
        print "Escoja una opcion:"
        print "1"

    #def message (self):
    #    a = "Loading Image"
    #    s = ugettext(a)
    #    return s
        
        


run = CLImessageClient()
print(run.readfile("es"))