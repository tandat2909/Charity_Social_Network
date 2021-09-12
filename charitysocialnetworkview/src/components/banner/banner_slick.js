import React, { Component } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css";
import BannerOwl from "./banner-owl";


function SampleNextArrow(props) {
  const { className, style, onClick } = props;
  return (
    <div
      className={className}
      style={{ ...style, display: "block", right: "10px" }}
      onClick={onClick}
    />
  );
}

function SamplePrevArrow(props) {
  const { className, style, onClick } = props;
  return (
    <div
      className={className}
      style={{ ...style, display: "block", left: '10px', zIndex: "1"}}
      onClick={onClick}
    />
  );
}

class SimpleSlider extends Component {
  render() {
    const settings = {
       
      dots: true,
      infinite: true,
      speed: 500,
      slidesToShow: 1,
      slidesToScroll: 1,
      nextArrow: <SampleNextArrow />,
      prevArrow: <SamplePrevArrow />
    };
    return (
      <div className="w3l-main-slider">
        <div className="companies20-content">
          
                <Slider {...settings}>
                    
                <BannerOwl></BannerOwl>
                <BannerOwl></BannerOwl>
                <BannerOwl></BannerOwl>
                <BannerOwl></BannerOwl>
                <BannerOwl></BannerOwl>
                
                </Slider>
            
        </div>
      </div>
    );
  }
}
export default SimpleSlider;