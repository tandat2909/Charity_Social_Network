
import React, { useContext } from 'react';
import { makeStyles } from "@material-ui/core/styles";
import {
    TextField, Typography, CardContent, CardMedia, Avatar, CardHeader, Card, IconButton, Paper
}
    from "@material-ui/core";
import {
    MoreVert, Message, Share,ThumbUp
}
    from '@material-ui/icons';
import ListEmoji from './list_emoji'
import { contexts } from "../../context/context"




const useStylesCard = makeStyles((theme) => ({
    
    media: {
        height: 0,
        paddingTop: '56.25%', // 16:9
    },
    expand: {
        transform: 'rotate(0deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    },
    avatar: {
        backgroundColor: 'red[500]',
    },


}));

const ListCard = (props) => {
    const classes = useStylesCard();
    const context = useContext(contexts)
    const hh = ()=>{
        let a= ""
        props.hashTag.forEach(h =>{
            a+= "#" + h.name +" "
        })
        return a
    }
    return (
        <>
            <Card className={classes.Cardroot} >
                <CardHeader
                    avatar={
                        <Avatar src={context.dataProfile.avatar} />
                    }
                    action={
                        <IconButton aria-label="settings">
                            <MoreVert />
                        </IconButton>
                    }
                    title={`${context.dataProfile.first_name}` + " " + `${context.dataProfile.last_name}`}
                    subheader={props.dateCreate}
                />
                <h3>{hh()}</h3>

                <CardMedia
                    className={classes.media}
                    image={props.image}
                    title="Paella dish"
                />
                <CardContent style={{
                    border: "1px solid #80808070",
                    margin: "0 20px 19px",
                    borderRadius: "0px 0px 15px 15px",
                    borderTop: "none",
                }}>
                    <p style={{color: "black"}}>{props.title}</p>
                    <Typography variant="body2" color="textSecondary" component="p">
                        {props.description}
                    </Typography>
                </CardContent>
                
                <CardContent style={{display: "flex", borderTop: "1px solid gray", borderBottom: "1px solid gray"}}>
                        <ListEmoji ></ListEmoji>
                    <IconButton aria-label="share">
                        <Share />Share
                    </IconButton>
                    <IconButton aria-label="comment">
                        <Message />Comment
                    </IconButton>
                </CardContent>

            </Card>
        <div style={{display: "flex", alignItems: "center"}}>
            <img src={context.dataProfile.avatar} alt=""
            style={{ width: "50px", height: "50px", borderRadius: '50%', border: ' 5px solid white' }} />
            <TextField
                id="filled-full-width"
                style={{ margin: 8 }}
                placeholder="Comment"
                label={`${context.dataProfile.first_name}` + " " + `${context.dataProfile.last_name}`}
                helperText="thời gian comment"
                fullWidth={true}
                margin="normal"
                InputLabelProps={{
                    shrink: true,
                }}
                variant="filled"
            />
        </div>
       </>
    )
}

export default ListCard;