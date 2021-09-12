import $ from 'jquery'
export let setting_owl=() =>{
  
        $('.owl-one').owlCarousel({
          loop: true,
          dots: false,
          margin: 0,
          nav: true,
          responsiveClass: true,
          autoplay: true,
          autoplayTimeout: 5000,
          autoplaySpeed: 1000,
          autoplayHoverPause: false,
          responsive: {
            0: {
              items: 1
            },
            480: {
              items: 1
            },
            667: {
              items: 1
            },
            1000: {
              items: 1
            }
          }
        })
}
   


