import React, { Component } from 'react';
import InnerBanner from './../banner/inner_banner';
import BannerImage from './../banner/banner-bottom-shape';
import ContactAdress from './contact_adress';
import SendMessage from './send_mesage';


class Contact extends Component {
    render() {
        return (
            <div >
                <InnerBanner title="Contact Us"></InnerBanner>
                <BannerImage></BannerImage>
                <section className="w3l-contact-7 py-5" id="contact">
                    <div className="contacts-9 py-lg-5 py-md-4">
                        <div className="container">
                            <div className="top-map">
                                <div className="row map-content-9">
                                    <SendMessage></SendMessage>
                                    <ContactAdress></ContactAdress>
                                    </div>
                                </div>
                            </div>
                        </div>
                </section>
            </div>
        )
    }
}
export default Contact;
