import React, { Component } from 'react';



class BottomGrids extends Component{
    render() {
        return(
            <section className="w3l-bottom-grids-6 py-5">
                <div className="container py-lg-5 py-md-4 py-2">
                    <div className="grids-area-hny main-cont-wthree-fea row">
                        <div className="col-lg-4 col-md-6 grids-feature">
                            <div className="area-box">
                                <img src={process.env.PUBLIC_URL + '/images/donate.png'} alt="" />
                                <h4><a href="#feature" className="title-head">Give Donation.</a></h4>
                                <p className="mb-3">Vivamus a ligula quam. Ut blandit eu leo non. Duis sed dolor amet ipsum primis in faucibus orci dolor sit et amet.</p>
                                <a href="#donate" className="btn btn-text">Donate Now </a>
                            </div>
                        </div>
                        <div className="col-lg-4 col-md-6 grids-feature mt-md-0 mt-5">
                            <div className="area-box">
                                <img src={process.env.PUBLIC_URL + '/images/volunteer.png'} alt="" />
                                <h4><a href="#feature" className="title-head">Become a Volunteer.</a></h4>
                                <p className="mb-3">Vivamus a ligula quam. Ut blandit eu leo non. Duis sed dolor amet ipsum primis in faucibus orci dolor sit et amet.</p>
                                <a href="contact.html" className="btn btn-text">Join Now </a>
                            </div>
                        </div>
                        <div className="col-lg-4 col-md-6 grids-feature mt-lg-0 mt-5">
                            <div className="area-box">
                                <img src={process.env.PUBLIC_URL + '/images/child.png'} alt="" width="52px" /> 
                                <h4><a href="#feature" className="title-head">Help the Children.</a></h4>
                                <p className="mb-3">Vivamus a ligula quam. Ut blandit eu leo non. Duis sed dolor amet ipsum primis in faucibus orci dolor sit et amet.</p>
                                <a href="#donate" className="btn btn-text">Help Now </a>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default BottomGrids;