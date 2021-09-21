import React, { useState, useContext } from 'react';
import CommentChildren from './comment_childrent';
import ListEmoji from '../../../profile/list_emoji';
import DragIndicatorIcon from '@material-ui/icons/DragIndicator';
import {Menu, MenuItem, ListItem, ListItemText, ListItemSecondaryAction, Checkbox, 
    List, ListSubheader
} from '@material-ui/core';
import { Input, Modal } from 'antd';
import { Edit, Delete, ArrowRightAlt } from '@material-ui/icons';
import { TextField } from '@material-ui/core';
import callApi from '../../../../utils/apiCaller';
import moment from 'moment';
import { contexts } from '../../../../context/context'
import { report } from '../../../../context/report';
import { makeStyles } from '@material-ui/core/styles';
import Avatar from '@mui/material/Avatar';

const useList = makeStyles((theme) => ({
    root: {
        width: '100%',
        margin: "0 auto",
        backgroundColor: theme.palette.background.paper,
    },
}));


const CommentParrent = (props) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [update, setUpdate] = useState(false)
    const [deleteSucess, setDeleteSucess] = useState(false)
    const [showReply, setShowReply] = useState(false)
    const [rep, setRep] = useState(false)
    const [showReplyChild, setShowReplyChild] = useState(false)

    const [postCommentChild, setPostCommentChild] = useState()
    let [soPhanHoi, setSoPhanHoi] = useState(props.commentChild.length)
    const [updateComment, setUpdateComment] = useState(props.content);
    let [commentChildrent, setCommentChildrent] = useState()
    const context = useContext(contexts)

    const { TextArea } = Input;
    const list = useList();


    const modal =  useContext(report)

    let [isShowModal, setShowModal] = useState(false)
    // modal.showModal =  {isShowModal, setShowModal}

    let [checkBoxValue, setCheckBoxValue] = useState()
    let [contentReport, setContentReport] = useState()

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleChange = (event) => {
        setUpdateComment(event.target.value);

    }

    const changePostCommentChild = (event) => {
        setPostCommentChild(event.target.value)
    }

    const handleChangeCheckbox = (event) => {
        setCheckBoxValue(event.target.value);
    }

    const handleChangeContent = (event) => {
        setContentReport(event.target.value);
    }

    const deleteComment = async () => {
        let url = 'api/comment/' + props.id + '/'
        let a = await callApi(url, 'DELETE', null, null).then(res => {
            if (res.status === 204)
                alert("bạn đã xóa bình luận thành công")
        })
        // console.log("url: ", url)
        console.log("có vô delelte")
        setDeleteSucess(true)
    }

    const postCommentChildren = async () => {
        let payload = { "comment_parent": props.id, "content": postCommentChild }
        let url = 'api/newspost/' + props.idPost + '/comment/'
        let a = await callApi(url, 'POST', payload, null)
        if (a.status === 200 || a.status === 201) {
            alert("bạn đã trả lời bình luận thành công")
            setShowReplyChild(true)
            setSoPhanHoi(soPhanHoi + 1)
            setCommentChildrent(a.data)
        }

        console.log("dl: ", Object.keys(a.data))
        console.log("comment: ", commentChildrent)
    }
    const patchComment = async () => {

        let payload = { "content": updateComment }
        let url = 'api/comment/' + props.id + '/'
        let a = await callApi(url, 'PATCH', payload, null).then(res => {
            if (res.status === 200 || res.status === 201) {
                alert("bạn đã sửa bình luận thành công")
                setUpdate(false)
            }
            else {
                setUpdateComment(props.comment)
            }

        })
        // console.log("content: ", payload)
    }

    const showCommentChild = () =>

        props.commentChild && props.commentChild.map((child) => {
            return (
                <CommentChildren
                    id={child.id}
                    key={child.id}
                    content={child.content}
                    timeComment={moment(new Date(child.update_date), "YYYYMMDD, h:mm:ss").fromNow()}
                    user={child.user}
                ></CommentChildren>
            )

        })


    const ReplyComment = () => {
        return (
            <div className="media second mt-4 p-0 pt-2">
                <a className="img-circle img-circle-sm" href="#url">
                    <img src={context.dataProfile.avatar} className="img-fluid" alt="..." />
                </a>
                <div className="media-body">
                    <ul className="time-rply mb-2">
                        <li><p style={{ color: "#1b1616c9" }}>{context.dataProfile.username}</p>
                            {showReplyChild !== false && commentChildrent !== undefined ? moment(new Date(commentChildrent.update_date), "YYYYMMDD, h:mm:ss").fromNow() : ""}
                        </li>
                        {showReplyChild !== false && commentChildrent !== undefined ? <><li className="reply-last" onClick={() => setRep(true)}>
                            <a href="#/" className="reply">
                                Reply</a>
                        </li>

                            <li className="reply-last">
                                <DragIndicatorIcon aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick} />
                            </li> </> : ""}
                        <li style={{ display: "block" }}>
                            {showReplyChild === false ?
                                <TextField
                                    style={{ backgroundColor: "#635b5b38" }}
                                    id="outlined-basic"
                                    variant="outlined"
                                    variant="outlined"
                                    size="small"
                                    onChange={changePostCommentChild}
                                    onKeyPress={event => { if (event.key === 'Enter') { postCommentChildren() } }}
                                /> :
                                <>

                                    <p>{postCommentChild}</p>
                                </>
                            }
                        </li>
                    </ul>


                </div>
            </div>
        )
    }


    const showListReport = () =>
        modal.list && modal.list.map((item, index) => {
            return (
                <ListItem dense button key={item.id} >
                        <ListItemText primary={(index + 1) + '. ' + item.content} />
                        <ListItemSecondaryAction>
                            <Checkbox  edge="end"
                                checked ={parseInt(checkBoxValue) === item.id}
                                onChange={handleChangeCheckbox}
                                value={item.id}
                                name="content"
                                inputProps={{ 'aria-label': item.id }}
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
            )
        })

    const ReportPost = async(id) => {
        console.log("id user: ", id)
        // console.log("id bài viết: ",hashTag.detail.id)
        if(checkBoxValue === undefined){
            alert("bạn cần chọn lí do để report")
        }
        else{
            let report = {"reason" : parseInt(checkBoxValue), "content" : contentReport, "user_report" : id}
            let url = 'api/accounts/report/'
            let a = await callApi(url, 'POST', report, null).then(res => {
                if (res.status === 200 || res.status === 201){
                    alert("bạn đã report user thành công")
                    setShowModal(false)
                }
                    

            }).catch(err => {console.log(err)})
            
        }
    }

    return (
        <>
            {deleteSucess === false ? <>
                <div className="media">
                    <div className="img-circle">
                        <img src={props.avatar} className="img-fluid" alt="..." />
                    </div>
                    <div className="media-body" >

                        <ul className="time-rply mb-2">
                            <li><p style={{ color: "#1b1616c9" }}>{props.authorName}</p>

                                {props.timeComment}

                            </li>
                            <li className="reply-last" onClick={() => setRep(true)}>
                                <a href="#/" className="reply">
                                    Reply</a>
                            </li>

                            <li className="reply-last">
                                <DragIndicatorIcon aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick} />
                            </li>

                            {/* <li className="reply-last" >
                                <ListEmoji ></ListEmoji>
                            </li>  */}

                        </ul>
                        {update === true ? <>
                            <TextField
                                id="outlined-disabled"
                                defaultValue={updateComment}
                                variant="outlined"
                                variant="filled"
                                size="small"
                                onChange={handleChange}
                                // name="content"
                                onKeyPress={event => { if (event.key === 'Enter') { patchComment() } }}
                            /><span style={{ fontSize: "15px", display: "block" }} onClick={() => setUpdate(false)}>Hủy</span> </> :
                            <p>{updateComment}</p>}
                        {
                            rep === true ? ReplyComment() : ""
                        }
                        {/* <ListEmoji></ListEmoji> */}
                        {/* <CommentParrent {...props.commentTest} ></CommentParrent> */}
                        {soPhanHoi > 0 && showReply === false ?
                            <p onClick={() => setShowReply(true)} style={{ fontStyle: "italic", fontSize: "16px", color: "#41aada" }}><ArrowRightAlt />{soPhanHoi} phản hồi</p>

                            : ""}
                        {showReply === true ? showCommentChild() : ""}
                        {/* <CommentChildren></CommentChildren> */}
                    </div>

                </div>
                <Menu
                    id="simple-menu"
                    anchorEl={anchorEl}
                    keepMounted
                    open={Boolean(anchorEl)}
                    onClose={handleClose}

                >
                    <MenuItem onClick={() => { setUpdate(true) }} ><Edit />Edit</MenuItem>
                    <MenuItem onClick={deleteComment}><Delete />Delete</MenuItem>
                    <MenuItem onClick={() => {setShowModal(true); setAnchorEl(null) }}><span class="fas fa-user-cog" aria-hidden="true" style={{ fontSize: "25px" }}></span>Report</MenuItem>
                </Menu>
                

                
                <Modal title="Repost Post" visible={isShowModal}  onCancel={() => {setShowModal(false)}} onOk={() => {ReportPost(props.user.id)}}>
                <List 
                    subheader={
                        <ListSubheader>
                            <p>Thông tin user</p>
                            <div style={{margin: "15px auto", display: "flex"}}>
                                <Avatar src={props.user.avatar} />
                                <p style={{color: "#ff5200", margin: "10px"}}>{props.authorName}</p>
                            </div>
                            
                            <h5 style={{color: "red"}}>Hãy chọn vấn đề</h5>
                            
                        </ListSubheader>
                        } 
                    className={list.root} style={{  margin: "0 auto"}}>
                    {showListReport()}
                </List>
                <TextArea
                    className="form-control-single" 
                    placeholder="Description" 
                    rows={2}
                    spellCheck="false" 
                    style={{backgroundColor:"#dcd4d433"}}
                    onChange={handleChangeContent}
                    >
                        </TextArea>
            </Modal>
            </>
                : ""}

        </>
    )

}
export default CommentParrent;


