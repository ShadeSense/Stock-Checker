#Objectives: This script does most of the data collection for the stock info.
#            It inputs data into the database and manipulates the linked list.

import datetime
import time
import pytz
import requests
from bs4 import BeautifulSoup
import stockDB
import stockLinkedList

class stockChecker:
    #Constructor for all general info
    def __init__(self, stockName, page, pageParse):
        self.stockName = stockName
        self.page = None
        self.pageParse = None
        self.quoteSummary = None
        self.time = None
        self.date = None
        self.stockPrice = None
        self.stockGrowth = None
        self.previousClose = None
        self.open = None
        self.bid = None
        self.ask = None
        self.daysRange = None
        self.yearTrgt = None
        self.PEratio = None
        self.dividendYield = None
        self.earningsDate = None
        self.infoLst = [None] * 14
    
    #Finds the page for specified stock and then parses the page for lookup
    def pageParser(self):
        #Need two parts of the url link to work with searching stock item
        urlSec1 = "https://finance.yahoo.com/quote/"
        urlSec2 = "/?p="
        urlComplete = urlSec1 + self.stockName + urlSec2 + self.stockName
        self.page = requests.get(urlComplete)
        self.pageParse = BeautifulSoup(self.page.content, 'html.parser')
    
    #Confirming if current page is for the right stock or if the stock is invalid
    #If user's response is no, user needs to re-enter stock name and redo
    #confirmStock()
    def confirmStock(self):
        try:
            stockName = self.pageParse.find(id = 'quote-header-info')
            stockName = stockName.find(class_ = 'D(ib) Fz(18px)').text
            return stockName
        except:
            print("Error: Cannot find specified stock.")
            return
    
    #Gets/sets info for current stock pricing and current growth
    def stockPriceGeneral(self):
        self.pageParser()
        general = self.pageParse.find(class_ = 'D(ib) Mend(20px)') #Finds price/growth on page

        #Sets current time
        self.time = datetime.datetime.now()
        self.time = self.time.strftime("%H:%M:%S")

        #Sets today's date
        self.date = datetime.date.today()
        self.date = str(self.date)

        self.stockPrice = general.find(class_ = 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').text #Sets price

        #Need to look for specific class info. Since rate is defined by color (green/red), need to be able to lookup both kinds just in case
        if general.find(class_ = 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)') != None:
            #Positive growth
            self.stockGrowth = general.find(class_ = 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)').text
        else:
            #Negative growth
            self.stockGrowth = general.find(class_ = 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)').text

    #Gets/sets all relative information on stock
    #Since searching data-test doesn't work, have to use an alternative to get all stocks info
    def stockPriceInfo(self):
        #Used reference below
        stockInfo = self.pageParse.find_all("tbody") #Holds all 'tbody' on page

        #Each section of "tbody" has its own "tr" sections which are being placed in their designated tables
        try:
            table1 = stockInfo[0].find_all("tr")
        except:
            table1 = None
        
        try:
            table2 = stockInfo[1].find_all("tr")
        except:
            table2 = None

        #Since the values are the only things needed for the stock's info, only the values will be stored
        stockList = list()
        
        #Finds "td" in each table and store's its values in the list
        for i in range(0, len(table1)):
            try:
                table1_td = table1[i].find_all("td")
            except:
                table1_td = None
            stockList.append(table1_td[1].text) #Appends the collective data to the list from the dict
        for i in range(0, len(table2)):
            try:
                table2_td = table2[i].find_all("td")
            except:
                table2_td = None

            stockList.append(table2_td[1].text)

        #Since SQL is being used, need to determine what info is needed for the database
        self.previousClose = stockList[0]
        self.open = stockList[1]
        self.bid = stockList[2]
        self.ask = stockList[3]
        self.daysRange = stockList[4]
        self.yearTrgt = stockList[15]
        self.PEratio = stockList[10]
        self.dividendYield = stockList[13]
        self.earningsDate = stockList[12]

        #Placing all needed info into list to be placed into database
        self.infoLst[0] = self.stockName
        self.infoLst[1] = self.time
        self.infoLst[2] = self.date
        self.infoLst[3] = self.stockPrice
        self.infoLst[4] = self.stockGrowth
        self.infoLst[5] = self.previousClose
        self.infoLst[6] = self.open
        self.infoLst[7] = self.bid
        self.infoLst[8] = self.ask
        self.infoLst[9] = self.daysRange
        self.infoLst[10] = self.yearTrgt
        self.infoLst[11] = self.PEratio
        self.infoLst[12] = self.dividendYield
        self.infoLst[13] = self.earningsDate

    #Checks current time to see if market is open. If it isn't, only shows current price/growth without 
    #recording to database.
    #Stock market opens at 9:30AM EDT and closes at 4PM EDT so need to check if time is in range of 9:30AM to 3:59:59PM
    def chkMarketOpen(self):
        lstTime = [None] * 8
        hour = ""
        minute = ""

        #Gets current eastern time since Yahoo Finance bases market openings in edt
        edtTimezone = pytz.timezone('US/Eastern')
        edt = datetime.datetime.now(edtTimezone)
        edt = edt.strftime("%H:%M:%S") #Sets edt time w/ format
        for i in range(len(lstTime)): #Parses edt time
            lstTime[i] = edt[i]
        hour += lstTime[0] + lstTime[1]
        minute += lstTime[3] + lstTime[4]
        hour = int(hour)
        minute = int(minute)

        if hour >= 9 and hour <= 15: #Only allows program usage between 9:30AM to 3:59:59PM
            if hour == 9 and minute < 30:
                return False
            else:
                return True
        return False

    #Checks stock name if it's in the list. If it isn't, add said stock to list and update SQL database.
    def addStock(self, stockName):
        if stockName == "":
            raise Exception("Error: Stock name is invalid.")

        tempLL = stockLinkedList.stockList()
        tempLL.initList() #Reads from 'listdump.txt' and creates ll
        tempDB = stockDB.stockDB()

        if tempLL.chkStockName(stockName) == False:
            tempLL.append(stockName) #Adds to ll
            tempDB.addTable(stockName) #Creates table in db for stock
        else:
            raise Exception("Error: Stock already exists.")

    #Remove said stock from list and updates SQL database.
    def removeStock(self, stockName):
        tempLL = stockLinkedList.stockList()
        tempLL.initList()
        tempDB = stockDB.stockDB()

        if tempLL.chkStockName(stockName) == True:
            tempLL.delete(stockName) #Delete from ll
            tempDB.dropTable(stockName) #Drop tbl from db
        else:
            raise Exception("Error: Stock does not exist or has already been removed.")

    #Gets all entries for stock from db
    def displayStock(self, stockName):
        tempLL = stockLinkedList.stockList()
        tempLL.initList()
        tempDB = stockDB.stockDB()

        if tempLL.chkStockName(stockName) == True:
            stockInfoLst = []
            stockInfoLst = tempDB.info(stockName)
            return stockInfoLst
        else:
            raise Exception("Error: Stock does not exist or has already been removed.")

    #Insert data into database
    def DBInsert(self, stockName):
        tempLL = stockLinkedList.stockList()
        tempLL.initList()
        tempDB = stockDB.stockDB()

        #Checks if stock exists in ll and if stock has any info
        if tempLL.chkStockName(stockName) == True and self.infoLst != None:
            tempDB.insertTable(self.infoLst)
        elif self.infoLst == None:
            raise Exception("Error: Cannot insert empty stock info list.")
        else:
            raise Exception("Error: Stock does not exist. Cannot insert.")

    #Removes specific stock info before certain time to prevent table clutter.
    #All stocks are wiped from table before that point.
    def refreshStock(self, timeRange, stockName):
        tempLL = stockLinkedList.stockList()
        tempLL.initList()
        tempDB = stockDB.stockDB()

        #Checks to see if stock exists and if the table for the stock is not empty
        if tempLL.chkStockName(stockName) == True:
            if tempDB.isEmpty(stockName) == True:
                raise Exception("Error: Table is already empty.")
        else:
            raise Exception("Error: Table for stock does not exist.")

        #Date to compare for removal
        today = datetime.date.today()
        remove_date = today - datetime.timedelta(days = timeRange)
        year = remove_date.year
        month = remove_date.month
        day = remove_date.day

        try:
            tempDB.removeBeforeDate(year, month, day, stockName)
        except:
            raise Exception("Error: Problem in refreshing table for stock.")

#Data testing
if __name__ == '__main__':
    '''
    potato = stockChecker('amzn')
    potato.pageParser()
    potato.stockPriceGeneral()
    potato.stockPriceInfo()
    #potato.DBInsert()
    '''

    '''
    today = datetime.date.today()
    remove = today - datetime.timedelta(days = 10)
    month = remove.month
    print(month)

    #print(datetime.datetime.utcfromtimestamp(today))
    #enddate = today - datetime.timedelta(days=5)
    #print(enddate)

    #potato = stockChecker('AMZN')
    #potato.pageParser()
    #pot = potato.confirmStock()
    #print(pot)
    #potato.pageParser()
    #potato.stockPriceInfo()
    #potato.stockPriceGeneral()
    #print(potato.stockPrice, potato.stockGrowth)
    '''

#Using this method, it is possible to collect all needed info about a certain stock and place them in a list
#Based on reference: https://codeburst.io/how-to-scrape-yahoo-finance-using-python-31164aa06468
#Author: Koolwal, Manthan