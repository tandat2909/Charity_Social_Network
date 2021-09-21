import React, { Component } from 'react';
import ListTestimonial from './list-testimonial';



class Testimonials extends Component {
    render() {
        return (
            <section className="w3l-testimonials" id="testimonials">
                
                <div className="customer-layout py-5">
                    <div className="container py-lg-5 py-md-4">
                        <div className="heading align-self text-center">
                            <h6 className="title-small">Our Testimonials</h6>
                            <h3 className="title-big mb-md-5 mb-4">Over 20 Years of Accomplishments</h3>
                        </div>
                        
                        <div className="row testimonial-row">
                            <div id="" className=" mb-lg-3 mb-5 col-12">
                                    <ListTestimonial></ListTestimonial>
                            </div>
                                            
                        </div>
                                           
                    </div>
                </div>
                                        
          </section>
                                    
                                    )
    }
    }
    
export default Testimonials