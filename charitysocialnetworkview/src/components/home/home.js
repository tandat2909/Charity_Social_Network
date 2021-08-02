import React, { Component } from 'react';

import Banner from '../banner/banner';
import HomePage from '../banner/home_page';
import Midle from './midle';
import BottomGrids from './bottom-grids'
import Start from './start';
import Bg from './bg';
import Causes from './causes';
import Mission from './mission';
import Clients from './clients';
import Footer from '../footer/main_footer';

class Home extends Component{
    render() {
        return(
            <div>
           
                <Banner></Banner>
                <HomePage></HomePage>
                <Midle></Midle>
                <BottomGrids></BottomGrids>
                <Start></Start>
                <Bg></Bg>
                <Causes></Causes>
                <Mission></Mission>
                <Clients></Clients>
                <Footer></Footer>
            </div>
        )
    }
}
export default Home;