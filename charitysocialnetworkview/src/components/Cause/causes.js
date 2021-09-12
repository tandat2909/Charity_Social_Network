import React, { Component } from 'react';
import BannerImage from '../banner/banner-bottom-shape';
import InnerBanner from '../banner/inner_banner';
import CausesItem from './causes_item';
import Story from './story';


class CausesPage extends Component {
    render() {
        return (
            <>
                <InnerBanner></InnerBanner>
                <BannerImage></BannerImage>
                <CausesItem></CausesItem>
                <Story></Story>
            </>
        )
    }
}
export default CausesPage;