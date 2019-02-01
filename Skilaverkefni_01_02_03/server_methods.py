from pathlib import Path

# Short function to initialize the files we use in this project
def InitFiles():
    path = Path("archive")
    filenames = ["file1.txt", "file2.txt", "file3.txt"]
    for x in range(0,3):
        tmpPath = path / filenames[x]
        if not tmpPath.is_file():
            if x == 0:
                textToWrite = "This is file1.\n\nHere is some additional flavor text.\nFile 1."
            elif x == 1:
                textToWrite = "This is file2.\n\nHere is some additional flavor text.\nFile 2."
            elif x == 2:
                textToWrite = "This is file3.\n\nHere is some additional flavor text.\nFile 3."
            else:
                textToWrite = "Something went wrong cap'n!"
            with open(tmpPath, "w") as file:
                file.write(textToWrite)

def CheckExtension(file):
    # Checking the file extension
    if file.lower()[-4:] != ".txt":
        file += ".txt"
        print("User selected to receive: " + file)

    return Path("archive") / file

# A function we use to parse some information from the client
# And then to send a file back (only works for txt files at the moment)
def SendFile(answer):
    # The file we receive from the client looks like this "answer:[filename]"
    # so we split the string and choose only the second half which contains the filename
    _answer = answer.split(":")[1]

    tmpPath = CheckExtension(_answer)

    with open(tmpPath, "rb") as file:
        # Send the file to the client
        return bytes("filename:" + _answer + ";content:", "utf8") + file.read()

def ModifyFile(answer):
    _answer = answer.split(":")[1]

    tmpPath = CheckExtension(_answer)

    try:
        open(tmpPath, )