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
    
    

        return (
            <div className="container pb-lg-4">
                <SinglePostImage></SinglePostImage>
                <div className="single-post-content">
                    <PostContent></PostContent>
                    <TagAndShare></TagAndShare>
                    <PreviousNext></PreviousNext>
                    { inforUsser.detail.category.id === 1  ? <AuthorCard></AuthorCard> : ""}
                    
                    <Comment></Comment>
                    <Reply></Reply>
        
                    <RelatedPost></RelatedPost>
                   
                </div>
            </div>
        )
    
}
export default BlogSingleContent;