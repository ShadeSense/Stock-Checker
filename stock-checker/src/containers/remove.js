import './remove.css';
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Alert, Button, Form } from 'react-bootstrap';
import Tabulator from 'tabulator-tables';

/*  
    Used to make table that shows stock names and their entries.
    Since I wanted this on page load, only solution found was
    to use async componentDidMount() with its post request. This
    is because reg dynamic table takes too much space and is
    unreliable while tabulator makes it better in this case.
*/
class StockList extends React.Component{
    async componentDidMount(){
        try{
            const stockDisplay = []; //stores obj of stock names & entries from post
            const pass = "false" //1st option in post request (retrieves from db)
            const feed = {pass}
            const response = await fetch("/remove", {
                method: "POST",
                headers: {
                    "Content_Type": "application/json"
                },
                body:
                    JSON.stringify(feed)
                });
            if (response.ok){
                const responseArr = await response.json();
                if(responseArr.length === 0){
                    return console.log("Nothing to Display");
                }
                /*Creates obj from array passed in from post and push to array*/
                for(var i = 0; i < responseArr.length; i++){
                    var tempHash = {};
                    tempHash.name = responseArr[i]
                    i += 1;
                    tempHash.entry = responseArr[i]
                    stockDisplay.push(tempHash);
                }
            }
            var table = new Tabulator("#disptbl", { //creates table
                    data:stockDisplay,
                    layout:"fitDataTable",
                    resizableColumns:false,
                    columns:[
                        {title:"Stocks", field:"name", sortable:false},
                        {title:"Entries", field:"entry", sortable:false},
                    ],
                });
            return table;
        }
        catch(e){
            console.log(e);
        }
    }
    render(){
        return(null);
    }
}

export function Remove(){
    const [stockName, setName] = useState('');
    const [showSuccess, setShowSuccess] = useState('');
    const [showWarn, setShowWarn] = useState('')
    return(
        <div>
            {/*Tabulator sources*/}
            <link href="https://unpkg.com/tabulator-tables@4.8.4/dist/css/tabulator.min.css" rel="stylesheet"></link>
            <script type="text/javascript" src="https://unpkg.com/tabulator-tables@4.8.4/dist/js/tabulator.min.js"></script>

            {/*Text Field*/}
            <Form className="RemoveForm">
                <Form.Group controlId="remove_name">
                    <Form.Label style={{'color':'#ffffff', 'font-size':'20px'}}>Remove Stock</Form.Label>
                    <Form.Control
                    type="label" 
                    placeholder="Enter Stock Name For Removal" 
                    value={stockName}
                    onChange = {event => setName(event.target.value)}
                    />
                    <Form.Text className="sub-text" style={{'color':'#ffffff', 'font-size':'14px'}}>Please type valid stock name and use abbreviated name (i.e. "Amazon" is "amzn").</Form.Text>
                </Form.Group>
            </Form>

            <StockList/> {/*Call to make table; placed after text field for css purpose*/}
            <div id="disptbl" className="disptbl"></div>

            {/*Removes stock from db if stock found*/}
            <Button className="removebtn" variant="outline-dark" style={{'color':'#ffffff', 'font-size':'18px'}} type="btn" onClick={async () => {
                    setShowWarn(false);
                    setShowSuccess(false);
                    if (stockName !== ""){
                        const pass = "true"; //2nd option in post request (deletion)
                        const removeStock = {stockName, pass};
                        const response = await fetch("/remove", {
                            method: "POST",
                            headers: {
                                "Content_Type": "application/json"
                            },
                            body:
                                JSON.stringify(removeStock)
                            });
                        if (response.ok){ /*PASS*/
                            document.getElementById('remove_name').placeholder = "Enter Stock Name For Removal";
                            setName("");
                            setShowSuccess(true); //somewhat useless due to reload; just for design
                            /*Reload is necessary to reload tabulator so user can see what stock is available*/
                            window.location.reload();
                            return false;
                        }    
                        else{
                            setShowWarn(true);
                            document.getElementById('remove_name').placeholder = "Enter Stock Name For Removal";
                            setName("");
                        }
                    }
                    else{
                        setShowWarn(true);
                        document.getElementById('remove_name').placeholder = "Enter Stock Name For Removal";
                        setName("");
                    }
                }}>
                Remove
            </Button>

            {/*Alerts*/}
            <Alert className="alertSuccess" variant="success" show={showSuccess} onClose={() => setShowSuccess(false)} dismissible>
                Stock has been successfully removed!
            </Alert>
            <Alert className="alertWarn" variant="warning" show={showWarn} onClose={() => setShowWarn(false)} dismissible>
                A problem occurred when removing stock!
            </Alert>
        </div>
    );
}

export default Remove;