import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './display.css';
import { Alert, Button, Form } from 'react-bootstrap';
import Tabulator from 'tabulator-tables';

export function Display(){
    const [stockName, setName] = useState('');
    const [showWarn, setShowWarn] = useState('');
    const [showUpdate, setShowUpdate] = useState(''); //update alert
    const [time, setTime] = useState(''); //for refresh time post request
    const stockDisplay = []; //stores obj of stock info for tabulator

    /*Simple tabulator*/
    function displayTbl(){
        var table = new Tabulator("#disptbl", {
            data:stockDisplay,
            layout:"fitDataTable",
            resizableColumns:false,
            columns:[
                {title:"#", field:"id"},
                {title:"Stock", field:"stockname"},
                {title:"Time", field:"time"},
                {title:"Date", field:"date"},
                {title:"Stock Price", field:"stockPrice"},
                {title:"Stock Growth", field:"stockGrowth"},
                {title:"Previous Close", field:"previousClose"},
                {title:"Open", field:"open"},
                {title:"Bid", field:"bid"},
                {title:"Ask", field:"ask"},
                {title:"Day's Range", field:"daysRange"},
                {title:"Year Target", field:"yearTrgt"},
                {title:"PE Ratio", field:"PEratio"},
                {title:"Dividend and Yield", field:"dividendYield"},
                {title:"Earnings Date", field:"earningsDate"},
            ],
        });
        return table;
    }
    return(
        <div>
            {/*Tabulator srcs*/}
            <link href="https://unpkg.com/tabulator-tables@4.8.4/dist/css/tabulator.min.css" rel="stylesheet"></link>
            <script type="text/javascript" src="https://unpkg.com/tabulator-tables@4.8.4/dist/js/tabulator.min.js"></script>
            
            {/*Display Text Field*/}
            <Form className="DisplayForm">
                <Form.Group controlId="display_name">
                    <Form.Label style={{'color':'#ffffff', 'font-size':'20px'}}>Display Stock</Form.Label>
                    <Form.Control
                    type="label" 
                    placeholder="Enter Stock Name For Display" 
                    value={stockName}
                    onChange = {event => setName(event.target.value)}
                    />
                    <Form.Text className="sub-text" style={{'color':'#ffffff', 'font-size':'14px'}}>Please type valid stock name and use abbreviated name (i.e. "Amazon" is "amzn").</Form.Text>
                </Form.Group>
            </Form>

            {/*Displays Stock Info*/}
            <Button className="displaybtn" variant="outline-dark" style={{'color':'#ffffff', 'font-size':'18px'}} type="btn" onClick={async () => {
                    setShowWarn(false);
                    setShowUpdate(false);
                    if (stockName !== ""){
                        const state = "display"; //for post request in python
                        const displayStock = {stockName, state};
                        const response = await fetch("/display", {
                            method: "POST",
                            headers: {
                                "Content_Type": "application/json"
                            },
                            body:
                                JSON.stringify(displayStock)
                            });
                        if (response.ok){ /*PASS*/
                            const responseArr = await response.json();
                            if (responseArr.length === 0){
                                return console.log("Nothing to Display");
                            }
                            /*Creates obj from post request for tabulator*/
                            for (var i = 0; i < responseArr.length; i++){
                                var tempHash = {};
                                tempHash.id = responseArr[i][0];
                                tempHash.stockname = responseArr[i][1];
                                tempHash.time = responseArr[i][2];
                                tempHash.date = responseArr[i][3];
                                tempHash.stockPrice = responseArr[i][4];
                                tempHash.stockGrowth = responseArr[i][5];
                                tempHash.previousClose = responseArr[i][6];
                                tempHash.open = responseArr[i][7];
                                tempHash.bid = responseArr[i][8];
                                tempHash.ask = responseArr[i][9];
                                tempHash.daysRange = responseArr[i][10];
                                tempHash.yearTrgt = responseArr[i][11];
                                tempHash.PEratio = responseArr[i][12];
                                tempHash.dividendYield = responseArr[i][13];
                                tempHash.earningsDate = responseArr[i][14];
                                stockDisplay.push(tempHash);
                            }
                            displayTbl(); //call to make table
                            document.getElementById('display_name').readOnly = true;
                        }    
                        else{
                            setShowWarn(true);
                            document.getElementById('display_name').placeholder = "Cannot display stock.";
                            document.getElementById('display_name').readOnly = true;
                            setName("");
                        }
                    }
                    else{
                        setShowWarn(true);
                        document.getElementById('display_name').placeholder = "Cannot display stock.";
                        document.getElementById('display_name').readOnly = true;
                        setName("");
                    }
                }}>
                Display
            </Button>

            {/*Adds entry for specified stock*/}
            <Button className="updatebtn" variant="outline-dark" style={{'color':'#ffffff', 'font-size':'18px'}} type="btn" onClick={async () => {
                    setShowWarn(false);
                    setShowUpdate(false);
                    if (stockName !== ""){
                        const state = "update"; //for post request in python
                        const updateStock = {stockName, state};
                        const response = await fetch("/display", {
                            method: "POST",
                            headers: {
                                "Content_Type": "application/json"
                            },
                            body:
                                JSON.stringify(updateStock)
                            });
                        if (response.ok){ /*PASS*/
                            setShowUpdate(true);
                            document.getElementById('display_name').placeholder = "Enter Stock Name For Display";
                            setName("");
                            window.location.reload();
                            return false;
                        }
                        else{
                            setShowWarn(true);
                            document.getElementById('display_name').placeholder = "Cannot update stock.";
                            document.getElementById('display_name').readOnly = true;
                            setName("");
                        }
                    }
                    else{
                        setShowWarn(true);
                        document.getElementById('display_name').placeholder = "Cannot update stock.";
                        document.getElementById('display_name').readOnly = true;
                        setName("");
                    }
                }}>
                Update
            </Button>

            {/*Simple Reset of Text Fields*/}
            <Button className="resetbtn" variant="outline-dark" style={{'color':'#ffffff', 'font-size':'18px'}} type="reset" onClick={async () => {
                    document.getElementById('display_name').readOnly = false;
                    document.getElementById('refresh_name').readOnly = false;
                    document.getElementById('display_name').placeholder = "Enter Stock Name For Display";
                    document.getElementById('refresh_name').placeholder = "Enter number of day(s) to refresh";
                    setName("");
                    setTime("");
                    setShowWarn(false);
                    setShowUpdate(false);
                }}>
                Reset
            </Button>

            {/*Refresh Form w/ Btns*/}
            <Form className="refreshForm">
                {/*Refresh Text Field*/}
                <Form className="refresh">
                    <Form.Group controlId="refresh_name">
                        <Form.Label style={{'color':'#ffffff', 'font-size':'20px'}}>Refresh</Form.Label>
                        <Form.Control
                        type="label" 
                        placeholder="Enter number of day(s) to refresh"
                        value={time}
                        onChange = {event => setTime(event.target.value)}
                        />
                        <Form.Text className="sub-text" style={{'color':'#ffffff', 'font-size':'14px'}}>Please input a whole number of 1 or greater.</Form.Text>
                    </Form.Group>
                </Form>

                {/*Request for refreshing stock data*/}
                <Button className="refreshbtn" variant="outline-dark" style={{'color':'#ffffff', 'font-size':'18px'}} type="btn" onClick={async () => {
                        setShowWarn(false);
                        setShowUpdate(false);
                        const temp = parseInt(time); //"time" from text field is text so need to parse
                        /*If "time" is num, int, >=1, and stock name is set in display text field*/
                        if (isNaN(temp) !== true && Number.isSafeInteger(parseInt(temp, 10)) && parseInt(temp, 10) >= 1 && stockName !== ""){
                            const state = "refresh"; //for post request in python
                            const refreshStock = {stockName, state, time};
                            const response = await fetch("/display", {
                                method: "POST",
                                headers: {
                                    "Content_Type": "application/json"
                                },
                                body:
                                    JSON.stringify(refreshStock)
                                });
                            if (response.ok){ /*PASS*/
                                document.getElementById('display_name').placeholder = "Enter Stock Name For Display";
                                setName("");
                                window.location.reload();
                                return false;
                            }
                            else{
                                setShowWarn(true);
                                document.getElementById('refresh_name').placeholder = "Cannot refresh stock.";
                                document.getElementById('refresh_name').readOnly = true;
                                setName("");
                            }
                        }
                        else{
                            setShowWarn(true);
                            document.getElementById('refresh_name').placeholder = "Cannot refresh stock.";
                            document.getElementById('refresh_name').readOnly = true;
                            setName("");
                        }
                    }}>
                    Refresh
                </Button>
            </Form>

            <div id="disptbl" className="dispTbl"></div> {/*Tabulator placed after other components because css purpose*/}

            {/*Alerts*/}
            <Alert className="alertSuccess" variant="success" show={showUpdate} onClose={() => setShowUpdate(false)} dismissible>
                Stock has been updated!
            </Alert>
            <Alert className="alertWarn" variant="warning" show={showWarn} onClose={() => setShowWarn(false)} dismissible>
                A problem occurred when making changes to stock!
            </Alert>
        </div>
    );
}

export default Display;