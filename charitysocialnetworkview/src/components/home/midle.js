import React, { Component } from 'react';


class Midle extends Component{
    render() {
        return(
            <div className="middle py-5" id="facts">
                <div className="container pt-lg-3">
                    <div className="welcome-left text-center py-md-5 py-3">
                        <h3 className="title-big">Over 93% of all Donations go directly to Projects.</h3>
                        <p className="my-3">Under 7% for admin, fundraising, and salaries.</p>
                        <h4>Thank you for your continued Support </h4>
                        <a href="#donate" className="btn btn-style btn-primary mt-sm-5 mt-4"><span className="fa fa-heart mr-1"></span> Donate Now</a>
                    </div>
                </div>
            </div>
        )
    }
}
export default Midle;