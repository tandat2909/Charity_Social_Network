import React, { Component } from 'react';
import InnerBanner from './../banner/inner_banner';
import BannerImage from '../banner/banner-bottom-shape';
import ALittleAbout from './A-little-about';
import '../../css/style-liberty.css'
import FactsAbout from './facts-about';
import Video from './video';
import Team from './team';
import Testimonials from './testimonials';


class About extends Component {
    render() {
        return (
            <div>
                <InnerBanner title="About"></InnerBanner>
                <BannerImage></BannerImage>
                <ALittleAbout></ALittleAbout>
                <FactsAbout></FactsAbout>
                <Video></Video>
                <Team></Team>
                <Testimonials></Testimonials>
                
            </div>
        )
    }
}
export default About;