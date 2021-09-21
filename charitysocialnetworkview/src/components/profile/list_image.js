
import React, {useContext, useState} from 'react';
import {  ImageList, ImageListItem,  ListSubheader, 
}from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";
import { contexts } from "../../context/context"
import callApi from '../../utils/apiCaller';


const useStyles = makeStyles((theme) => ({
    root: {
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'space-around',
      overflow: 'hidden',
      backgroundColor: theme.palette.background.paper,
    },
    imageList: {
      width: 500,
      height: 450,
    },
  }));


const ListImage = () => {
    
    let context = useContext(contexts)
    const [reload, setReload] = useState(false);
    const classes = useStyles();
    const getListImage = async() => {
        let url = 'api/newspost/get-all-image-post-user/' + context.dataProfile.id + '/'
        let a = await callApi(url, 'GET', null, null)
        context.imagePost = a.data.results
        console.log("list img: ", context.imagePost)
        setReload(true)
    }
    if(context.imagePost.length === 0)
     getListImage()
    return (
        <div className={classes.root}>
          <ImageList rowHeight={160} className={classes.imageList} cols={3}>
            <ImageListItem key="Subheader" cols={1} style={{ height: 'auto' }}>
                <ListSubheader component="div">Image</ListSubheader>
            </ImageListItem>
            <ImageListItem key="Subheader" cols={2} style={{ height: 'auto' }}>
                <ListSubheader component="div">All</ListSubheader>
            </ImageListItem>
            { context.imagePost.length >0 && context.imagePost.map((item) => 
              <ImageListItem key={item.id} cols={1} >
                    <img src={item.image} alt={item.image}/>
              </ImageListItem>
            )
             }
          </ImageList>
        </div>
      );
}
export default ListImage;