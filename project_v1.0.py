import email.parser
from email.parser import Parser
from os import listdir
from os.path import isfile, join
from csv import DictReader, DictWriter


# Code to extract a particular section from raw emails.

class Email:
    def __init__(self, msg):

        # Get the separate parts from the email
        self.Head_To = msg.__getitem__("To")
        self.Head_From = msg.__getitem__("From")
        self.Head_Date = msg.__getitem__("Date")
        self.Head_Subject = msg.__getitem__("Subject")
        self.Head_Content_Type = msg.__getitem__("Content-Type")
        self.Head_X_From = msg.__getitem__("X-From")
        self.Head_X_To = msg.__getitem__("X-To")
        self.Head_X_From = msg.__getitem__("X-From")
        self.Head_X_Cc = msg.__getitem__("X-cc")
        self.Head_X_Bcc = msg.__getitem__("X-bcc")
        self.Head_X_Folder = msg.__getitem__("X-Folder")
        self.Head_X_Origin = msg.__getitem__("X-Origin")
        self.Head_X_Filename = msg.__getitem__("X-Filename")
        self.Body = msg.get_payload()
        # if msg.is_multipart():
        #     for payload in msg.get_payload():
        #         print payload.get_payload()
        #         print "***************************here****************************"
        # else:
        #     print msg.get_payload()

        # Print the part

    def printAll(self):
        parts = vars(self)
        for p in parts.items():
            print p



if __name__ == "__main__":
    parser = Parser()
    # text1 = open("./allen-p", "r").read()
    # msg = email.message_from_string(text1)
    # e = Email(msg)
    # e.printAll()
    # email = parser.parsestr(text1)

    users = [f for f in listdir("./data") if not isfile(join("./data", f))]
    directories = [f for f in listdir("./allen-p") if not isfile(join("./allen-p", f))]
    print directories
    allfiles = dict()
    for directory in directories:
        directoryPath = "./allen-p/" + directory
        files = [f for f in listdir(directoryPath) if isfile(join(directoryPath, f))]
        allfiles[directory] = files
    print allfiles

    o = DictWriter(open("EmailData.csv", 'w'), ["Head_To", "Head_From", "Head_Date"])
    o.writeheader()

    for key in allfiles.keys():
        values = allfiles[key]
        for file in values:
            emailObject = open("./allen-p/"+key+"/"+file, "r").read()
            msg = email.message_from_string(emailObject)
            e = Email(msg)
            # e.printAll()
            d = {'Head_To': e.Head_To, 'Head_From': e.Head_From, 'Head_Date': e.Head_Date}
            o.writerow(d)
