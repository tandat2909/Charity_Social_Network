import React, { Component } from 'react';




class ItemTestimonial extends Component {
    render() {
        return (
            <div className="item mr-3">
                <div className="testimonial-content">
                    <div className="testimonial">
                        <blockquote>
                            <q>Lorem ipsum dolor sit amet int consectetur adipisicing elit. Velita beatae laudantium
                                voluptate rem ullam dolore nisi voluptatibus est quasi, doloribus tempora.</q>
                        </blockquote>
                        <div className="testi-des">
                            <div className="test-img"><img src={process.env.PUBLIC_URL + '/images/team1.jpg'} className="img-fluid" alt="client-img" />
									</div>
                                <div className="peopl align-self">
                                    <h3>Michael D. Kirby</h3>
                                    <p className="indentity">Former U.S. Ambassador </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )
    }
}
export default ItemTestimonial;