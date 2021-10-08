import React from 'react';
import dateFormat from 'dateformat';
import { Link } from 'react-router-dom';
import { Badge } from 'antd';
import 'antd/dist/antd.css';
import { Statistic } from 'antd';

const BlogPostItem = (props) =>{

    const hashTag = ()=>{
        let a= ""
        props.hashTag.forEach(h =>{
            a+= "#" + h.name +" "
        })
        return a
    }
    let date = new Date().getTime()
    const { Countdown } = Statistic;

    
    let deadline = props.end_datetime !== undefined ? new Date(props.end_datetime).getTime()  :"";
    let kq = deadline > date ? "đúng" : "không đúng"
    console.log(kq, deadline)
        return (
            <div className="item mt-5" style={{textAlign: "left"}}>
                <div className="row">
                    <div className="col-lg-6">
                        {props.category.id === 1 ?
                        <Badge.Ribbon text={deadline > date === true ? "Happening" : "Finished"} color={deadline > date === true ? "volcano": "purple"} 
                        style={{fontSize: "25px", width: "30%", height: "10%", textAlign:"center"}}>
                            <Link to={'blog_single/' + `${props.id}`} >
                                <img className="card-img-bottom d-block radius-image-full" src={props.image} alt="" />
                            </Link>
                        </Badge.Ribbon>: 
                        <Link to={'blog_single/' + `${props.id}`} >
                            <img className="card-img-bottom d-block radius-image-full" src={props.image} alt="" />
                        </Link>}
                    </div>
                    <div className="col-lg-6 blog-details align-self mt-lg-0 mt-4">
                        <Link to={'blog_single/' + `${props.id}`} className="blog-desc-big">{props.title}
                        </Link>
                        <div className="entry-meta mb-3"><span className="comments-link"> <a href="blog-single.html#reply">{hashTag()}</a> </span></div>
                        <div className="entry-meta mb-3"> 
                            <span className="comments-link"> <a href="blog-single.html#reply">{props.category.name}</a> </span> /
                            <span className="cat-links"><a href="#url" rel="category tag">{props.category.name}</a></span> / 
                            <span className="posted-on"><span className="published">{dateFormat(props.created_date, "dd-mm-yyyy HH:MM:ss TT")}</span></span>
                        </div>
                        <p style={{
                            whiteSpace: "pre-wrap", 
                            textOverflow: "ellipsis", 
                            overflow: "hidden", 
                            WebkitLineClamp: "3",
                            WebkitBoxOrient: "vertical",
                            width: "100%", 
                            display: "block", 
                            display: "-webkit-box",
                            height:"16px*1.3*3",
                            textAlign: "justify"
                            }}>{props.description}</p>
                        {/* {props.end_datetime} */}
                        {props.category.id === 1  ? <Link to={'blog_single/' + `${props.id}`} className="btn btn-primary btn-style mt-4">
                            {deadline > date ? <Countdown title="Time remaining" value={deadline} format="D day, HH:mm:ss" /> : "Read More"}</Link> : <Link to={'blog_single/' + `${props.id}`} className="btn btn-primary btn-style mt-4">Read More</Link>}
                        
                    </div>
                </div>
        </div>
        )
}
export default BlogPostItem;