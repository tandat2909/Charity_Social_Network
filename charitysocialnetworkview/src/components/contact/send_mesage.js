import React, { Component } from 'react';


class SendMessage extends Component {
    render() {
        return (
            <div className="col-lg-8">
                <h3 className="title-big">Send us a Message</h3>
                <p className="mb-4 mt-lg-0 mt-2">Your email address will not be published. Required fields are marked *</p>
                <form action="https://sendmail.w3layouts.com/submitForm" method="post" className="text-right">
                    <div className="form-grid" >
                        <input type="text" name="w3lName" id="w3lName" placeholder="Name*" required="" style={{color:"#696687"}}/>
                        <input type="email" name="w3lSender" id="w3lSender" placeholder="Email*" required="" />
                        <input type="text" name="w3lPhone" id="w3lPhone" placeholder="Phone number*" required="" />
                        <input type="text" name="w3lSubject" id="w3lSubject" placeholder="Subject" />
                    </div>
                    <textarea name="w3lMessage" id="w3lMessage" placeholder="Message"></textarea>
                    <button type="submit" className="btn btn-primary btn-style mt-3">Send Message</button>
                </form>
            </div>
        )
    }
}
export default SendMessage;