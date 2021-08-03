import React, { Component } from 'react';
import FooterContent from './footer_content';
import FooterFlex from './footer_flex';
import Session from './session';


class Footer extends Component{
    render() {
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
                        
                        <button  id="movetop" title="Go to top">
                            &uarr;
                        </button>
                        
                        

                    </footer>
                    
                </div>
            </div>
        )
    }
}
export default Footer;