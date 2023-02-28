import email.message
import os
import sys
import re
import logging

# get valid email addresses using regex
def getValidEmailAddress(prompt):
    """
    This function takes an email address prompt as input and returns a valid email address. 
    It uses a regex to check whether the email address is in a valid format or not.
    """

    emailRegex = r"[^@]+@[^@]+\.[^@]+"
    while True:
        emailAddress = input(prompt)
        if re.match(emailRegex, emailAddress):
            return emailAddress
        print("Invalid email address format. Please enter a valid email address")

# add attachemnt to email message
def addAttachment(msg):
    """
    This function takes an email message as input and adds attachments to it.
    It prompts the user to choose whether they want to attach a single file or multiple files.
    It then asks for the file/folder path and iterates through each file in the folder to add it as an attachment.
    If there are any errors (e.g. file not found, permission denied), it logs the error and continues with the next file.
    """
    # configure logging settings
    logging.basicConfig(filename="attachment.log",level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')
    # attachment mode
    print("1.Single File\n2.Multiple File")
    attachMode = int(input("Choose 1 or 2: "))
    # validating user input
    while(attachMode not in (1,2)):
        attachMode = input("Invalid input. Choose 1 or 2: ")
    # Single File Mode
    if attachMode == 1:
        filePath = input("File Path: ").strip('"')
        print("\n")
        while(os.path.isfile(filePath) == False):
            filePath = input("A directory path was provided instead of a file path. Please enter File Path: ").strip('"')
        try:
            # open file in binary mode
            with open(filePath, 'rb') as f:
                fileData = f.read()
                fileName= os.path.basename(filePath)
                fileExtension= os.path.splitext(fileName)[1]
            # add file data as attachment to message
            msg.add_attachment(fileData,maintype='application',subtype=fileExtension,filename=fileName)
        except (FileNotFoundError, PermissionError) as e:
            # log error and print error message
            logging.error(f"Error: {str(e)} - {fileName}")
            print(f"Error: {fileName} not found or permission denied.")
    # Multiple File Mode
    elif attachMode == 2:
        successFileCount = 0
        failureFileCount = 0
        folderPath = input("\nFolder Path: ").strip('"')
        try:
            # traverse directory structure recursively
            for root,dirs,files in os.walk(folderPath):
                #iterate over the files in current directory
                for fileName in files:
                    #construct file path
                    filePath = os.path.join(root,fileName)
                    try:
                        with open(filePath, 'rb') as f:
                            fileData = f.read()
                            fileExtension= os.path.splitext(fileName)[1]
                        msg.add_attachment(fileData,maintype='application',subtype=fileExtension,filename=fileName)
                        successFileCount+=1
                    except PermissionError:
                        logging.error(f"Error: Permission denied {filePath}")
                        print(f"File {fileName} not attached due to permission error.")
                        failureFileCount += 1
                    except FileNotFoundError as e:
                        logging.error(f"{filePath} not found, {fileName}")
                        print(f"File Not Found.")
                        failureFileCount += 1
                    except Exception as e:
                        logging.error(f"Error: {str(e)} - {fileName}")
                        print("Error occured.Please check log.")
                        failureFileCount += 1
        except Exception as e:
            logging.error(f"Error: {str(e)} - {fileName}")
            print("Error occured.Please check log.")
        if successFileCount > 0:
            print(f"{successFileCount} files attached successfully.")
        if failureFileCount > 0:
            print(f"{failureFileCount} files failed to attach.")
    else:
        print("Invalid Input. Please enter '1' or '2'.")

if __name__=="__main__":
    attachmentConfirmation = ["y","n","yes","no"]
    attachmentPositiveConfirm= ["y","yes"]
    
    print("\n\tEML Creation\n")

    if len(sys.argv) > 1:
        sender=sys.argv[1]
        receiver = sys.argv[2]
        subject = sys.argv[3]
    else:
        sender = getValidEmailAddress("From: ")
        receiver = getValidEmailAddress("To: ")
        subject = input("Subject: ")

    #creating empty message
    msg = email.message.EmailMessage()

    #setting message header
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    #setting message body
    msgBody=input("Message Body: ")
    msg.set_content(msgBody)

    #attachment prompt
    attachFile= input("\nAttach File To Email? (y/n): ").lower()
    while attachFile not in attachmentConfirmation:
        attachFile = input("Invalid input. Attach File To Email? (y/n): ").lower()
    if(attachFile in attachmentPositiveConfirm):
        addAttachment(msg)
            
    #EML File Creation
    emlFileName=input("\nEnter the EML File Name: ")
    fullEmlFileName = emlFileName + ".eml"
    try:
        with open(fullEmlFileName, 'w') as f:
            f.write(str(msg))
            print(f"'{emlFileName}' has been saved as '{fullEmlFileName}'.")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"An error occurred while saving '{emlFileName}' as '{fullEmlFileName}' : {str(e)}")