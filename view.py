#!/usr/bin/python3
import os, sys, curses
from datetime import datetime

def createStreamList():
    streamList = []
    streamListFile = open("messages/streamList", "r")
    for line in streamListFile:
        streamList.append(line.strip())
    streamListFile.close()
    return streamList

def createPermissionList(username, streamList):
    userPermissionStreamList = []

    flag = 0
    for word in streamList:

        userFileName = "messages/" + word + "UserStream"
        userListFile = open(userFileName, "r")
        for line in userListFile:
            if username.strip() == line.strip(" \n0123456789"):
                flag = 1
                userPermissionStreamList.append(word)
    if flag == 0:
        print ("User has no permissions...")
        print ("here1")
        return userPermissionStreamList
    print ("here2")
    return userPermissionStreamList

def getReadMessages(username, outFileUserName):
    fPtr = open(outFileUserName, "r")
    for line in fPtr:
        if line.strip(" \n0123456789") == username.strip():
            for s in line.split():
                if s.isdigit():
                    fPtr.close()
                    return s
    return 0

def getToPrint(readList, unreadList, streamname, username):
    outFileStreamName = "messages/" + streamname + "Stream"
    outFileDataName = "messages/" + streamname + "StreamData"
    outFileUserName = "messages/" + streamname + "UserStream"
    i = getReadMessages(username, outFileUserName)
    offset = 0;
    if int(i) != 0:
        fPtr = open(outFileDataName, "r")
        count = 1
        for line in fPtr:
            if int(i) == int(count):
                offset = int(line)
                break;
            count = count + 1
        fPtr.close()
    fPtr = open(outFileStreamName, "r")
    count = 0
    for line in fPtr:
        if count < offset:
            if "Sender:" in line:
                readList.append("Stream: " + streamname + "\n")
            readList.append(line)
        else:
            if "Sender:" in line:
                unreadList.append("Stream: " + streamname + "\n")
            unreadList.append(line)
        for char in line:
            count = count + 1

    fPtr.close()
    return readList, unreadList

def sortByDate(myList):
    dateList = []
    tempList = []
    for item in myList:
        if "Stream:" in item:
            if tempList:
                copyList = tempList[:]
                dateList.append(copyList)
                tempList[:] = []
        tempList.append(item)
    if tempList:
        copyList = tempList[:]
        dateList.append(copyList)
    dateList.sort(key=lambda date: datetime.strptime(date[2], "Date: %b. %d, %Y, %I : %M %p\n"))
    finalList = []
    for l in dateList:
        for item in l:
            finalList.append(item)
    return finalList

def sortByAuthor(readList, unreadList):
    combinedList = readList + unreadList
    authorList = []
    tempList = []
    for item in combinedList:
        if "Stream:" in item:
            if tempList:
                copyList = tempList[:]
                authorList.append(copyList)
                tempList[:] = []
        tempList.append(item)
    if tempList:
        copyList = tempList[:]
        authorList.append(copyList)

    authorList.sort(key=lambda x: x[1])
    finalList = []
    for l in authorList:
        for item in l:
            finalList.append(item)
    return finalList

def printToWindow(window, readList, unreadList, currentLineNumber):
    window.clear()
    allList = readList + unreadList
    count = 0
    currentLines = 0
    for line in allList:
        if(count < int(currentLineNumber)):
            count = count + 1
            continue
        if currentLines < 23 :
            window.addstr(line)
            currentLines = currentLines + 1
            count = count + 1

def getLastLine(readList, unreadList):
    allList = unreadList + readList
    count = 0
    for line in allList:
        count = count + 1
    return count

def markAllRead(username, streamname):
    outFileDataName = "messages/" + streamname + "StreamData"
    outFileUserName = "messages/" + streamname + "UserStream"
    fp = open(outFileDataName, "r")
    count = 0
    for line in fp:
        count = count + 1
    fp.close()
    fp = open(outFileUserName, "r")
    fpcopy = open("copy", "w")
    for line in fp:
        if line.strip(" \n0123456789") == username:
            fpcopy.write(username + " " + str(count) + "\n")
        else:
            fpcopy.write(line)
    fpcopy.close
    os.rename("copy", outFileUserName)

