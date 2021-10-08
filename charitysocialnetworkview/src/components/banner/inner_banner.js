
import React from 'react';

const InnerBanner = (props) => {
  
        return (
            <div className="inner-banner">
                <section className="w3l-breadcrumb py-5">
                    <div className="container py-lg-5 py-md-3">
                        {/* <h4 className="title">About Us</h4> */}
                        <h4 className="title">{props.title}</h4>
                    </div>
                </section>
            </div>
        )
    
}
export default InnerBanner;