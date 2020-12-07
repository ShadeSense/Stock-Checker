#**IMPORTANT**  
*__This project web scrapes data from stocks from Yahoo Finance.  
This is due to it being legal to web scrape from Yahoo Finance.  
If you choose to change to a different website, use at your own  
discretion.__*  

#**Side Notes**  
*This is my first time using JS and react-bootstrap as well as  
only having used html and css a small bit beforehand. Things  
such as positions of elements, JS syntax, etc. might seem a bit  
awkward. The main goal of this project was to display information  
found from Yahoo Finance because web scraping with just Python  
seemed like a dull project. This project is also meant as a  
template for if, or when, I decide to work on this more. Since it  
did its intended purpose that I strived for, I decided to stop.  
I wanted this to be a somewhat small project so I can proceed  
with other projects and, therefore, I don't get tied down by one  
thing. So, sorry in advance for the messiness.*  
  
*As for SQL, as stated previously, this project is meant only  
for display and changing stock info. So SQL injection preventions  
weren't entirely in place. I have followed some procedures, but  
since the main purpose of the project is for personal use, it  
wasn't something sought after. If I decide to continue this  
project at a later time, it'll be something to look forward to.*  
  
#####**WHAT TO INSTALL**  
**Javascript**: For JS, "yarn" is installed instead of using npm,  
so everything needed should be contained in the folder.  
However, here's a list:  
```
   jquery.tabulator  
   react-bootstrap  
   yarn  
   react router dom
```
  
**Python**: For Python, an environment is made in the folder  
because flask is used. So, everything should also be in  
the folder. Here's the list:  
```
   pip
   beautifulsoup4
   requests
   flask
   flask_cors
   mysql.connector
```
  
*__NOTE__: This project was done in python 3.7.5. If using Visual Studios,  
need to 'view' > 'command palette' > 'Python: select interpreter' > Python 3.7.5.*  
  
#####**SETTING UP DB IF IT DOESNT WORK BY DEFAULT**  
The Python code handling connections to the DB has been tested to work  
if a database for it hasn't been made yet. However, there is still a possibility  
of it not working. Copy/paste the code below in an empty python file to create the database:  
  
```python
if __name__ == '__main__':
    stockDB = mysql.connector.connect(
        host = "yourhostname",
	user = "yourrootname",
	password = "yourpass",
    )
    stockCursor = stockDB.cursor()
    stockCursor.execute("CREATE DATABASE stocksdatabase")
```
  
#####**SETTING FLASK SERVER AND WEBAPP**  
To run this project, you need to setup both the webapp and python servers in order  
for them to communicate with each other.  
  
**Webapp**: Open "stock-checker" in the project folder in Visual Studios. At the bottom,  
	go to terminal and type "yarn start".  
  
**Python**: Open command prompt and copy file location text of project folder. Type:  
	"cd filelocationtext" where "filelocationtext" is the location of file.  
	Then copy/paste these in order:
```
   env\Scripts\activate
   set FLASK_APP=stockTester.py
   flask run
   *(Don't copy/paste all at once; enter each line one-by-one)
```
  
*__NOTE__:  To stop the project, do ctrl+c in the command prompt to stop the server from  
	running on Python's side. Also, do ctrl+c in the terminal for the webapp and  
	type "y" to stop the server.*  
  
#####**HOW TO USE EACH PAGE**  
**FIND**: 	Type a stock name in the text field provided (use abbreviations; i.e. 'Amazon' = 'amzn').  
	Clicking "Find" will search Yahoo Finance for the stock and return the stock name in the  
	text field if found. Clicking "Submit" afterwards will add the stock to the database as  
	well as an entry.  
	*This page only finds the stock, if you want repeated entries, go to "Display" page.*  
  
**REMOVE**:	The table on this page shows all the stocks and their entries. Type in any of the stock  
	names provided in the table in the text field for removal. Clicking "Remove" will delete  
	all entries and the stock itself from the database. The page will refresh so the table  
	will reflect these changes.  
  
**DISPLAY**: Type a stock name in the text field provided (use abbreviations; i.e. 'Amazon' = 'amzn').  
	 Clicking "Display" will display the twenty most recent entries of that specific stock.   
	 The # next to each stock* represents how many entries were made for it. Clicking "Update"  
	 will add an entry for that stock**. For "Refresh," type in a number of day(s) you would want  
	 to keep the stock. For example, if you only want to keep stock entries that were made 2 days  
	 prior from the current time, you would type "2". This will remove all previous stock entries  
	 prior to the number. If you want to display/change another stock, simply click "Reset."  
  	
	*If you refresh the stock, the # will mean total entries but not how many exists in the DB.  
	**Clicking "Display," "Update," or "Refresh" after entering a stock name will gray out the  
	text field. So, clicking "Update"/"Refresh" after "Display" will change that stock.  
