
import React, { useState, useContext} from 'react';
import BannerImage from '../banner/banner-bottom-shape';
import {Paper, Grid}from "@material-ui/core";
import './../../css/profile_style.css'
import { contexts } from "../../context/context"
import ListProfile from './list_profile';
import ListImage from './list_image';
import PostCard from './post_card';
import UpdateProfile from './update_profile';
import MenuCategory from '../menu/menu_newspost';
import {NewsPostAllUser} from './render_post'
import {NewsPostContext} from '../../context/newspost'
import AvatarImg from './upload_avatar';
import Avatars from './avatar';




//main
const Profile = () => {
    let context = useContext(contexts)
    // let [status, setstatus] = useState(false)
    // let listProfile = useMemo(({context}) => <ListProfile />,[context])
    let [nav_link,setNav_link]= useState('all')
    
    let contextNewAll = useContext(NewsPostContext)
    // let [action,setAction] = useState(true)
    let [profile, setProfile] = useState(context.dataProfile)
   

    let renderProfile = () => {
        setProfile(context.dataProfile)
        // console.log("má m đạt")
        // setAction(!action)       
    }

    let handlerOnClickMenu =(id)=>{
        contextNewAll.result = []
        console.log("handlerOnClickMenu: " + id)
        setNav_link(id)

    }
  

    // useEffect(() => {
    //     // let myheader = new Headers();
    //     // myheader.append("Content-Type", "application/json")
    //     // console.log(myheader)
    //     // let a = await callApi('api/accounts/profile/', 'GET', null, null)
    //     // context.dataProfile = a.data
        
    //     getProfile()
        
      
    // }, [status])


  
    return (
        <>

            <div>
            
            <div className="inner-banner">
                <section className="w3l-breadcrumb py-5">
                    <div className="container py-lg-5 py-md-3">
                        <div style={{ textAlign: 'center' }}>
                            
                            <Avatars></Avatars>

                            {/* <img src={context.dataProfile.avatar} alt=""
                                style={{ width: "200px", height: "200px", borderRadius: '50%', border: ' 5px solid white' }} /> */}
                            <h4 style={{ color: 'white' }}>{context.dataProfile.nick_name}</h4>
                            {/* <AvatarImg></AvatarImg> */}
                        </div>
                    </div>
                </section>
            </div>
            <BannerImage></BannerImage>
            <div className={ " container"} >
                <Grid container style={{ padding: '30px' }} spacing={3}>
                    <Grid item xs={12} sm={4} >
                        <Paper style={{marginBottom:"30px"}} >
                            <div style={{display: "flex", justifyContent: "space-between", padding: "10px 10px"}}>
                                <h4 style={{ textAlign: 'center', padding: '10px' }}>Thông tin</h4>
                                <UpdateProfile update={renderProfile}></UpdateProfile>
                            </div>
                            
                            {/* {listProfile(status)} */}
                            <ListProfile action= {true} profile={profile}></ListProfile>
                            
                        </Paper>
                        <Paper>
                            <ListImage></ListImage>
                        </Paper>
                    </Grid>
                    <Grid item xs={12} sm={8} >
                        <Paper  style={{marginBottom:"20px"}}>
                            <MenuCategory onClickMenu  = {handlerOnClickMenu}></MenuCategory>
                        </Paper>
                        <Paper  style={{marginBottom:"20px"}}>
                            <PostCard></PostCard>
                        </Paper>
                        
                           <NewsPostAllUser nav_link = {nav_link}/>
                            
                        
                    </Grid>

                    </Grid>
            </div>
            </div>
            
        </>
            )

}

export default Profile