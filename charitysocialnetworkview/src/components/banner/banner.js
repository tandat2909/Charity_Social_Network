
import React, { Component } from 'react';
import BannerImage from './banner-bottom-shape';
import BannerOwl from './banner-owl';


class Banner extends Component {

    render() {

        return (
            <>
                <section class="w3l-main-slider" id="home">
                    <div class="companies20-content">
                        <div class="owl-one owl-carousel owl-theme">
                            <BannerOwl></BannerOwl>
                            <BannerOwl></BannerOwl>
                            <BannerOwl></BannerOwl>
                            <BannerOwl></BannerOwl>
                            <BannerOwl></BannerOwl>
                        </div>
                    </div>
                </section>
                <BannerImage></BannerImage>


            </>
        )
    }
}
export default Banner;