import React, { useContext } from 'react';
import {NewsPostContextMod} from "../../../../context/newspost_mod"



const AuthorImage = () => {
    let author = useContext(NewsPostContextMod)
  
        return (
            <div className="author-left col-md-3">
                <a href="#author">
                    <img className="img-fluid radius-image" src={author.detail.user.avatar} alt="" />
                </a>
            </div>
        )
    
}
export default AuthorImage;