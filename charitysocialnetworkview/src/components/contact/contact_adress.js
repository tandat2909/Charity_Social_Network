import React, { Component } from 'react';

class ContactAdress extends Component {
    render() {
        return (
            <div className="col-lg-4 cont-details">
                <address>
                    <h5 className="">Contact Address</h5>
                    <p><span className="fa fa-map-marker"></span>235 Terry, 10001 20C Trolley Square, DE 19806 U.S.A. </p>
                    <p> <a href="mailto:info@example.com"><span
                        className="fa fa-envelope"></span>info@example.com</a></p>
                    <p><span className="fa fa-phone"></span><a href="tel:+44-000-888-999"> +44-000-888-999</a></p>
                    <a href="donate.html" className="btn btn-style btn-outline-primary mt-4">
                        <span className="fa fa-heart mr-1"></span> Make Donation</a>
                </address>
            </div>
        )
    }
}
export default ContactAdress;