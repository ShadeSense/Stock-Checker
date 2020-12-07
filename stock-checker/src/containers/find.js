import './find.css';
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Alert, Button, Form } from 'react-bootstrap';

export const Find = () => {
    const [stockName, setName] = useState(''); //sets name from text field
    const [sub, setSub] = useState(''); //indicator for submit btn
    const [stockSubName, setStockSub] = useState(''); //sets stock name from post request
    /*Alerts*/
    const [showWarn, setShowWarn] = useState('');
    const [showSuccess, setShowSuccess] = useState('');
    return(
        <div>
            {/*Text Field*/}
            <Form className="FindForm">
                <Form.Group controlId="find_name">
                    <Form.Label style={{'color':'#ffffff', 'font-size':'20px'}}>Search Stock</Form.Label>
                    <Form.Control
                    type="label" 
                    placeholder="Enter Stock Name" 
                    value={stockName}
                    onChange = {event => setName(event.target.value)}
                    />
                    <Form.Text className="sub-text" style={{'color':'#ffffff', 'font-size':'14px'}}>Please type valid stock name and use abbreviated name (i.e. "Amazon" is "amzn").</Form.Text>
                </Form.Group>
            </Form>

            {/*Finds stock on Yahoo Finance and returns/sets name if found*/}
            <Button className="find" variant="outline-dark" style={{'color':'#ffffff', 'font-size':'18px'}} type="find" onClick={async () => {
                    const pass = "false";
                    const findStock = {stockName, pass};
                    const FindResponse = await fetch("/find", {
                        method: "POST",
                        headers: {
                            "Content_Type": "application/json"
                        },
                        body:
                            JSON.stringify(findStock)
                        });
                    if (FindResponse.ok){ /*PASS*/
                        const FindResponseGet = await FindResponse.json();
                        const rtrnStock = FindResponseGet["rtrnName"];
                        document.getElementById('find_name').readOnly = true;
                        setStockSub(FindResponseGet["stockName"]); //sets stock name from Yahoo Finance for submit
                        setName(rtrnStock); //same as above but for text field (not submit)
                        setShowWarn(true);
                        setShowSuccess(false);
                        setSub("true"); //stock ready for submit
                    }    
                    else{
                        setName("Please retype valid stock name.");
                        document.getElementById('find_name').readOnly = true;
                    }
                }}>
                Find
            </Button>

            {/*Tries to add stock to database, rtns error if can't*/}
            <Button className="submit" variant="outline-dark" style={{'color':'#ffffff', 'font-size':'18px'}} type="submit" onClick={async () => {
                    if (sub === "true"){
                        const pass = "true"; //since there are 2 post requests, pass="true" is to submit to database in python
                        const subStock = {stockSubName, pass};
                        const SubmitResponse = await fetch("/find", {
                            method: "POST",
                            headers: {
                                "Content_Type": "application/json"
                            },
                            body:
                                JSON.stringify(subStock)
                            });
                        if (SubmitResponse.ok){ /*PASS*/
                            document.getElementById('find_name').readOnly = true;
                            setSub("false");
                            setShowWarn(false);
                            setShowSuccess(true);
                        }    
                        else{
                            setName("Problem with submission. Please reset and try again.");
                            document.getElementById('find_name').readOnly = true;
                            setSub("false");
                            setShowWarn(false);
                            setShowSuccess(false);
                        }
                    }
                    else{
                        setName("Please enter stock first before submitting.");
                        document.getElementById('find_name').readOnly = true;
                        setSub("false");
                        setShowWarn(false);
                        setShowSuccess(false);
                    }
                }}>
                Submit
            </Button>

            {/*Simple reset fields*/}
            <Button className="reset" variant="outline-dark" style={{'color':'#ffffff', 'font-size':'18px'}} type="reset" onClick={async () => {
                    document.getElementById('find_name').readOnly = false;
                    document.getElementById('find_name').placeholder = "Enter Stock Name";
                    setName("");
                    setSub("false");
                    setShowWarn(false);
                    setShowSuccess(false);
                }}>
                Reset
            </Button>

            <Alert className="alertWarn" variant='warning' show={showWarn} onClose={() => setShowWarn(false)} dismissible>
                Make sure this is the stock you want to submit.
            </Alert>
            <Alert className="alertSuccess" variant='success' show={showSuccess} onClose={() => setShowSuccess(false)} dismissible>
                Stock has been successfully added!
            </Alert>
        </div>
    );
}

export default Find;

//Used for understanding how components/containers work and how python flask is used with them
//Reference: https://towardsdatascience.com/build-a-react-flask-app-that-suggests-novel-novels-with-a-python-graph-9491e714bbdf
//Author: Franck, Jay