import SearchPopup from './search-popup'
import React, { Component } from 'react';


class SearchRight extends Component {
    render() {
        return (
            <div className="search-right">
                <a href="#search" title="search"><span className="fa fa-search" ></span></a>
                 {/* <!-- search popup --> */}
                <SearchPopup></SearchPopup>
            </div>
                )
  }
}

export default SearchRight;