import React, { Component } from 'react';


class Video extends Component {
    render() {
        return (
            <section className="w3l-aboutblock3 py-5" id="videos">
                <div className="video-recipe py-lg-5 py-md-3">
                    <div className="container">
                        <div className="row">
                            <div className="col-lg-5 align-self">
                                <h3 className="title-big">To help the poor to raise their head and face the future with pride</h3>
                                <p className="mt-4">Lorem ipsum viverra feugiat. Pellen tesque libero ut justo,
                                    ultrices in ligula. Semper at tempufddfel. Lorem ipsum dolor sit amet consectetur adipisicing
                                    elit. Non quae, fugiat consequatur voluptatem nihil ad. Lorem ipsum dolor sit amet</p>
                            </div>
                            <div className="col-lg-7 mt-lg-0 mt-md-5 mt-4">
                                <div className="row">
                                    <div className="col-md-6">
                                        <iframe src="https://www.youtube.com/embed/MG3jGHnBVQs" frameBorder="0" title="video1"
                                            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                                            allowFullScreen></iframe>
                                        <h3 className="video-title mt-sm-4 mt-3">The man of the poor.</h3>
                                    </div>
                                    <div className="col-md-6 mt-md-0 mt-5">
                                        <iframe src="https://www.youtube.com/embed/MG3jGHnBVQs" frameBorder="0" title="video2"
                                            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                                            allowFullScreen></iframe>
                                        <h3 className="video-title mt-sm-4 mt-3">Mission of “garbage people”</h3>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default Video