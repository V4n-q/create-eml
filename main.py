import email.message
import os
import sys
import re
import logging

# get valid email addresses using regex
def get_valid_email_address(prompt):
    """
    This function takes an email address prompt as input and returns a valid email address. 
    It uses a regex to check whether the email address is in a valid format or not.
    """

    email_regex = r"[^@]+@[^@]+\.[^@]+"
    while True:
        email_address = input(prompt)
        if re.match(email_regex, email_address):
            return email_address
        print("Invalid email address format. Please enter a valid email address")

# add attachemnt to email message
def add_attachment(msg):
    """
    This function takes an email message as input and adds attachments to it.
    It prompts the user to choose whether they want to attach a single file or multiple files.
    It then asks for the file/folder path and iterates through each file in the folder to add it as an attachment.
    If there are any errors (e.g. file not found, permission denied), it logs the error and continues with the next file.
    """
    # attachment mode
    print("1.Single File\n2.Multiple File")
    while True:
        try:
            attach_mode = int(input("Choose 1 or 2: "))
            # validating user input
            if attach_mode in (1,2):
                break
        except ValueError:
            pass
        print("Invalid Input.")
    # Single File Mode
    if attach_mode == 1:
        file_path = input("File Path: ").strip('"')
        print("\n")
        while(os.path.isfile(file_path) == False):
            file_path = input("A directory path was provided instead of a file path. Please enter File Path: ").strip('"')
        try:
            # open file in binary mode
            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_name= os.path.basename(file_path)
                # Gets File extension and removes dot from the extension
                file_extension= os.path.splitext(file_name)[1].strip(".")
            # add file data as attachment to message
            msg.add_attachment(file_data,maintype='application',subtype=file_extension,filename=file_name)
        except (FileNotFoundError, PermissionError) as e:
            # log error and print error message
            logging.error(f"Error: {str(e)} - {file_name}")
            print(f"Error: {file_name} not found or permission denied.")
    # Multiple File Mode
    elif attach_mode == 2:
        success_file_count = 0
        failure_file_count = 0
        folderPath = input("\nFolder Path: ").strip('"')
        try:
            # traverse directory structure recursively
            for root,dirs,files in os.walk(folderPath):
                #iterate over the files in current directory
                for file_name in files:
                    #construct file path
                    file_path = os.path.join(root,file_name)
                    try:
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                            file_extension= os.path.splitext(file_name)[1]
                        msg.add_attachment(file_data,maintype='application',subtype=file_extension,filename=file_name)
                        success_file_count+=1
                    except PermissionError:
                        logging.error(f"Error: Permission denied {file_path}")
                        print(f"File {file_name} not attached due to permission error.")
                        failure_file_count += 1
                    except FileNotFoundError as e:
                        logging.error(f"{file_path} not found, {file_name}")
                        print(f"File Not Found.")
                        failure_file_count += 1
                    except Exception as e:
                        logging.error(f"Error: {str(e)} - {file_name}")
                        print("Error occured.Please check log.")
                        failure_file_count += 1
        except Exception as e:
            logging.error(f"Error: {str(e)} - {file_name}")
            print("Error occured.Please check log.")
        if success_file_count > 0:
            print(f"{success_file_count} files attached successfully.")
        if failure_file_count > 0:
            print(f"{failure_file_count} files failed to attach.")
    else:
        print("Invalid Input. Please enter '1' or '2'.")

if __name__=="__main__":
    # configure logging settings
    logging.basicConfig(file_name="attachment.log",level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')
    
    attachment_confirmation = ["y","n","yes","no"]
    attachment_positive_confirm= ["y","yes"]
    
    print("\n\tEML Creation\n")

    if len(sys.argv) > 1:
        sender=sys.argv[1]
        receiver = sys.argv[2]
        subject = sys.argv[3]
    else:
        sender = get_valid_email_address("From: ")
        receiver = get_valid_email_address("To: ")
        subject = input("Subject: ")

    #creating empty message
    msg = email.message.EmailMessage()

    #setting message header
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    #setting message body
    msg_body=input("Message Body: ")
    msg.set_content(msg_body)

    #attachment prompt
    attach_file= input("\nAttach File To Email? (y/n): ").lower()
    while attach_file not in attachment_confirmation:
        attach_file = input("Invalid input. Attach File To Email? (y/n): ").lower()
    if(attach_file in attachment_positive_confirm):
        add_attachment(msg)
            
    #EML File Creation
    eml_file_name=input("\nEnter the EML File Name: ")
    full_eml_file_name = eml_file_name + ".eml"
    try:
        with open(full_eml_file_name, 'w') as f:
            f.write(str(msg))
            print(f"'{eml_file_name}' has been saved as '{full_eml_file_name}'.")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"An error occurred while saving '{eml_file_name}' as '{full_eml_file_name}' : {str(e)}")