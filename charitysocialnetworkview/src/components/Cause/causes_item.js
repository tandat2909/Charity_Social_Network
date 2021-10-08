import React from 'react';
import VisibilityIcon from '@material-ui/icons/Visibility';
import dateFormat from 'dateformat';
import { NavLink } from 'react-router-dom';
import callApi from '../../utils/apiCaller';

const CausesItem = (props) => {

    const browseArticles = async() =>{
        let browse = {"is_show": true}
        let url = "api/newspost/" + props.id + "/is-post-allowed/"
        // console.log("url:", url)
        let p = await callApi(url, 'PATCH', browse, null).then(res => {
            if (res.status === 200 || res.status === 201) {
                alert("bạn đã duyệt bài thành công")
            }
            else    
                alert("bạn đã sửa thất bại")
          
            
        })
    }

    return (

        <div className="col-lg-4 col-md-6 causes-grid">
            <div className="causes-grid-info">
                <NavLink to={'/blog_single/' + `${props.id}`} className="cause-title-wrap">
                    <div style={{display: "flex"}}>
                    <p className="title">{props.category.name} </p> <VisibilityIcon/>
                   </div>
                    <h4 className="cause-title" 
                        style={{
                            whiteSpace: "pre-wrap", 
                            textOverflow: "ellipsis", 
                            overflow: "hidden", 
                            WebkitLineClamp: "2",
                            WebkitBoxOrient: "vertical",
                            width: "100%", 
                            display: "block", 
                            display: "-webkit-box",
                            height:"16px*1.3*3",
                            textAlign: "justify"
                            }}
                    >{props.title}
                    </h4>
                    <p className="counter-inherit">
                        {dateFormat(props.dateCreate, "fullDate")}
                    </p>
                </NavLink>
                <div style={{width: "100%", height:"30%"}}>
                <img src={props.image}  
                    alt="" /></div>
                <div className="submit text-right">
                    <button className="btn btn-primary btn-style mt-4" onClick={browseArticles}>Accept</button>
                </div>
            </div>
        </div>

    )

}
export default CausesItem;