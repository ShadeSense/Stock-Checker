import React from 'react';
import { Route, Switch } from 'react-router-dom';

import Home from './containers/home';
import Find from './containers/find';
import Remove from './containers/remove';
import Display from './containers/display';

function Routes(){
    return (
        <Switch>
            <Route exact path="/">
                <Home />
            </Route>
            <Route exact path="/find">
                <Find />
            </Route>
            <Route exact path="/remove">
                <Remove />
            </Route>
            <Route exact path="/display">
                <Display />
            </Route>
        </Switch>
    );
}

export default Routes;

//Used to set up router for react to switch to webpages
//Reference: https://serverless-stack.com/