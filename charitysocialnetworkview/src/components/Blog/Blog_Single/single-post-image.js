import React, {useContext} from 'react';
import {NewsPostContextMod} from '../../../context/newspost_mod'

const SinglePostImage = () => {
    let detail = useContext(NewsPostContextMod)
    
    
        return (
            <div className="single-post-image" style={{textAlign: 'center'}}>
                <div className="post-content">
                    <img src={detail.detail.image} className="radius-image-full img-fluid mb-5" alt="" />
                </div>
            </div>
        )
    
}
export default SinglePostImage;