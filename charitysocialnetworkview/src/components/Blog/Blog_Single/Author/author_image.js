import React, { useContext } from 'react';
import {NewsPostContextMod} from "../../../../context/newspost_mod"



const AuthorImage = () => {
    let author = useContext(NewsPostContextMod)
  
        return (
            <div className="author-left col-md-3">
                <a href="#author">
                    {author.detail.info_auction.receiver !== null ?
                    <img className="img-fluid radius-image" src={author.detail.info_auction.receiver.avatar} alt="" />
                    : ""}
                </a>
            </div>
        )
    
}
export default AuthorImage;