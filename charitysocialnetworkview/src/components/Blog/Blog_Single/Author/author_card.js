import React, { Component } from 'react';
import AuthorImage from './author_image';
import AuthorInfor from './author_infor';



class AuthorCard extends Component {
    render() {
        return (
            <div className="author-card mt-5">
                    <div className="row align-items-center">
                        <AuthorImage></AuthorImage>
                        <AuthorInfor></AuthorInfor>
                    </div>
                </div>
        )
    }
}
export default AuthorCard;