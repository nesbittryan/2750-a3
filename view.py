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
        return userPermissionStreamList
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

def updateReadMessages(streamname, username, readNum, limit):
    if readNum == -1:
        return
    outFileUserName = "messages/" + streamname.strip() + "UserStream"
    read = int(readNum) + 1
    infileRead = int(getReadMessages(username, outFileUserName))
    if read < int(infileRead):
        read = int(infileRead)
    if read > limit:
        return()
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

def printButtons(username, inputFlag, readNum, limit):

    print("<form action=\"processChangeMsg.php\" method=\"post\">")
    print("\n\t<input type=\"hidden\" name=\"username\" value=\""+ username.strip() +"\">\n")
    print("\n\t<input type=\"hidden\" name=\"streamChoice\" value=\""+ inputFlag + "\">\n")
    if readNum > 0:
        print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\""+ str(readNum-1) +"\">\n")
    else:
        print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\""+ str(readNum) +"\">\n")
    print("\t<input type=\"submit\" value=\"Prev Post\">\n</form>\n")

    print("<form action=\"processChangeMsg.php\" method=\"post\">")
    print("\n\t<input type=\"hidden\" name=\"username\" value=\""+ username.strip() +"\">\n")
    print("\n\t<input type=\"hidden\" name=\"streamChoice\" value=\""+ inputFlag + "\">\n")
    if int(readNum) < (int(limit) - 1):
        if int(readNum) == -1:
            print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\""+ str(readNum+2) +"\">\n")
        else:
            print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\""+ str(readNum+1) +"\">\n")
    else:
        print("\n\t<input type=\"hidden\" name=\"messageNum\" value=\""+ str(readNum) +"\">\n")
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

def getLimit(inputFlag, userStreamList):
    limit = 0
    if inputFlag == "all":
        for item in userStreamList:
            outFileDataName = "messages/" + item + "StreamData"
            fp = open(outFileDataName, "r")
            for line in fp:
                limit = limit + 1

    else:
        outFileDataName = "messages/" + inputFlag + "StreamData"
        fp = open(outFileDataName, "r")
        for line in fp:
            limit = limit + 1
    return limit

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

    username = username.strip()

    # creating list of all streams
    streamList = createStreamList()
    # checking each user file for a list of streams they are associated with
    userPermissionStreamList = createPermissionList(username, streamList)
    # check which stream they would like to view
    inputFlag = streamname.strip()
    unreadList = []
    readList = []
    mode = "chrono"
    limit = 0
    limit = getLimit(inputFlag, userPermissionStreamList) + limit;

    if inputFlag != "all":
        readList, unReadList = getToPrint(readList, unreadList, inputFlag, username)
        if readNum == -1:
            readNum = 0;
            for line in readList:
                if "Stream:" in line:
                    readNum = readNum + 1
        allList = readList + unreadList;
        msg = -1
        updateReadMessages(inputFlag, username, readNum, limit)
        printButtons(username, inputFlag, readNum, limit)
        print("<br>")
        print("<p>")
        for item in allList:
            if "Stream:" in item:
                msg = msg + 1
            if msg == readNum:
                print(item + "<br>")
                if "Date:" in item:
                    print("---------------------------------------<br>")
        print("</p>")
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
        printButtons(username, inputFlag, readNum, limit)
        print("<br>")
        print("<p>")
        for item in allList:
            if "Stream:" in item:
                msg = msg + 1
            if msg == readNum:
                print(item + "<br>")
                if "Date:" in item:
                    print("---------------------------------------<br>")
        print("</p>")
    return()

if __name__ == "__main__":
    main()
