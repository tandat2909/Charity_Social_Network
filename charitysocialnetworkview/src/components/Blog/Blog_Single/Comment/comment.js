import React, { useContext, useEffect, useState } from 'react';
import CommentParrent from './comment_parrent'
import {NewsPostContextMod} from "../../../../context/newspost_mod"
import axios from 'axios';
import dateFormat from 'dateformat';
import moment from 'moment';



const Comment = (props) =>  {
    let commentParrent = useContext(NewsPostContextMod)
    let [get_comment_success, setGetCommentSuccess] = useState(false)

    // let [array, setArray] = useState(false)
    const CommentParrents = async() => {
        let url = 'http://127.0.0.1:8000/api/newspost/' + commentParrent.detail.id + '/comments/'
        let a = await axios({
            method: "GET",
            url: url
        }).catch(err => { console.log(err) })
        // console.log(a)
        // setArray(true)
        commentParrent.comment = a.data
        setGetCommentSuccess(true)
        // console.log(url)
        
    }
    
    // console.log("props: ", props.postComment)
    // useEffect(() => {
    //     CommentParrents()
    // },[props.postComment])

    if(Object.keys(commentParrent.comment).length === 0){
        CommentParrents()
    }
    
    // console.log("comment: ",commentParrent.comment)
    
    
    const ShowComment = (props = commentParrent.comment) => 
        props.results && props.results.map((commentItem) => {
                return(
                <CommentParrent 
                    key={commentItem.id}
                    id={commentItem.id}
                    user={commentItem.user}
                    avatar={commentItem.user.avatar}
                    authorName={commentItem.user.username}
                    Name={`${commentItem.user.last_name}` + ' ' + `${commentItem.user.first_name}`}
                    timeComment={moment(new Date(commentItem.created_date), "YYYYMMDD, h:mm:ss").fromNow()}
                    content={commentItem.content}
                    commentChild={commentItem.comment_child}
                    idPost={commentParrent.detail.id}
                    
                    >
                </CommentParrent>)
            });
    

        return (

            
            <div className="comments mt-5 pt-lg-4">
                <h4 className="side-title ">Comments ({commentParrent.comment.count})</h4>
                {ShowComment()}
               
            </div>
        )
    
}
export default Comment;