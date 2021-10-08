import React, { useContext, useState} from 'react';
import callApi from '../../utils/apiCaller';
import BannerImage from '../banner/banner-bottom-shape';
import InnerBanner from '../banner/inner_banner';
import CausesItem from './causes_item';
import Story from './story';
import {PostOfUserMod} from '../../context/post_userMod'


const CausesPage = () => {
    const post = useContext(PostOfUserMod)
    const [reload, setReload] = useState(false)
    const getPostMod =  async() =>{
        let a = await callApi('api/accounts/is-user-mod/', 'GET', null, null)
        let p = await callApi('api/newspost/list_pending_post/?page_size=6', 'GET', null, null)
        post.isUserMod = a.data.usermod
        post.results = p.data.results
        setReload(true)
    }
    if(Object.keys(post.results).length === 0 ){
        getPostMod()
    }


    const GetListPostMod = () => 
    post.results && post.results.map((postItem) => {
          
            return(
                <CausesItem
                    key={postItem.id}
                    id={postItem.id}
                    title={postItem.title}
                    hashTag={postItem.hashtag}
                    category={postItem.category}
                    dateCreate={postItem.created_date}
                    description={postItem.description}
                    image={postItem.image}
                    end_datetime={postItem.category.id === 1 ? postItem.info_auction.end_datetime:undefined}
            
                >
            </CausesItem>)
        });


        return (
            <>
                <InnerBanner></InnerBanner>
                <BannerImage></BannerImage>
                <div className="w3-services py-5">
                    <div className="container py-lg-4 py-md-3">
                        <div className="row w3-services-grids">
                            {GetListPostMod()}
                            
                        </div>
                    </div>
                </div>
                <Story></Story>
            </>
        )

}
export default CausesPage;