import React from 'react';
import './home.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Carousel } from 'react-bootstrap';
import bgi from './assets/img/stocks.jpg';
//import color from './assets/img/color.png';

function Home(){
    return(
        <div>
            <h1 className="stockChecker">
                Stock Checker
            </h1>

            {/*Simple carousel with img*/}
            <Carousel style={{'margin-left':'10%', 'margin-right':'10%', 'margin-top':'5%'}}>
                <Carousel.Item interval={5000}>
                    <img 
                        className="d-block w-100"
                        src={bgi}
                        style={{'height':'400px', 'width':'400px'}}
                        alt=""
                    />
                    <Carousel.Caption>
                        <h1>What Is Stock Checker?</h1>
                        <p>
                            Stock checker allows you to search up your favorite stocks and keep tabs on them
                            by adding it to the database!
                        </p>
                    </Carousel.Caption>
                </Carousel.Item>
                <Carousel.Item interval={5000}>
                    <img 
                        className="d-block w-100"
                        src={bgi}
                        style={{'height':'400px', 'width':'400px'}} 
                        alt=""
                    />
                    <Carousel.Caption>
                        <h1>Finding Your Favorite Stocks</h1>
                        <p>
                            Simply type in your stock on the "find" page ("Find" on the navigation bar above) 
                            and a suggested stock will appear. Determine if this is the right stock and hit 
                            submit. This will add the stock right into the database for safe keeping!
                        </p>
                    </Carousel.Caption>
                </Carousel.Item>
                <Carousel.Item interval={5000}>
                    <img 
                        className="d-block w-100"
                        src={bgi}
                        style={{'height':'400px', 'width':'400px'}} 
                        alt=""
                    />
                    <Carousel.Caption>
                        <h1>What If I Don't Want All These Stocks?</h1>
                        <p>
                            Locate "Remove" on the navigation bar and once on the page, hit the "Display"
                            button. This will show you all current stocks that are being kept. From the list
                            given, type the stock you want to remove and it'll be gone from the database.
                        </p>
                    </Carousel.Caption>
                </Carousel.Item>  
                <Carousel.Item interval={5000}>
                    <img 
                        className="d-block w-100"
                        src={bgi}
                        style={{'height':'400px', 'width':'400px'}} 
                        alt=""
                    />
                    <Carousel.Caption>
                        <h1>Updating Your Stocks and Cleaning the Clutter</h1>
                        <p>
                            The "display" page not only displays information of your selected stock, but
                            you're able to add unlimited entries for that stock. If there are too many
                            entries, just set how many days back you want to keep your stock and it'll
                            remove entries before that day.
                        </p>
                    </Carousel.Caption>
                </Carousel.Item>
            </Carousel>
        </div>
    );
}

export default Home;