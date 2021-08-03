import React, { Component } from 'react';
import InnerBanner from './../banner/inner_banner';
import BannerImage from '../banner/banner-bottom-shape';
import ALittleAbout from './A-little-about';
import Footer from '../footer/main_footer';
import FactsAbout from './facts-about';
import Video from './video';
import Team from './team';

class About extends Component {
    render() {
        return (
            <div>
                <InnerBanner></InnerBanner>
                <BannerImage></BannerImage>
                <ALittleAbout></ALittleAbout>
                <FactsAbout></FactsAbout>
                <Video></Video>
                <Team></Team>
                <Footer></Footer>
                
            </div>
        )
    }
}
export default About;