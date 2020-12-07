#Objective: Python script for running the database.

#Note:  I tried to make sql executes injection resistant,
#       but since this is just a simple proj for one user,
#       I decided it wasn't completely needed. However, if
#       this becomes something bigger, than injection preventions
#       would need to be looked further into.

import mysql.connector
import datetime

class stockDB:
    #Constructor that connects to server and makes a cursor.
    #Checks to see if database is made, if not, a dummy cursor
    #makes a connection to server to create database and
    #remakes connection to the database.
    #This is in response to a possible future case that there 
    #might be multiple objs in js that might create errors.
    def __init__(self):
        try:
            self.stockDB = mysql.connector.connect(
                host = "localhost",
                user = "root",
                port = 3306,
                password = "",
                database = "stocksdatabase"
            )
            #Having unbuffered cursor creates unread results when selecting * from table
            self.stockCursor = self.stockDB.cursor(buffered=True)
        except:
            #Creates database
            self.stockDB = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = ""
            )
            self.stockCursor = self.stockDB.cursor(buffered=True)
            self.stockCursor.execute("CREATE DATABASE stocksdatabase")

            #Reconnects to database
            self.stockDB = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "stocksdatabase"
            )
            self.stockCursor = self.stockDB.cursor(buffered=True)

    #Can have upto 10 tables. It is possible to make two tables with general info and in-depth info,
    #but since each stock will have multiple entries of their data, it's best to have each stock have
    #their own table with pertained info.
    def addTable(self, stockName):
        try:
            sqlStr1 = "CREATE TABLE "
            sqlStr2 = " (id INT AUTO_INCREMENT PRIMARY KEY, stock_name VARCHAR(255), time VARCHAR(255), \
                date VARCHAR(255), stock_price VARCHAR(255), growth VARCHAR(255), prev_close VARCHAR(255), \
                open VARCHAR(255), bid VARCHAR(255), ask VARCHAR(255), days_range VARCHAR(255), \
                yr_trgt VARCHAR(255), PE_Ratio VARCHAR(255), Divid_Yield VARCHAR(255), earn_date VARCHAR(255))"
            sql = sqlStr1 + stockName + sqlStr2
            self.stockCursor.execute(sql)
            self.stockDB.commit()
        except:
            print("Error: Table for specified stock has already been made.")
            return

    #Drops specified table
    def dropTable(self, stockName):
        try:
            sql = "DROP TABLE IF EXISTS " + stockName
            self.stockCursor.execute(sql)
            self.stockDB.commit()
        except:
            print("Error: Table does not exist.")
            return

    #Checks if specific table is empty
    def isEmpty(self, stockName):
        try:
            sql = "SELECT * FROM " + stockName
            self.stockCursor.execute(sql)
            if self.stockCursor.fetchone() == None:
                return True
            return False
        except:
            print("Error: Problem in checking stock table.")
            return

    #Inserts given list into table row by converting the list into a tuple
    def insertTable(self, infoLst):
        try:
            stockName = infoLst[0]
            convLstToTuple = tuple(infoLst)
            sqlStr1 = "INSERT INTO "
            sqlStr2 = " (stock_name, time, date, stock_price, growth, prev_close, open, bid, ask, days_range, \
                yr_trgt, PE_Ratio, Divid_Yield, earn_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql = sqlStr1 + stockName + sqlStr2
            self.stockCursor.execute(sql, convLstToTuple)
            self.stockDB.commit()
        except:
            raise Exception("Error: Problem in inserting to table.")

    def removeBeforeDate(self, year, month, day, stockName):
        try:
            sql = "SELECT date FROM " + stockName
            self.stockCursor.execute(sql)
            result = self.stockCursor.fetchall()
            for i in result:
                #Parsing date string from sql table to usable date
                date = "".join(i)
                tempYear, tempMonth, tempDay = "", "", ""
                tempYear += date[0] + date[1] + date[2] + date[3]
                tempMonth += date[5] + date[6]
                tempDay += date[8] + date[9]

                #Takes both date passed in and parsing date and makes them date objects
                #They then can be compared to see if the date retrieved needs to be deleted
                removeBefore = datetime.datetime(year, month, day)
                tempDate = datetime.datetime(int(tempYear), int(tempMonth), int(tempDay))
                if tempDate < removeBefore:
                    sql = "DELETE FROM " + stockName + " WHERE date = %s"
                    date = (i[0], )
                    self.stockCursor.execute(sql, date)
                    self.stockDB.commit()
                    
                #Since the table's data does not need to be sorted nor moved around, 
                #it means that the data in the table is already in chronological order.
                #So, it just needs to repeat the process till removeBefore date is found.
                #aka: new entry is added at the bottom of the table instead of top.
                else:
                    print("No needed changes were done.")
                    return
        except:
            raise Exception("Error: Problem in removing entry from table.")

    #Counts number of entries for certain stock
    def numEntries(self, stockName):
        try:
            sql = "SELECT * FROM " + stockName
            self.stockCursor.execute(sql)
            result = self.stockCursor.fetchall()
            count = 0
            for i in result: #Ignore warning; 'i' only used for incrementing
                count += 1
            return count
        except:
            raise Exception("Error: Problem in counting number of entries in table.")

    #Retrieves all entries from stock
    def info(self, stockName):
        try:
            sql = "SELECT * FROM " + stockName
            self.stockCursor.execute(sql)
            result = self.stockCursor.fetchall()
            stockInfoLst = []
            for i in result:
                stockInfoLst.append(i)
            return stockInfoLst
        except:
            raise Exception("Error: Problem in getting info on stock.")

