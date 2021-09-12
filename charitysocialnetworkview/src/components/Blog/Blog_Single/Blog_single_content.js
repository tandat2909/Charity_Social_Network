import React, { useContext, useState, } from 'react';
import AuthorCard from './Author/author_card';
import Comment from './Comment/comment';
import PostContent from './post_content';
import PreviousNext from './previous_next';
import TagAndShare from './Tag_Share';
import SinglePostImage from './single-post-image';
import Reply from './reply/reply';
import RelatedPost from './ReplatedPost/RelatedPost';



const BlogSingleContent = () => {
    

        return (
            <div className="container pb-lg-4">
                <SinglePostImage></SinglePostImage>
                <div className="single-post-content">
                    <PostContent></PostContent>
                    <TagAndShare></TagAndShare>
                    <PreviousNext></PreviousNext>
                    <AuthorCard></AuthorCard>
                    <Comment></Comment>
                    <Reply></Reply>
                    <RelatedPost></RelatedPost>
                   
                </div>
            </div>
        )
    
}
export default BlogSingleContent;