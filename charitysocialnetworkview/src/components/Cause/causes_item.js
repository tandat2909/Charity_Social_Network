import React from 'react';



const CausesItem = () => {
   
        return (
                <div className="w3-services py-5">
                    <div className="container py-lg-4 py-md-3">
                        <div className="row w3-services-grids">
                            <div className="col-lg-4 col-md-6 causes-grid">
                                <div className="causes-grid-info">
                                    <a href="#cause" className="cause-title-wrap">
                                        <p className="title">Medicine </p>
                                        <h4 className="cause-title">Help From Injuries
                                        </h4>
                                        <p className="counter-inherit">
                                            $86,800 Donated of $310,000
                                        </p>
                                    </a>
                                    <div className="barWrapper my-4">
                                        <div className="progress-box">
                                            <div className="progress" data-value="60">
                                                <div className="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0"
                                                    aria-valuemax="100" style={{ width: "60%" }}>
                                                    <div className="value-holder"><span className="value"></span></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <a href="#cause"><img src={process.env.PUBLIC_URL + '/images/blog4.jpg'} className="img-fuild radius-image-full"
                                        alt="" /></a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            
        )
    
}
export default CausesItem;