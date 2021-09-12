
import React from 'react';
import {  ImageList, ImageListItem, ImageListItemBar, ListSubheader, IconButton, 
}from "@material-ui/core";
import { Info }from '@material-ui/icons';
import { makeStyles } from "@material-ui/core/styles";


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1
    },
    imageRoot: {
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
    icon: {
        color: 'rgba(255, 255, 255, 0.54)',
    },

}));


const ListImage = (props) => {
    const classes = useStyles();
    const itemData = [
        {
            img: 'https://lavenderstudio.com.vn/wp-content/uploads/2017/03/chup-san-pham.jpg',
            title: 'Image',
            author: 'author',
        },
        {
            img: 'https://lavenderstudio.com.vn/wp-content/uploads/2017/03/chup-san-pham.jpg',
            title: 'Image',
            author: 'author',
        },
        {
            img: 'https://lavenderstudio.com.vn/wp-content/uploads/2017/03/chup-san-pham.jpg',
            title: 'Image',
            author: 'author',
        },
        {
            img: 'https://lavenderstudio.com.vn/wp-content/uploads/2017/03/chup-san-pham.jpg',
            title: 'Image',
            author: 'author',
        },
        {
            img: 'https://lavenderstudio.com.vn/wp-content/uploads/2017/03/chup-san-pham.jpg',
            title: 'Image',
            author: 'author',
        },
        {
            img: 'https://lavenderstudio.com.vn/wp-content/uploads/2017/03/chup-san-pham.jpg',
            title: 'Image',
            author: 'author',
        },

    ];
    return (
        <div className={classes.imageRoot}>
            <ImageList rowHeight={180} className={classes.imageList}>
                <ImageListItem key="Subheader" cols={2} style={{ height: 'auto' }}>
                    <ListSubheader component="div">Image</ListSubheader>
                </ImageListItem>
                {itemData.map((item,index) => (
                    <ImageListItem key={index}>
                        <img src={item.img} alt={item.title} />
                        <ImageListItemBar
                            title={item.title}
                            subtitle={'by: '+item.author}
                            // subtitle={<span>by: {item.author}</span>}
                            actionIcon={
                                <IconButton aria-label={`info about ${item.title}`} className={classes.icon}>
                                    <Info />
                                </IconButton>
                            }
                        />
                    </ImageListItem>
                ))}
            </ImageList>
        </div>
    )
}
export default ListImage;