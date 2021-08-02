import React, { Component } from 'react';


class Session extends Component{
    render() {
        return(
            <section className="_form-3">
                <div className="form-main">
                    <div className="container">
                        <div className="middle-section grid-column top-bottom">
                            <div className="image grid-three-column">
                                <img src={process.env.PUBLIC_URL + '/images/subscribe.png'} alt="" className="img-fluid radius-image-full" />
                            </div>
                            <div className="text-grid grid-three-column">
                                <h2>Subscribe our Newsletter to receive latest updates from us</h2>
                                <p>We won’t give you spam mails.</p>
                            </div>
                            <div className="form-text grid-three-column">
                                <form action="/" method="GET">
                                    <input type="email" name=" placeholder" placeholder="Enter Your Email" required="" />
                                    <button type="submit" className="btn btn-style btn-primary">Submit</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default Session;