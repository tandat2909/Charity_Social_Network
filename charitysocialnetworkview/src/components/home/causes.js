import React, { Component } from 'react';

class Causes extends Component{
    render() {
        return(
            <section className="w3l-index5 py-5" id="causes">
                <div className="container py-lg-5 py-md-4">
                    <div className="row">
                        <div className="col-lg-4">
                            <div className="header-section">
                                <h3 className="title-big">Our Charity Causes </h3>
                                <h4>If you want to work with for Save Poor charity? <a href="#url">Send your Details.</a></h4>
                                <p className="mt-3 mb-lg-5 mb-4"> Lorem ipsum dolorus animi obcaecati vel ipsum. Vivamus a ligula quam.
                                    Ut blandit eu leo non. Duis sed dolor amet ipsum primis in faucibus orci dolor sit et amet igula quam.</p>
                            </div>
                            <a href="contact.html" className="btn btn-outline-primary btn-style">Contact Us</a>
                        </div>
                        <div className="col-lg-4 col-md-6 mt-lg-0 mt-5">
                            <div className="img-block">
                                <a href="causes.html">
                                    <img src={process.env.PUBLIC_URL + '/images/blog5.jpg'} className="img-fluid radius-image-full" alt="" />
                                    <span className="title">Food for Hungry</span>
                                </a>
                            </div>
                            <div className="img-block mt-4">
                                <a href="causes.html"> <img src={process.env.PUBLIC_URL + '/images/blog2.jpg'} className="img-fluid radius-image-full"
                                        alt="" />
                                    <span className="title">Help from Injuries</span>
                                </a>
                            </div>
                        </div>
                        <div className="col-lg-4 col-md-6 mt-lg-0 mt-md-5 mt-4">
                            <div className="img-block">
                                <a href="causes.html"> <img src={process.env.PUBLIC_URL + '/images/blog3.jpg'} className="img-fluid radius-image-full"
                                        alt="" />
                                    <span className="title">Education for all</span>
                                </a>
                            </div>
                            <div className="img-block mt-4">
                                <a href="causes.html">
                                    <img src={process.env.PUBLIC_URL + '/images/blog4.jpg'} className="img-fluid radius-image-full" alt="" />
                                    <span className="title">Clean water for all</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default Causes;