def updateReadMessages(streamname, username, currentLineNumber, unreadList, readList):
    outFileDataName = "messages/" + streamname + "StreamData"
    outFileUserName = "messages/" + streamname + "UserStream"
    outFileStreamName = "messages/" + streamname + "Stream"
    j = 0
    read = 0
    postStream = "DEFAULT"
    allList = readList + unreadList
    for item in allList:
        if "Stream:" in item:
            postStream = item[8:].strip()
        if "Date: " in item:
            if postStream == streamname:
                read = read + 1
        j = j + 1
        x = currentLineNumber + 23
        if j >= x:
            break
    infileRead = int(getReadMessages(username, outFileUserName))
    if read < int(infileRead):
        read = int(infileRead)
    #writing to output file
    fpUser = open(outFileUserName, "r+")
    fpcopy = open("copy", "w")
    for line in fpUser:
        if username == line.strip(" \n0123456789"):
            fpcopy.write(username + " " + str(read) + "\n")
        else:
            fpcopy.write(line)
    fpUser.close()
    fpcopy.close()
    os.rename("copy", outFileUserName)

def getLastItem(myList):
    count = 0
    for item in myList:
        count = count + 1
    return count

def printButtons(username, inputFlag, readNum):
    print("<form action=\"processChangeMsg.php\" method=\"post\">")
    print("\n\t<input type=\"hidden\" name=\"username\" value=\""+ username.strip() +"\">\n")
    print("\n\t<input type=\"hidden\" name=\"streamChoice\" value=\""+ inputFlag + "\">\n")
    print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\""+ str(readNum-1) +"\">\n")
    print("\t<input type=\"submit\" value=\"Prev Post\">\n</form>\n")

    print("<form action=\"processChangeMsg.php\" method=\"post\">")
    print("\n\t<input type=\"hidden\" name=\"username\" value=\""+ username.strip() +"\">\n")
    print("\n\t<input type=\"hidden\" name=\"streamChoice\" value=\""+ inputFlag + "\">\n")
    print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\""+ str(readNum+1) +"\">\n")
    print("\t<input type=\"submit\" value=\"Next Post\">\n</form>\n")

    print("<form action=\"processChangeMsg.php\" method=\"post\">")
    print("\n\t<input type=\"hidden\" name=\"username\" value=\""+ username.strip() +"\">\n")
    print("\n\t<input type=\"hidden\" name=\"streamChoice\" value=\""+ inputFlag + "\">\n")
    print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\"-1\">\n")
    print("\t<input type=\"submit\" value=\"Mark all Read\">\n</form>\n")

    print("<form action=\"processChangeMsg.php\" method=\"post\">")
    print("\n\t<input type=\"hidden\" name=\"username\" value=\""+ username.strip() +"\">\n")
    print("\n\t<input type=\"hidden\" name=\"streamChoice\" value=\""+ inputFlag + "\">\n")
    print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\"-1\">\n")
    print("\t<input type=\"submit\" value=\"Sorting\">\n</form>\n")

    print("<form action=\"processChangeMsg.php\" method=\"post\">")
    print("\n\t<input type=\"hidden\" name=\"username\" value=\""+ username.strip() +"\">\n")
    print("\n\t<input type=\"hidden\" name=\"streamChoice\" value=\""+ inputFlag + "\">\n")
    print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\"-1\">\n")
    print("\t<input type=\"submit\" value=\"Check for New\">\n</form>\n")

