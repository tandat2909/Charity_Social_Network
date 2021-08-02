import React, { Component } from 'react';


class FooterContent extends Component{
    render() {
        return(
            <div className="footers20-content">
            <div className="d-grid grid-col-4 grids-content">
                <div className="column">
                    <h4>Our Address</h4>
                      <p>235 Terry, 10001 20C Trolley Square,
                        DE 19806  U.S.A.</p>
                </div>
                <div className="column">
                    <h4>Call Us</h4>
                    <p>Mon - Fri 10:30 -18:00</p>
                    <p><a href="tel:+44-000-888-999">+44-000-888-999</a></p>
                </div>
                <div className="column">
                    <h4>Mail Us</h4>
                    <p><a href="mailto:info@example.com">info@example.com</a></p>
                    <p><a href="mailto:no.reply@example.com">no.reply@example.com</a></p>
                </div>
                <div className="column">
                    <h4>Follow Us On</h4>
                    <ul>
                        <li><a href="#facebook"> {null}<span className="fa fa-facebook"
                                    aria-hidden="true"></span></a>
                        </li>
                        <li><a href="#linkedin"> {null}<span className="fa fa-linkedin"
                                    aria-hidden="true"></span></a>
                        </li>
                        <li><a href="#twitter"> {null}<span className="fa fa-twitter"
                                    aria-hidden="true"></span></a>
                        </li>
                        <li><a href="#google"> {null}<span className="fa fa-google-plus"
                                    aria-hidden="true"></span></a>
                        </li>
                        <li><a href="#github"> {null}<span className="fa fa-github" aria-hidden="true"></span></a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        )
    }
}
export default FooterContent;