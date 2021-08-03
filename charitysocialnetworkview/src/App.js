import React, {Component} from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Menu from './components/menu/menu';
import Home from './components/home/home';
import About from './components/about/about';


class MyComponent extends Component {
  render() {
    return (
        <Router>
            <Menu></Menu>
            <Switch>
              <Route path="/" exact component={Home} ></Route>
              <Route path="/about"  component={About}></Route>
            </Switch>
        </Router>
        
    );
  }
}

export default MyComponent;
