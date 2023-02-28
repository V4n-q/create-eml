# createEML

Python Script to create an EML(Electronic Mail) file with an email message and attachments.

**This script is written for just testing of other EML scripts, so its just a "Test Suite" for now.**

# Requirements

All of the imported modules are preinstalled.

# Usage

- `py main.py "SenderEmail" "ReceiverEmail" "Subject"`

  Enter Message Body and Choose if you wanna attach any files or not when prompted.

<center>Or,</center>

- `py main.py`

  Enter Sender Email, Receiver Email, Subject & Message Body in order when prompted.
  And Choose if you wanna attach any files or not.

## Attachment Type:

1) Single Mode
   Choose `1` for Single File, and provide the file path.
   Should Support any type of file.
   
   Example: `D:\Files\TestDoc.pdf`
   
2) Multi Mode
   Choose `2` For Multiple Files, and provide the folder path where all the files are located.
   Will work for sub directories too.
   
   Example: `D:\Files\`
