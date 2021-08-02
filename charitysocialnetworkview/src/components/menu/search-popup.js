
import React, {Component} from 'react';


class SearchPopup extends Component {
  render() {
    return (
        <div id="search" className="pop-overlay">
            <div className="popup">
                <h4 className="mb-3">Search here</h4>
                <form action="error.html" method="GET" className="search-box">
                    <input type="search" placeholder="Enter Keyword" name="search" required="required" autoFocus="" />
                    <button type="submit" className="btn btn-style btn-primary">Search</button>
                </form>
            </div>
            <a className="close" href="#close">×</a>
        </div>
        )
  }
}

export default SearchPopup;