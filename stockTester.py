#Objective: Takes user inputs from webapp and runs the other python scripts

#Note:  This project web scrapes data specifically from Yahoo Finance because
#       it's a site that can have its stocks legally web scraped. You can switch
#       to another site, but use at your own discretion.

from bs4 import BeautifulSoup #Web scraper
import requests #Communicate with webapp
from flask import Flask, redirect, request, jsonify #How python communicates to webapp
from flask_cors import cross_origin #Used for communication of different ports
#PORTS:
#   PYTHON: 5000
#   WEBAPP: 5001

app = Flask(__name__) #Setting up route to retrieve from webapp

import stockChecker #Web scrapes data from Yahoo Finance and other methods
import stockDB #Solely for database management
import stockLinkedList #Keeps track of what stock is in database
    #Note 1:    Since MySQL in Python can't do consecutive sql executes, the solution
    #           I found was to use a linked list. I may be wrong about sql executes,
    #           but it gives me a chance to use linked list for practice.

    #Note 2:    If a login setup was to be made, would need to change from linked list
    #           to hash table because of id in db. This would mean the id currently
    #           being used in db needs to be changed accordingly since atm it is being
    #           used solely to track number of entries. 

#Finds the page for specified stock and either parses the page for lookup
#or appends stock to link list then inserts into db
@app.route("/find", methods = ["POST"])
@cross_origin()
def pageParser():
    stock = request.get_json()
    passBool = str(stock["pass"]) #Used instead of making second post request to same page

    #Searches stock on Yahoo Finance and returns name if it's found
    if passBool == "false":
        stockName = str(stock["stockName"])
        try:
            url = "https://finance.yahoo.com/quote/" + stockName + "/?p=" + stockName
            page = requests.get(url)
            pageParse = BeautifulSoup(page.content, 'html.parser')
            stockTemp = pageParse.find(id = 'quote-header-info')
            stockTemp = stockTemp.find(class_ = 'D(ib) Fz(18px)').text
            dictStock = {"stockName": stockName, "rtrnName": stockTemp}
            return jsonify(dictStock), 200
        except:
            return "Cannot find specified stock.", 400 #bad request

    #Makes calls to stockChecker to web scrape needed info and adds the
    #stock to both the db and linked list
    elif passBool == "true":
        stockName = str(stock["stockSubName"])
        try:
            stockObj = stockChecker.stockChecker(stockName, None, None)
            bool = stockObj.chkMarketOpen() #Stock market open at 9:30AM EDT and closes at 4PM EDT
            if bool == False:
                return "Stock market is not open.", 400
            stockObj.stockPriceGeneral() #stock time, date, price, growth
            stockObj.stockPriceInfo() #stock specific info

            try:
                stockObj.addStock(stockName) #add stock to linked list
                stockObj.DBInsert(stockName) #insert stock into db
                return "ok", 200
            except Exception as e:
                print(e)
                return "Problem in inserting into database.", 400

        except Exception as e:
            print(e)
            return "Problem in inserting into database.", 400

#Returns list of stocks & entries for tabulator js and
#removes specified stock
@app.route("/remove", methods = ["POST"])
@cross_origin()
def remove():
    stock = request.get_json()
    passBool = str(stock["pass"])

    #Returns list of stocks & entries
    if passBool == "false":
        try:
            tempLL = stockLinkedList.stockList()
            stockDBObj = stockDB.stockDB()
            tempLL.initList() #Reads info from 'listdump.txt' to create linked list
            templst = tempLL.getList() #Retrieves list of stocks
            countlst = [None] * len(templst)
            rtnlst = [None] * len(templst) * 2 #Dbl size of 'countlst' because of also entries

            #Counting entries from db for each stock found
            for i in range(len(templst)):
                countlst[i] = stockDBObj.numEntries(templst[i])

            #Places stock and entries into same list and returns the list
            i = 0
            j = 0
            while j < len(templst):
                rtnlst[i] = templst[j]
                rtnlst[i + 1] = countlst[j]
                i += 2
                j += 1
            return jsonify(rtnlst), 200
        except Exception as e:
            print(e)
            return "Error: Could not display stocks.", 400

    #Removes specified stock from webapp
    elif passBool == "true":    
        try:
            stockName = str(stock["stockName"])
            stockObj = stockChecker.stockChecker(stockName, None, None)
            stockObj.removeStock(stockName) #Call removes stock from ll and db
            return "ok", 200
        except Exception as e:
            print(e)
            return "Error: Could not remove stock.", 400

#Retrieves data for tabulator js, add entries to db, and refreshes stocks in db
@app.route("/display", methods = ["POST"])
@cross_origin()
def display():
    stock = request.get_json()
    stockName = str(stock["stockName"])
    state = str(stock["state"])
    tempLL = stockLinkedList.stockList()
    tempLL.initList()

    if tempLL.chkStockName(stockName):
        #Data retrieval for tabulator js
        if state == "display": 
            try:
                stockObj = stockChecker.stockChecker(stockName, None, None)
                stockInfoLst = []
                stockInfoLst = stockObj.displayStock(stockName) #Gets all entries for stock
                #Since there would be too much info on webapp, narrowed table size to 20 entries
                if len(stockInfoLst) > 20: #Only keeps 20 of most recent entries
                    while len(stockInfoLst) > 20:
                        stockInfoLst.pop(0)
                    return jsonify(stockInfoLst), 200
                else:
                    return jsonify(stockInfoLst), 200
            except Exception as e:
                print(e)
                return "Error: Could not get selected info for stock", 400

        #Adds entries to db
        elif state == "update":
            try:
                stockObj = stockChecker.stockChecker(stockName, None, None)
                bool = stockObj.chkMarketOpen()
                if bool == False:
                    return "Stock market is not open.", 400
                #Does basic webscrape from previous and adds entry to db
                stockObj.stockPriceGeneral()
                stockObj.stockPriceInfo()
                stockObj.DBInsert(stockName)
                return "ok", 200
            except Exception as e:
                print(e)
                return "Error: Could not update stock.", 400

        #Refreshes stocks in db
        elif state == "refresh": #Takes allowable time and removes entries before it
            try:
                timeRange = str(stock["time"])
                timeRange = int(timeRange)
                stockObj = stockChecker.stockChecker(stockName, None, None)
                stockObj.refreshStock(timeRange, stockName)
                return "ok", 200
            except Exception as e:
                print(e)
                return "Error: Could not refresh stock.", 400
    else:
        return "Error: Stock does not exist.", 400

#if __name__ == '__main__':