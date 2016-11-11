import email.parser
from email.parser import Parser
from os import listdir
from os.path import isfile, join
from csv import DictReader, DictWriter
import copy


# Code to extract a particular section from raw emails.

class Email:
    def __init__(self, msg):
        # Get separate parts from the email
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
    allfiles = dict(dict())

    # Get all the users
    users = [f for f in listdir("./data") if not isfile(join("./data", f))]
    temp = dict()
    total = 0

    # Get all the files into a dictionary
    for user in users:
        userDirectories = [f for f in listdir("./data/" + user) if not isfile(join("./data/" + user, f))]
        for folder in userDirectories:
            folderPath = "./data/" + user + "/" + folder
            files = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
            temp[folder] = files
            total += len(files)
        allfiles[user] = copy.deepcopy(temp)
        print "Total folders in %s; " % user, len(allfiles[user])
        temp.clear()
    print "Dictionary of data: ", allfiles
    print "Total files in all folders: ", total

    # Create a dictionary writer
    o = DictWriter(open("EmailData.csv", 'w'), ["Head_To", "Head_From", "Head_Date"])
    o.writeheader()

    # Write all the separated features of the email into a CSV file
    for user in allfiles.keys():
        userFolders = allfiles[user]
        for folder in userFolders:
            files = allfiles[user][folder]
            for file in files:
                emailObject = open("./data/" + user + "/" + folder + "/" + file, "r").read()
                msg = email.message_from_string(emailObject)
                e = Email(msg)
                # e.printAll()
                d = {'Head_To': e.Head_To, 'Head_From': e.Head_From, 'Head_Date': e.Head_Date}
                o.writerow(d)
