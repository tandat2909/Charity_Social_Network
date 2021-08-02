import React, { Component } from 'react';

class Bg extends Component{
    render() {
        return(
            <div className="w3l-bg py-5">
                <div className="container py-lg-5 py-md-4">
                    <div className="welcome-left text-center py-lg-4">
                        <span className="fa fa-heart-o"></span>
                        <h3 className="title-big">Help the Homeless & Hungry People.</h3>
                        <a href="#donate" className="btn btn-style btn-primary mt-sm-5 mt-4">Donate Now</a>
                    </div>
                </div>
            </div>
        )
    }
}
export default Bg;