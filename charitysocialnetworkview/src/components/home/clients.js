import React, { Component } from 'react';

class Clients extends Component{
    render() {
        return(
            <section className="w3l-clients py-5" id="clients">
                <div className="call-w3 py-lg-5 py-md-4">
                    <div className="container">
                        <h3 className="title-big text-center">Whom we work with</h3>
                        <div className="company-logos text-center mt-5">
                            <div className="row logos">
                                <div className="col-lg-2 col-md-3 col-4">
                                    <img src={process.env.PUBLIC_URL + '/images/brand1.png'} alt="" className="img-fluid" />
                                </div>
                                <div className="col-lg-2 col-md-3 col-4">
                                    <img src={process.env.PUBLIC_URL + '/images/brand2.png'} alt="" className="img-fluid" />
                                </div>
                                <div className="col-lg-2 col-md-3 col-4">
                                    <img src={process.env.PUBLIC_URL + '/images/brand3.png'} alt="" className="img-fluid" />
                                </div>
                                <div className="col-lg-2 col-md-3 col-4 mt-md-0 mt-4">
                                    <img src={process.env.PUBLIC_URL + '/images/brand4.png'} alt="" className="img-fluid" />
                                </div>
                                <div className="col-lg-2 col-md-3 col-4 mt-lg-0 mt-4">
                                    <img src={process.env.PUBLIC_URL + '/images/brand5.png'} alt="" className="img-fluid" />
                                </div>
                                <div className="col-lg-2 col-md-3 col-4 mt-lg-0 mt-4">
                                    <img src={process.env.PUBLIC_URL + '/images/brand6.png'} alt="" className="img-fluid" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default Clients;