import React, { Component } from 'react';
import RelatedPostContent from './relatedpost_content';


class RelatedPost extends Component {
    render() {
        return (
            <div className="item mt-5 pt-lg-5">
                    <h3 className="section-title-left mb-4">Related posts for you </h3>
                    <div className="row">
                        <RelatedPostContent></RelatedPostContent>
                        <RelatedPostContent></RelatedPostContent>
                    </div>
            </div>
        )
    }
}
export default RelatedPost;