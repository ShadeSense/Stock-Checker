#Objective: Python script for linked list to see what stocks been recorded.

#sys is used to find file location of 'listdump.txt' without having to
#manually find where the file is.
#os is to get size of txt in path
import sys, os

class Node:
    def __init__(self, next = None, data = None):
        self.data = data
        self.next = next

class stockList():
    def __init__(self): #Reads from 'listdump.txt' where ll is stored
        self.head = None
        self.path = sys.path[0] + "\\listdump.txt"

    #Dump to hold linked list info; does nothing if file is empty
    def initList(self):
        self.f = open(self.path, "r+") #For reading txt only
        if os.path.getsize(self.path) > 0: #If the txt has info in it
            for i in self.f:
                self.append(i.rstrip("\n")) #For python, '\n' is added at every end line of file
        self.f.close()

    #Finalizes changes to list and writes back to file
    def finList(self):
        self.f = open(self.path, "w") #Write only
        curr = self.head
        while curr != None:
            #Because of how python reads/writes to file, an empty line is added to top of file
            self.f.write(curr.data + "\n")
            curr = curr.next
        self.f.close()

    #Delete stock from ll
    def delete(self, stockName):
        if self.head == None: #Checks if list has been made
            print("Error: List of stocks has not been made.")
            return False
        elif stockName == None: #Checks if data of stock name has been passed
            print("Error: Stock name was not received to be removed.")
            return False

        #Removes from head if there is only one item in the list
        if self.head.data == stockName and self.head.next == None:
            self.head = None
            self.finList() #Finalizes any changes made
            return True
        #Removes from head if there is another item in the list
        elif self.head.data == stockName and self.head.next != None:
            temp = self.head.next
            self.head = None
            self.head = temp
            self.finList()
            return True
        
        #Checks the whole list to see if stock exists and removes it from list
        curr = self.head
        nextNode = self.head.next
        try:
            while curr != None:
                if nextNode.data != stockName:
                    curr = curr.next
                    nextNode = nextNode.next
                elif nextNode.data == stockName:
                    temp = nextNode.next
                    nextNode = None
                    curr.next = temp
                    self.finList()
                    return True
        except:
            print("Error: Problem occurred when removing stock. Make sure stock name is correct.")
            return False

    #Since the list will be small, the order does not matter meaning stock names
    #can be added at end of the list. The time complexity for reading the list
    #will be small so no need for inserting in middle nor pushing onto list
    def append(self, stockName):
        temp = Node(data = stockName)

        if self.chkStockName(stockName) == True:
            print("Error: Stock is already in database.")
            return False

        if self.head == None: #If linked list is empty, just append to head
            self.head = temp
            self.finList()
            return True

        #Append at end of ll
        curr = self.head
        try:
            while curr != None:
                if curr.next != None:
                    curr = curr.next
                elif curr.next == None:
                    curr.next = temp
                    self.finList()
                    return True
        except:
            print("Error: Problem occurred when appending to list of stocks")
            return False

    #Retrieves list of stocks from txt
    def getList(self):
        lst = []
        curr = self.head.next
        while curr != None:
            lst.append(curr.data)
            curr = curr.next
        return lst

    #Checks if stock is in linked list
    def chkStockName(self, stockName):
        curr = self.head
        while curr != None:
            if curr.data != stockName:
                curr = curr.next
            else:
                return True
        return False

    #Checks the size of the linked list. Since the allowed amount of tables is 10,
    #the linked list should only hold 10 stock names.
    def chkMaxSize(self):
        count = 0
        curr = self.head
        while curr != None:
            count += 1
            curr = curr.next
        if count > 10:
            print("Error: Stocks in database has reached full capacity.")
            return False

#Data testing
if __name__ == '__main__':
    stockLL = stockList()
    #stockLL.initList()
    #temp = stockLL.getList()
    #print(temp)
    #stockLL.delete("YH")
    #stockLL.append("YK")
    #stockLL.finList()
    #stockLL.print()
    #stockLL.append("AMZN")
    #stockLL.append("YH")
    #stockLL.append("FB")
    #stockLL.append("YB")