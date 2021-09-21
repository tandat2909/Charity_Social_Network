import React, { useContext} from 'react';
import { NewsPostContextMod } from '../../../context/newspost_mod'
import { Link } from 'react-router-dom';
import {Gavel} from '@material-ui/icons';
// import { Tooltip, Avatar } from 'antd';


const PostContent = () => {
   
    let post = useContext(NewsPostContextMod)
    return (
        <>
        {/* {post.detail.description.charAt(0).toUpperCase()} */}
            <p className="alphabet mb-4"><span className="big-letter">{post.detail.description.charAt(0).toUpperCase()}</span>{post.detail.description.slice(1, post.detail.description.lenght)}
            </p>
            <div dangerouslySetInnerHTML={{ __html: post.detail.content }}></div>
            <div className="submit text-right"><i>Được viết bởi {post.detail.user.username}</i></div>
            {post.detail.category.id === 1 ? <>
                <div className="submit text-center">
                    <Link to={"/blog/" + `${post.detail.id}` + "/auction"} props={post.detail} className="btn btn-primary btn-style mt-4">
                    <Gavel />Auction </Link>
                </div> 
            </> : ""}    


                       
        </>
    )

}
export default PostContent;