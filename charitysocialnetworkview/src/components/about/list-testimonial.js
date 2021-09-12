import React, { Component } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css";
import ItemTestimonial from "./item-testimonial";



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

class ListTestimonial extends Component {
  render() {
    const settings = {
       
      dots: true,
      infinite: true,
      speed: 500,
      slidesToShow: 3,
      slidesToScroll: 1,
      nextArrow: <SampleNextArrow />,
      prevArrow: <SamplePrevArrow />,
    //   variableWidth: true
    };
    return (
      
          
                <Slider {...settings}>
                    
                
                    <ItemTestimonial></ItemTestimonial>
                    <ItemTestimonial></ItemTestimonial>         
                    <ItemTestimonial></ItemTestimonial>
                    <ItemTestimonial></ItemTestimonial>
                    <ItemTestimonial></ItemTestimonial>
                
                </Slider>
            
       
    );
  }
}
export default ListTestimonial;