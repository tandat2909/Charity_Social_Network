import '../../css/style-starter.css'
import React, { Component } from 'react';
import NavItem from './nav-item';
import LightDark from './light-dark';
import { Link, withRouter } from 'react-router-dom';




const WebsiteHeader = props => {
    if (props.location.pathname === "/login" || props.location.pathname === "/chat" || props.location.pathname === "/register") return null;
    return (
        <Menu></Menu>
    );
};



class Menu extends Component {
    render() {
        return (
            
            <header id="site-header" className="fixed-top">
                <div className="container">
                    <nav className="navbar navbar-expand-lg stroke">
                        <h1 style={{marginTop: "0px"}}><Link className="navbar-brand mr-lg-5"  to="/">
                            <img src={process.env.PUBLIC_URL + '/images/logo.png'} alt="Your logo" title="Your logo" />Save Poor</Link>
                        </h1>

                        <button className="navbar-toggler  collapsed bg-gradient" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon fa icon-expand fa-bars"></span>
                            <span className="navbar-toggler-icon fa icon-close fa-times"></span>
                        </button>
                        <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
                            <NavItem></NavItem>
                        </div>
                        {/* toggle switch for light and dark theme  */}
                        <LightDark></LightDark>
                    </nav>
                </div>
            </header>
           
           
        )
    }
}

export default withRouter(WebsiteHeader);