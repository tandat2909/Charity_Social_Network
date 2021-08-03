
import React, { Component } from 'react';
import BannerImage from './banner-bottom-shape';



class Banner extends Component {
    render() {
        return (
        <div>
            <section className="w3l-main-slider" id="home">
                <div className="companies20-content">
                    <div className="owl-one owl-carousel owl-theme">
                        <div className="item">
                            <li>
                                <div className="slider-info banner-view bg bg2">
                                    <div className="banner-info">
                                        <div className="container">
                                            <div className="banner-info-bg text-left">
                                                <p>Charity Life</p>
                                                <h5>Charity, Faith and Hope. Help the Homeless. Charity life.</h5>
                                                <a href="about.html" className="btn btn-primary btn-style">Read More</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </div>
                        <div className="item">
                            <li>
                                <div className="slider-info  banner-view banner-top1 bg bg2">
                                    <div className="banner-info">
                                        <div className="container">
                                            <div className="banner-info-bg text-left">
                                                <p>Save Children</p>
                                                <h5>Donate with Kindness. Every amount Donated by you Counts.</h5>
                                                <a href="about.html" className="btn btn-primary btn-style">Read More</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </div>
                        <div className="item">
                            <li>
                                <div className="slider-info banner-view banner-top2 bg bg2">
                                    <div className="banner-info">
                                        <div className="container">
                                            <div className="banner-info-bg text-left">
                                                <p>Unconditional Help</p>
                                                <h5>Give a Helping hand. We all need to come together. Our Mission.</h5>
                                                <a href="about.html" className="btn btn-primary btn-style">Read More</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </div>
                        <div className="item">
                            <li>
                                <div className="slider-info banner-view banner-top3 bg bg2">
                                    <div className="banner-info">
                                        <div className="container">
                                            <div className="banner-info-bg text-left">
                                                <p>Unconditional Help</p>
                                                <h5>Should Children suffer this way? Don't leave Orphans alone</h5>
                                                <a href="about.html" className="btn btn-primary btn-style">Read More</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </div>
                    </div>
                </div>
            </section>
            <BannerImage></BannerImage>
        </div>
        )
    }
}
export default Banner;