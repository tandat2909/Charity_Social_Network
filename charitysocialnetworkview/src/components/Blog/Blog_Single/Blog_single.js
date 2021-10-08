import React, { useContext, useState} from 'react';
import BannerImage from '../../banner/banner-bottom-shape';
import InnerBanner from '../../banner/inner_banner';
import BlogDescBig from './blog-desc-big';
import BlogSinglePost from './Blog_single_post';
import callApi from '../../../utils/apiCaller';
import { NewsPostContextMod } from '../../../context/newspost_mod'

const BlogSingle = (props) => {
    let detailPost = useContext(NewsPostContextMod)
    let [get_post_success, setGetPostSuccess] = useState(false)
    // let url = 'http://localhost:8000/api/newspost/' + props.id.match.params.id + '/'
    const GetDetailPost = async () => {
        let url = 'api/newspost/' + props.id.match.params.id + '/'
        let a =  await callApi(url, 'GET', null, null).catch(err => { console.log(err) })
        console.log(a)
        detailPost.detail = a.data
        setGetPostSuccess(true)
    }
    console.log("BlogSingle: ",detailPost.detail)
    
    // useEffect(() => {})

    if (Object.keys(detailPost.detail).length === 0 || detailPost.detail.id !== props.id.match.params.id) {
        GetDetailPost()
        //setGetPostSuccess(false)
    }
    


    return (
        <div>
            <InnerBanner title="Single post"></InnerBanner>
            <BannerImage></BannerImage>
            {Object.keys(detailPost.detail).length !== 0 ?
                <>
                    <BlogDescBig ></BlogDescBig>
                    <BlogSinglePost></BlogSinglePost>
                </>
                : ''}

        </div>
    )
}
export default BlogSingle;
