import React, { useContext, useState, } from 'react';
import AuthorCard from './Author/author_card';
import Comment from './Comment/comment';
import PostContent from './post_content';
import PreviousNext from './previous_next';
import TagAndShare from './Tag_Share';
import SinglePostImage from './single-post-image';
import Reply from './reply/reply';
import RelatedPost from './ReplatedPost/RelatedPost';
import { NewsPostContextMod } from '../../../context/newspost_mod';
import callApi from '../../../utils/apiCaller';
import { useHistory } from "react-router-dom";
import {contexts} from "../../../context/context"
import {  Input } from 'antd';



const BlogSingleContent = () => {
    let inforUsser = useContext(NewsPostContextMod)
    let [post_comment_success, setPostCommentSuccess] = useState(false)
    const { TextArea } = Input;
    let [comment, setComment]=useState({
        content: ""
    })
    let commentParrent = useContext(NewsPostContextMod)
    const detailPost = useContext(NewsPostContextMod)
    const context = useContext(contexts)
    let history = useHistory()
    console.log("id bài viêt: ",detailPost.detail.id)
    const handleChangeContent = (event) => {
        const target = event.target;
        const {name, value} = target;
        setComment({...comment,
            [name]: value,
        });
    }

    const postComment = async() => {
        if(context.authorization){
            let url = 'api/newspost/' + detailPost.detail.id + '/comment/'
            let a = await callApi(url, 'POST', comment, null).then(res => {
                if (res.status === 200 || res.status === 201) 
                {
                    console.log("comment: ", res.data)
                    alert("bạn đã tạo comment thành công")
                    commentParrent.comment = {}
                    setPostCommentSuccess(res.data.id)
                    
                }
                    
            })
        }
        else{
            history.replace("/login")
        }
    }

        return (
            <div className="container pb-lg-4">
                <SinglePostImage></SinglePostImage>
                <div className="single-post-content">
                    <PostContent></PostContent>
                    <TagAndShare></TagAndShare>
                    <PreviousNext></PreviousNext>
                    { inforUsser.detail.category.id === 1  ? <AuthorCard></AuthorCard> : ""}
                    
                    <Comment postComment={post_comment_success}></Comment>
                    <div>
                    <div className="form-group">
                    <TextArea 
                        name="content" 
                        className="form-control-single" 
                        placeholder="Your Comment*" 
                        rows={4}
                        required="" 
                        spellCheck="false" 
                        style={{backgroundColor:"#b7b2b233"}}
                        onChange={handleChangeContent}>
                        </TextArea>
                </div>
                

                    <div className="submit text-right">
                        <button className="btn btn-style btn-primary" onClick={postComment}>Post Comment </button>
                    </div>

                    </div>
        
                    <RelatedPost></RelatedPost>
                   
                </div>
            </div>
        )
    
}
export default BlogSingleContent;