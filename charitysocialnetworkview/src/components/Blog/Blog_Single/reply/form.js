import React, { useContext, useState } from 'react';
import {NewsPostContextMod} from '../../../../context/newspost_mod'
import callApi from '../../../../utils/apiCaller';
import { useHistory } from "react-router-dom";
import {contexts} from "../../../../context/context"
import {  Input } from 'antd';




const Form = () => {
    const { TextArea } = Input;
    let [comment, setComment]=useState({
        content: ""
    })
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
            // let post = {...comment}
            let url = 'api/newspost/' + detailPost.detail.id + '/comment/'
            let a = await callApi(url, 'POST', comment, null).then(res => {
                if (res.status === 200 || res.status === 201) 
                    alert("bạn đã tạo comment thành công")
            })
        }
        else{
            history.replace("/login")
        }
    }

    
        return (
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
                        <button className="btn btn-style btn-primary" onClick={postComment}>Post Comment </button></div>
                </div>
        )
    
}
export default Form;