#Data testing
if __name__ == '__main__':
    '''
    infoLst = [None]*14
    infoLst[0] = "AMZN"
    infoLst[1] = "10:24"
    infoLst[2] = datetime.date.today()
    infoLst[3] = "316.48"
    infoLst[4] = "61 (+3.6%)"
    infoLst[5] = "312"
    infoLst[6] = "564564"
    infoLst[7] = "54654"
    infoLst[8] = "21234"
    infoLst[9] = "6546"
    infoLst[10] = "56498"
    infoLst[11] = "8974564"
    infoLst[12] = "654123"
    infoLst[13] = "5644654"
    '''
    '''
    potato = stockDB()
    #potato.insertTable(infoLst)
    #print(potato.isEmpty("AMZN"))
    #potato.addTable("AMZN")
    #name = "AMZN"
    #potato.dropTable(name)
    '''
    '''
    #columnName = [None]*14
    stockDB = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "stocksdatabase"
    )
    mycursor = stockDB.cursor()
    #mycursor.execute("SHOW TABLES")
    mycursor.execute("SELECT date FROM tsla")
    for i in mycursor:
        print(i)
    '''
    '''
    #mycursor.execute("SHOW columns FROM AMZN")
    mycursor.execute("SELECT date FROM AMZN")
    myresult = mycursor.fetchall()
    for i in myresult:
        datelst = [None] * 10
        year, month, day = "", "", ""
        #month = ""
        #day = ""
        date = "".join(i)
        #for i in range(len(datelst)):
        #    datelst[i] = date[i]
        #print(datelst)
        year += date[0] + date[1] + date[2] + date[3]
        month += date[5] + date[6]
        day += date[8] + date[9]
        year = int(year)
        month = int(month)
        day = int(day)
        removeBefore = datetime.datetime(year, month, day)
        print(removeBefore)
    '''
    #mycursor.execute("CREATE DATABASE stocksdatabase")
    #sql = "DROP DATABASE " + 'stocksdatabase'
    #mycursor.execute(sql)
    #mycursor.execute("SHOW DATABASES")
    #test = mycursor.execute("SHOW DATABASES LIKE 'stocksdatabase'")
    #if test == None:
    #    mycursor.execute("CREATE DATABASE stocksdatabase")
    