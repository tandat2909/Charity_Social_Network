import React, { Component } from 'react';


class Team extends Component {
    render() {
        return (
            <section className="w3l-team-main" id="team">
                <div className="team py-5">
                    <div className="container py-lg-5">
                        <div className="title-content text-center">
                            <h3 className="title-big">Happy Volunteers</h3>
                        </div>
                        <div className="team-row mt-md-5 mt-4">
                            <div className="team-wrap">
                                <div className="team-member text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team1.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Luke jacobs</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-wrap">
                                <div className="team-member text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team2.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Claire olson</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-wrap">
                                <div className="team-member last text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team3.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Phillip hunt</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-wrap">
                                <div className="team-member last text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team4.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Sara grant</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-wrap">
                                <div className="team-member last text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team5.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Sara grant</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-wrap">
                                <div className="team-member last text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team6.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Sara grant</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-wrap">
                                <div className="team-member last text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team7.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Sara grant</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-wrap">
                                <div className="team-member last text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team8.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Sara grant</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-wrap">
                                <div className="team-member last text-center">
                                    <div className="team-img">
                                        <img src={process.env.PUBLIC_URL + '/images/team9.jpg'} alt="" className="radius-image img-fluid" />
                                    </div>
                                    <a href="#url" className="team-title">Sara grant</a>
                                    <p>Volunteers</p>
                                </div>
                            </div>


                            <div className="team-apply">
                                <a href="#url" className="team-title m-0"><span className="fa fa-plus-circle d-block mb-3"></span> Apply for Volunteer</a>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default Team;