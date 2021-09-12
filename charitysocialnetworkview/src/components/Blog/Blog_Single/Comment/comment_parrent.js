import React from 'react';
import CommentChildren from './comment_childrent';
import ListEmoji from '../../../profile/list_emoji';



const CommentParrent = (props) => {
    // let listEmotion = useContext(ListEmotion)
    // const renderEmotion = (props = listEmotion.list) =>
    //     props && props.map((emotionItem) => {
    //         return (

    //             <Tooltip title={emotionItem.name} placement="top">
    //                 <Avatar  src={emotionItem.image} onClick={() => { postEmotion(emotionItem.id) }} />
    //             </Tooltip>
    //         )
    //     })

        return (
            <div className="media">
                    <div className="img-circle">
                        <img src={props.avatar} className="img-fluid" alt="..." />
                    </div>
                    <div className="media-body">

                        <ul className="time-rply mb-2">
                            <li><a href="#URL" className="name mt-0 mb-2 d-block">{props.authorName}</a>
                                {props.timeComment}

                            </li>
                            <li className="reply-last">
                                <a href="#reply" className="reply">
                                    Reply</a>
                            </li>
                            
                                <li className="reply-last">
                                    {/* <a href="#reply" className="reply">
                                        Like</a> */}
                                        <ListEmoji></ListEmoji>
                                </li>
                            
                        </ul>
                        <p>{props.content}</p>
                        <CommentChildren></CommentChildren>
                    </div>
                </div>

        )
    
}
export default CommentParrent;