import React, { Component } from 'react';



class CommentChildren extends Component {
    render() {
        return (
            <div className="media second mt-4 p-0 pt-2">
                <a className="img-circle img-circle-sm" href="#url">
                    <img src={process.env.PUBLIC_URL + '/images/team3.jpg'} className="img-fluid" alt="..." />
                </a>
                <div className="media-body">
                    <ul className="time-rply mb-2">
                        <li><a href="#URL" className="name mt-0 mb-2 d-block">Jackson Wyatt</a>
                            August 19th, 2020 - 14:20 pm

                        </li>
                        <li className="reply-last">
                            <a href="#reply" className="reply"> Reply</a>
                        </li>
                    </ul>
                    <p>At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis
                        corrupti quos dolores et. Lorem ipsum dolor sit amet......</p>
                </div>
            </div>
        )
    }
}
export default CommentChildren;