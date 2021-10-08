import React, { useContext } from 'react';
import AuthorImage from './author_image';
import AuthorInfor from './author_infor';
import {NewsPostContextMod} from "../../../../context/newspost_mod"


const AuthorCard = () => {
    let author = useContext(NewsPostContextMod)
        return (
            <div className="author-card mt-5">
                    <div className="row align-items-center">
                    {author.detail.info_auction.receiver !== null ?
                        <>
                            <AuthorImage></AuthorImage>
                            <AuthorInfor></AuthorInfor>
                        </>
                    : ""}
                    </div>
                </div>
        )
    }

export default AuthorCard;