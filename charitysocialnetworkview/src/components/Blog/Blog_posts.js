import React, {  useContext, useState } from 'react';
import InnerBanner from '../banner/inner_banner';
import BlogPostItem from './Blog_post_item';
import Pagination from './pagination';
import BannerImage from '../banner/banner-bottom-shape';
import axios from 'axios';
import {NewsPostContextMod} from '../../context/newspost_mod'




const BlogPost = () => {
    let detailPost = useContext(NewsPostContextMod)
    
    
    const GetPost = async(page = 1) => {
        let a = await axios({
            method: "GET",
            url: "http://localhost:8000/api/newspost/?page=" + page
          }).catch(err => {console.log(err)})
          console.log("page", page)
        detailPost.results = a.data
        // setReloadPage(true)
        setPagination({...pagination,page:page, totalRow: detailPost.results.count, })
        
    }
    let [pagination, setPagination] = useState({
        page: 1,
        limit: 3,
        totalRow: detailPost.results.count,
    })

    if(Object.keys(detailPost.results).length===0){
        GetPost()
    }

    const handlePageChange = (page) =>{
       
        GetPost(page);
        
        // console.log("new page:", get_page)
        
    }
    
    const ShowPost = (props = detailPost.results) => 
        props.results && props.results.map((postItem) => {
              
                return(
                <BlogPostItem 
                    key={postItem.id}
                    id={postItem.id}
                    title={postItem.title}
                    hashTag={postItem.hashtag}
                    category={postItem.category}
                    dateCreate={postItem.created_date}
                    description={postItem.description}
                    image={postItem.image}
                    end_datetime={postItem.category.id === 1 ? postItem.info_auction.end_datetime:undefined
                    }
                                                                     
                    >
                </BlogPostItem>)
            });
    
      
    


    return (

        <div style={{backgroundColor: "#f8f9fa"}}>
            <InnerBanner title="Latest Updates"></InnerBanner>
            <BannerImage></BannerImage>
            <section className="w3l-blogblock py-5">
                <div className="container pt-lg-4 pt-md-3">
                    {ShowPost()}
                    {Object.keys(detailPost.results).length !== 0 ? <Pagination pagination={pagination} onPageChange={handlePageChange}></Pagination> : ""}
                    
                </div>
            </section>
        </div>
        
    );
        
    
    
}
export default BlogPost;