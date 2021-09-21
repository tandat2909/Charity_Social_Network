import React, {useContext} from 'react';
import {NewsPostContextMod} from '../../../context/newspost_mod'
import dateFormat from 'dateformat';
import AuthorImage from './Author/author_image';

const BlogDescBig = () => {
    let detail = useContext(NewsPostContextMod)
        return (
         
            <div className="py-md-5 pt-5 pb-4 w3l-singleblock1" >
                <div className="container mt-md-3">
                    <h3 className="blog-desc-big">{detail.detail.title}</h3>
                    <div className="blog-post-align">
                        <div className="entry-meta">
                            <span className="comments-link"> <a href="#reply">Leave a Comment</a> </span> /
                            <span className="cat-links"><a href="#url" rel="category tag">{detail.detail.category.name}</a></span> /
                            <span className="posted-on"><span className="published"> {dateFormat(detail.detail.update_date, "fullDate")}</span></span>
                        </div>
                    </div>
                </div>
            </div>
            
        )   
}
export default BlogDescBig;