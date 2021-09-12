import React, { Component } from 'react';
import Form from './form';


class Reply extends Component {
    render() {
        return (
            <div className="leave-comment-form mt-5 pt-lg-4" id="reply">
                <h4 className="side-title mb-2">Leave a reply</h4>
                <p className="mb-4">Your email address will not be published. Required fields are marked *
                </p>
                <Form></Form>
            </div>
        )
    }
}
export default Reply;
