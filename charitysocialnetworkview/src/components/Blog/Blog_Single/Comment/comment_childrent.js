import React, { useState } from 'react';
import DragIndicatorIcon from '@material-ui/icons/DragIndicator';
import {Menu, MenuItem, TextField} from '@material-ui/core';
import {Edit,Delete} from '@material-ui/icons';
import callApi from '../../../../utils/apiCaller';

const CommentChildren = (props) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [update, setUpdate] = useState(false)
    const [deleteSucess, setDeleteSucess] = useState(false)
    const [updateComment, setUpdateComment] = useState(props.content);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
      };
    
    const handleClose = () => {
    setAnchorEl(null);
    };

    const handleChange = (event) => {
        const target = event.target;
        const { name, value } = target;
        setUpdateComment(value );
    }
    const patchComment = async() =>{
       
        let payload = {"content":updateComment}
        let url = 'api/comment/' + props.id + '/'
        let a =  await callApi(url, 'PATCH', payload, null).then(res => {
            if (res.status === 200 || res.status === 201 )
            {
                alert("bạn đã sửa bình luận thành công")
                setUpdate(false)
            } 
            else{
                setUpdateComment(props.comment)
            }
                
        })
        // console.log("content: ", payload)
    }
        return (
            <>
            
            {deleteSucess === false ?<>
            <div className="media second mt-4 p-0 pt-2">
                <a className="img-circle img-circle-sm" href="#url">
                    <img src={props.user.avatar} className="img-fluid" alt="..." />
                </a>
                <div className="media-body">
                    <ul className="time-rply mb-2">
                        <li><p style={{color: "#1b1616c9"}}>{props.user.username}</p>
                           {props.timeComment}
                        </li>
                        <li className="reply-last">
                            <a href="#reply" className="reply"> Reply</a>
                        </li>
                        <li className="reply-last">
                                <DragIndicatorIcon aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}/>
                        </li>
                    </ul>
                    {update === true ? <>
                            <TextField
                            id="outlined-disabled"
                            defaultValue={updateComment}
                            variant="outlined"
                            variant="filled"
                            size="small"
                            onChange={handleChange}
                            name="content"
                            onKeyPress={event => {if(event.key === 'Enter'){patchComment()}}}
                        /><span style={{fontSize: "15px", display: "block"}} onClick={() => setUpdate(false)}>Hủy</span> </>: 
                    <p>{updateComment}</p>}
                  
                </div>
            </div>
            <Menu
                    id="simple-menu"
                    anchorEl={anchorEl}
                    keepMounted
                    open={Boolean(anchorEl)}
                    onClose={handleClose}

                >
                    <MenuItem onClick={() => { setUpdate(true)}}><Edit/>Edit</MenuItem>
                    <MenuItem><Delete/>Delete</MenuItem>
                    
                </Menu>
             </>
                :""}
        </>
        )
  
}
export default CommentChildren;