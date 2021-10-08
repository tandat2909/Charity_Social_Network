import React, { Component } from 'react';
import FooterContent from './footer_content';
import FooterFlex from './footer_flex';
import Session from './session';
import { withRouter } from 'react-router-dom';


const WebsiteFooter = props => {
    if (props.location.pathname === "/login" || props.location.pathname === "/chat" || props.location.pathname === "/register") return null;
    return (
        <Footer></Footer>
    );
};


const Footer = () =>{

    const topFunction = () =>{
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
        return(
            <div className="w3l-footer-main">
                <div className="w3l-sub-footer-content">
                    <Session></Session>
                    
                    <footer className="footer-14">
                        <div id="footers14-block">
                            <div className="container">
                                <FooterContent></FooterContent>
                                <FooterFlex></FooterFlex>
                            </div>
                        </div>
                        
                        <button  id="movetop" onClick={topFunction} title="Go to top">
                            &uarr;
                        </button>
                        
                        

                    </footer>
                    
                </div>
            </div>
        )
    
}
export default withRouter(WebsiteFooter);