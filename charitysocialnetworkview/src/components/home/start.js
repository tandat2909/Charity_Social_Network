import React, { Component } from 'react';


class Start extends Component{
    render() {
        return(
            <section className="w3_stats py-5" id="stats">
                <div className="container py-lg-5 py-md-4 py-2">
                    <div className="title-content text-center">
                        <h3 className="title-big">Our mission is to help people by distributing Money and Service globally.</h3>
                    </div>
                    <div className="w3-stats text-center">
                        <div className="row">
                            <div className="col-md-3 col-6">
                                <div className="counter">
                                    <span className="fa fa-users"></span>
                                    <div className="timer count-title count-number mt-3" data-to="1500" data-speed="1500"></div>
                                    <p className="count-text ">Total Volunteers</p>
                                </div>
                            </div>
                            <div className="col-md-3 col-6">
                                <div className="counter">
                                    <span className="fa fa-cutlery"></span>
                                    <div className="timer count-title count-number mt-3" data-to="2256" data-speed="1500"></div>
                                    <p className="count-text ">Meals Served</p>
                                </div>
                            </div>
                            <div className="col-md-3 col-6">
                                <div className="counter">
                                    <span className="fa fa-home"></span>
                                    <div className="timer count-title count-number mt-3" data-to="1000" data-speed="1500"></div>
                                    <p className="count-text ">Got Shelter</p>
                                </div>
                            </div>
                            <div className="col-md-3 col-6">
                                <div className="counter">
                                    <span className="fa fa-male"></span>
                                    <div className="timer count-title count-number mt-3" data-to="260" data-speed="1500"></div>
                                    <p className="count-text ">Adapted Children</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default Start;