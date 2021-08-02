import React, { Component } from 'react';

class Mission extends Component{
    render() {
        return(
            <section className="w3-services-ab py-5" id="mission">
                <div className="container py-lg-5 py-md-4">
                    <h3 className="title-big text-center mb-5">Our Mission and Goals</h3>
                    <div className="w3-services-grids">
                        <div className="fea-gd-vv row">
                            <div className="col-lg-4 col-md-6">
                                <div className="float-lt feature-gd">
                                    <div className="icon">
                                        <img src={process.env.PUBLIC_URL + '/images/home.png'} alt="" className="img-fluid" />
                                    </div>
                                    <div className="icon-info">
                                        <h5>Homeless Charities.</h5>
                                        <p> Lorem ipsum dolor sit amet, dolor elit, sed eiusmod init
                                            tempor primis in init.</p>

                                    </div>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6 mt-md-0 mt-4">
                                <div className="float-mid feature-gd">
                                    <div className="icon">
                                        <img src={process.env.PUBLIC_URL + '/images/education.png'} alt="" className="img-fluid" />
                                    </div>
                                    <div className="icon-info">
                                        <h5>Education Charities.</h5>
                                        <p> Lorem ipsum dolor sit amet, dolor elit, sed eiusmod init
                                            tempor primis in init.</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6 mt-lg-0 mt-4">
                                <div className="float-rt feature-gd">
                                    <div className="icon">
                                        <img src={process.env.PUBLIC_URL + '/images/health.png'} alt="" className="img-fluid" />
                                    </div>
                                    <div className="icon-info">
                                        <h5>Health Charities.</h5>
                                        <p> Lorem ipsum dolor sit amet, dolor elit, sed eiusmod init
                                            tempor primis in init.</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6 mt-4 pt-md-2">
                                <div className="float-lt feature-gd">
                                    <div className="icon">
                                        <img src={process.env.PUBLIC_URL + '/images/icon1.png'} alt="" className="img-fluid" />
                                    </div>
                                    <div className="icon-info">
                                        <h5>Animal Charities.</h5>
                                        <p> Lorem ipsum dolor sit amet, dolor elit, sed eiusmod init
                                            tempor primis in init.</p>

                                    </div>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6 mt-4 pt-md-2">
                                <div className="float-lt feature-gd">
                                    <div className="icon">
                                        <img src={process.env.PUBLIC_URL + '/images/food.png'} alt="" className="img-fluid" />
                                    </div>
                                    <div className="icon-info">
                                        <h5>Food Charities.</h5>
                                        <p> Lorem ipsum dolor sit amet, dolor elit, sed eiusmod init
                                            tempor primis in init.</p>

                                    </div>
                                </div>
                            </div>
                            <div className="col-lg-4 col-md-6 mt-4 pt-md-2">
                                <div className="float-lt feature-gd">
                                    <div className="icon">
                                        <img src={process.env.PUBLIC_URL + '/images/eco.png'} alt="" className="img-fluid" />
                                    </div>
                                    <div className="icon-info">
                                        <h5>Eco Charities.</h5>
                                        <p> Lorem ipsum dolor sit amet, dolor elit, sed eiusmod init
                                            tempor primis in init.</p>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default Mission;
