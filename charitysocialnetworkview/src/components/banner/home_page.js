import React, { Component } from 'react';


class HomePage extends Component{
    render() {
        return(
            <section className="homeblock1">
                <div className="container">
                    <div className="row">
                        <div className="col-lg-4 col-md-6 col-sm-12">
                            <div className="box-wrap">
                                <h4><a href="#mission">View our Mission</a></h4>
                            </div>
                        </div>
                        <div className="col-lg-4 col-md-6 col-sm-12 mt-md-0 mt-sm-4 mt-3">
                            <div className="box-wrap">
                                <h4><a href="#team">Top Founders</a></h4>
                            </div>
                        </div>
                        <div className="col-lg-4 col-md-6 col-sm-12 mt-lg-0 mt-sm-4 mt-3">
                            <div className="box-wrap">
                                <h4><a href="contact.html">Requst a Quote</a></h4>
                            </div>
                        </div>
                    </div>
                </div>
        </section>
        )
    }
}
export default HomePage;