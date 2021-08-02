import React, { Component } from 'react';


class FactsAbout extends Component {
    render() {
        return (
            <section className="w3l-forms-9 py-5" id="">
                <div className="main-w3 py-lg-5 py-md-3">
                    <div className="container">
                        <div className="row align-items-center">
                            <div className="main-midd col-lg-9">
                                <h3 className="title-big">Facts about Save Poor charity</h3>
                                <p className="mt-3">A lot of work goes down at the grass root level in villages in the remotest corners
                                    as
                                    well as the most populous metros across India, with schools and government bodies.
                                    We need your contributions to keep coming in.</p>
                            </div>
                            <div className="main-midd-2 col-lg-3 mt-lg-0 mt-4 text-lg-right">
                                <a className="btn btn-style btn-primary" href="#donate"><span className="fa fa-heart mr-1"></span> Donate
                                    Now </a>
                            </div>
                        </div>

                        <div className="donar-img mt-5">
                            <div className="right-side text-center">
                                <span className="fa fa-heart"></span>
                                <p>OUR TOP DONAR</p>
                                <h3 className="big my-3">$1.6m</h3>
                                <a className="btn btn-text" href="#ViewMore">View More</a>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default FactsAbout;