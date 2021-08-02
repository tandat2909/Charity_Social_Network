import React, { Component } from 'react';


class ALittleAbout extends Component {
    render() {
        return (
            <section className="w3l-aboutblock1 py-5" id="about">
                <div className="container py-lg-5 py-md-3">
                    <div className="row">
                        <div className="col-lg-6">
                            <h5 className="title-small">A little about Us</h5>
                            <h3 className="title-big">Welcome to Save Poor charity</h3>
                            <p className="mt-3">Lorem ipsum viverra feugiat. Pellen tesque libero ut justo,
                                ultrices in ligula. Semper at tempufddfel. Lorem ipsum dolor sit amet viverra ornare
                                elit. Non quae, ut diam libero erat.</p>
                            <p className="mt-3">Duis cursus, mi quis viverra ornare, eros dolor interdum nulla, ut sed diam libero erat. Aenean faucibus
                                nibh et justo cursus.</p>
                            <h3 className="title mt-4">"Over 20 Years of Accomplishments”</h3>
                            <a href="#MoreAboutUs" className="btn btn-primary btn-style mt-lg-5 mt-4">Learn More about Us</a>
                        </div>
                        <div className="col-lg-6 mt-lg-0 mt-5">
                            <img src={process.env.PUBLIC_URL + '/images/about.jpg'} alt="" className="radius-image img-fluid" />
                </div>
                        </div>
                    </div>
            </section>
                )
    }
}
export default ALittleAbout;