import React, { Component } from 'react';
import HomePage from '../banner/home_page';
import Midle from './midle';
import BottomGrids from './bottom-grids'
import Start from './start';
import Bg from './bg';
import Causes from './causes';
import Mission from './mission';
import Clients from './clients';
import SimpleSlider from '../banner/banner_slick';
import BannerImage from '../banner/banner-bottom-shape';



class Home extends Component {

    render() {
       
        return (
            <div>
                <SimpleSlider></SimpleSlider>
                <BannerImage></BannerImage>
                <HomePage></HomePage>
                <Midle></Midle>
                <BottomGrids></BottomGrids>
                <Start></Start>
                <Bg></Bg>
                <Causes></Causes>
                <Mission></Mission>
                <Clients></Clients>

            </div>
        )
    }
}
export default Home;