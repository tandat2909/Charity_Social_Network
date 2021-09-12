import React, { Component } from 'react';


class RelatedPostContent extends Component {
    render() {
        return (
            <div className="col-md-6">
                <div className="list-view list-view1">
                    <div className="grids5-info">
                        <a href="blog-single.html" className="d-block zoom"><img src={process.env.PUBLIC_URL + '/images/blog5.jpg'} alt="" className="img-fluid radius-image news-image" /></a>
                        <div className="blog-info align-self">
                            <a href="blog-single.html" className="blog-desc1">Request for an audience with First Lady Melania
                            </a>
                            <div className="entry-meta mb-3">
                                <span className="cat-links"><a href="#url" rel="category tag">Uncategorized</a></span> /
                                <span className="posted-on"><span className="published"> August 18, 2020</span></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
export default RelatedPostContent;