def main():
    #checking for valid username, and placing it into variable

    streamname = ""
    username = ""
    readNum = 0
    if sys.argv[1] != "STREAM_NAME:":

        for word in sys.argv:
            if word != "./view.py":
                username = username + " " + word
        username = username.lstrip()
        # creating list of all streams
        streamList = createStreamList()

        # checking each user file for a list of streams they are associated with
        userPermissionStreamList = createPermissionList(username, streamList)
        print ("<form action=\"home.php\" method=\"post\">\n")
        print ("\t<input type=\"hidden\" name=\"username\" value=\""+ username +"\">\n")
        i = 0
        for word in userPermissionStreamList:
            print (word +"<input type=\"radio\" name=\"streamChoice\"")
            print (" value =\"" + word + "\"")
            if i == 0:
                print ("checked>")
            else:
                print (">")
            i = i + 1
        print ("all<input type=\"radio\" name=\"streamChoice\" value =\"all\"")
        if i == 0:
            print ("checked>")
        else:
            print (">")
        print ("\t<input type=\"submit\" value=\"submit\">\n</form>\n")
        return()
    streamname = sys.argv[2]
    readNum = int(sys.argv[3])
    i = 0
    for word in sys.argv:
        if i > 3:
            username = username +" "+ word
        i = i + 1
    # creating list of all streams
    streamList = createStreamList()
    # checking each user file for a list of streams they are associated with
    userPermissionStreamList = createPermissionList(username, streamList)

    # check which stream they would like to view
    inputFlag = streamname.strip()

    unreadList = []
    readList = []
    mode = "chrono"
    printButtons(username, inputFlag, readNum)
    print("<br><br><p>")
    if inputFlag != "all":
        readList, unReadList = getToPrint(readList, unreadList, inputFlag, username)
        if readNum == -1:
            readNum = 0;
            for line in readList:
                if "Stream:" in line:
                    readNum = readNum + 1
        allList = readList + unreadList;
        msg = -1

        for item in allList:
            if "Stream:" in item:
                msg = msg + 1
            if msg == readNum:
                print(item + "<br>")
                if "Date:" in item:
                    print("---------------------------------------<br>")
    else:
        for item in userPermissionStreamList:
            readList, unReadList = getToPrint(readList, unreadList, item, username)
        if readNum == -1:
            readNum = 0;
            for line in readList:
                if "Stream:" in line:
                    readNum = readNum + 1
        allList = readList + unreadList;
        msg = -1
        for item in allList:
            if "Stream:" in item:
                msg = msg + 1
            if msg == readNum:
                print(item + "<br>")
                if "Date:" in item:
                    print("---------------------------------------<br>")
    print("</p>")
    return()
#############################################################################################
    if inputFlag == "all" and updateListFlag == 1:
        unreadList = []
        readList = []
        for stream in userPermissionStreamList:
            readList, unReadList = getToPrint(readList, unreadList, stream, username)
        currentLineNumber = getLastItem(readList)
        if mode == "author":
            readList = sortByAuthor(readList, unreadList)
            currentLineNumber = 0
        else:
            readList = sortByDate(readList)
            unreadList = sortByDate(unreadList)
        if not unreadList:
            currentLineNumber = 0
        updateListFlag = 0
        needToPrint = 1
    elif updateListFlag == 1:
        unreadList = []
        readList = []
        readList, unReadList = getToPrint(readList, unreadList, inputFlag, username)
        currentLineNumber = getLastItem(readList)
        if mode == "author":
            readList = sortByAuthor(readList, unreadList)
            currentLineNumber = 0
        else:
            readList = sortByDate(readList)
            unreadList = sortByDate(unreadList)
        if not unreadList:
            currentLineNumber = 0
        updateListFlag = 0
        needToPrint = 1

    #add update read messages
    if inputFlag == "all" and mode == "chrono":
        for stream in userPermissionStreamList:
            updateReadMessages(stream, username, currentLineNumber, unreadList, readList)
    elif mode == "chrono":
        updateReadMessages(inputFlag, username, currentLineNumber, unreadList, readList)

    # determines if it needs to print if a certain action is taken
    if needToPrint == 1:
        printToWindow(window, readList, unreadList, currentLineNumber)
        window.addstr(23, 0, "Page Up   Page Down   O-order toggle   M-mark all   S-stream   C-check for new")
    needToPrint = 0

    c = window.getch()
    if c == 65:
        currentLineNumber = currentLineNumber - 23;
        if currentLineNumber < 0:
            currentLineNumber = 0
        needToPrint = 1
    elif c == 66:
        currentLineNumber = currentLineNumber + 23;
        maxline = getLastLine(readList, unreadList)
        if currentLineNumber >= int(maxline):
            currentLineNumber = currentLineNumber - 23
        needToPrint = 1
    elif c == ord('o') or c == ord('O'):
        if mode == "author":
            mode = "chrono"
        else:
            mode = "author"
        updateListFlag = 1
    elif c == ord('m') or c == ord('M'):
        if inputFlag == "all":
            for stream in userPermissionStreamList:
                markAllRead(username, stream)
        else:
            markAllRead(username, inputFlag)
        updateListFlag = 1
    elif c == ord('s') or c == ord('S'):
        updateListFlag = 1
        curses.echo()
        curses.endwin()
        for word in userPermissionStreamList:
            print (word.strip(), end=' ')
        print ("all")
        inputFlag = getStreamChoice(userPermissionStreamList)
        window = curses.initscr()
        curses.noecho()
        window = curses.newwin(24, 80, 0, 0)
    elif c == ord('c') or c == ord('C'):
        updateListFlag = 1

if __name__ == "__main__":
    main()
