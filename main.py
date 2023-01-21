# This is a sample Python script.

import csv

import pandas
import pandas as pd
import urllib.request
import urllib.error

sfHeader = 'SFV East Coast and GG Strive 1: Connection test to Ashburn, VA. Speeds must be checked at testmyspeed.onl [here.](https://testmyspeed.onl/)'
ggHeader = 'GG Strive 2 AND SFV West Coast: Connection test to Sacramento, CA. Speeds must be checked at testmyspeed.onl [here.](https://testmyspeed.onl/)'
discord = 'Join https://discord.gg/pVUHbgX on Discord!'

df = pd.read_csv("attendeeList.csv", usecols=['GamerTag',sfHeader,ggHeader,discord,'SFV East Coast','West Coast SFV','Guilty Gear Strive BEGINNER ONLY'])

regionNumber = int(input('what region are you testing for 0 = ECSFV, 1 = WC SFV, 2 = GG Strive: \n'))

def SortEntrantsByGame(num):
    if num==0:
        return pd.DataFrame(df.dropna(subset=['SFV East Coast']))
    elif num==1:
        return  df.dropna(subset=['West Coast SFV'])
    elif num==2:
        return  df.dropna(subset=['Guilty Gear Strive BEGINNER ONLY'])
    else:
        return




def speedTestMain(num):
    check = bool
    check1 = bool
    check2 = bool

    evalFrame = SortEntrantsByGame(num)
    if num==0:
        location = '"Ashburn'
    elif num==1:
        location = '"Sacramento'

    correctLoc = bool
    correctLoc1 =bool
    correctLoc2 = bool

    if num==0:
        for ind in evalFrame.index:
            urlData = evalFrame.loc[ind].at[sfHeader]
            tag = str(evalFrame.loc[ind].at[discord])
            gtag = evalFrame.loc[ind].at['GamerTag']
            try:
                urlOpen = urllib.request.urlopen((urlData))
                data = urlOpen.read()
                checkJitter(data, 6,tag)
                correctLoc = checkLocation(data,location, tag)
                checkPing(data, 50, tag)
                check = True
            except:
                check = False

            if not check:
                print("@" + tag + ": " + gtag + " Didn't submit a valid speedtest to Ashburn, VA on <https://testmyspeed.onl")

            elif not correctLoc:
                print("@" + tag + ": " + gtag + " Wrong Server selected East Coast use Ashburn, VA on <https://testmyspeed.onl> ")

    if num==1:
        for ind in evalFrame.index:
            urlData = evalFrame.loc[ind].at[ggHeader]
            tag = str(evalFrame.loc[ind].at[discord])
            gtag = evalFrame.loc[ind].at['GamerTag']
            check = False
            try:
                urlOpen = urllib.request.urlopen((urlData))
                data = urlOpen.read()
                checkJitter(data, 6,tag)
                correctLoc = checkLocation(data,location, tag)
                checkPing(data, 50, tag)
                check = True
            except:
                check = False

            if not check:
                print("@" + tag + ": " + gtag + " Didn't submit a valid speedtest to Sacramento, CA on <https://testmyspeed.onl>")

            if not correctLoc:
                print("@" + tag + ": " + gtag + " Wrong Server selected West coast use Sacramento, CA on <https://testmyspeed.onl>")

    if num==2:
        for ind in evalFrame.index:
            urlData = evalFrame.loc[ind].at[sfHeader]
            urlData2 = evalFrame.loc[ind].at[ggHeader]
            tag = str(evalFrame.loc[ind].at[discord])
            gtag = evalFrame.loc[ind].at['GamerTag']
            check1 = False
            check2 = False

            try:
                urlOpen = urllib.request.urlopen((urlData))
                data = urlOpen.read()
                checkJitter(data, 6, tag)
                correctLoc1 = checkLocation(data, '"Ashburn', tag)
                checkPing(data, 100, tag)
                check1 = True
            except:
                check1 = False

            try:
                urlOpen2 = urllib.request.urlopen(urlData2)
                data2 = urlOpen2.read()
                checkJitter(data2, 6, tag)
                correctLoc2 = checkLocation(data2, '"Sacramento', tag)
                checkPing(data2, 100, tag)
                check2 = True
            except:
                Check2 = False

            if not check1:
                print("@" + tag + ": " + gtag + " Didn't submit a valid speedtest to Ashburn, VA")
            if not check2:
                print("@" + tag + ": " + gtag + " Didn't submit a valid speedtest to Sacramento, CA")

            if not correctLoc1:
                print("@" +tag + " Wrong Server selected for East Coast, use Ashburn, VA")
            if not correctLoc2:
                print("@" +tag + " Wrong Server selected for West Coast, use Sacramento, CA")



#urlData = df.loc[10].at[sfHeader]
#urlData2 = df.loc[10].at[ggHeader]


#print(urlData2)



#jitter = urlOpen.find('jitter')

#df2 = pd.read_json(data,usecols)

def checkJitter(data,jitterMax, tag):
    dStr = str(data)
    dataSplit = dStr.split(",")

    for d in dataSplit:
        if '"jitter":' in d:
            split = d.split(":")
            if(int(split[1])>jitterMax):
                print("@" + tag + " jitter is: " + split[1] + "ms must be below 6ms")

def checkLocation(data, location,tag):
    dStr = str(data)
    dataSplit = dStr.split(",")

    for d in dataSplit:
        if '"serverName":' in d:
            split = d.split(":")
            if split[1] != location:
                return False
            else:
                return True

def checkPing(data, maxPing, tag):
    dStr = str(data)
    dataSplit = dStr.split(",")
    for d in dataSplit:
        if '"latency":' in d:
            split = d.split(":")
            if int(split[1]) > maxPing:
                print("@" + tag + " Ping is at: " + split[1]+"ms must be below 50ms")



speedTestMain(regionNumber)
