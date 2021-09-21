import React, {useContext, useState}  from 'react';
import { makeStyles } from "@material-ui/core/styles";
import {ThumbUp}
from '@material-ui/icons';
import {SpeedDial, SpeedDialAction} from "@material-ui/lab";
import { ListEmotion } from '../../context/emotion';
import {Avatar, IconButton} from '@material-ui/core';
import axios from 'axios';
import "../../css/style-emotions.css"

const useStyleEmoji = makeStyles((theme) => ({
    root: {
        transform: "translateZ(0px)",
        flexGrow: 1
    },
    exampleWrapper: {
       
        // marginTop: theme.spacing(3),

    },

    speedDial: {
        // position: "absolute",
        // color: "red",
        alignItems: "normal",
       
        // ' > button': {
        //     boxShadow:"none",
        //     backgroundColor: '#ffffff00'
        //   },
        // button:{
        //     boxShadow:"none",
        //     backgroundColor: 'red',
            
        // }
       
    },
    
    
}));






const ListEmoji = () => {
    // let a = new Array()
    const classes = useStyleEmoji();

    const [open, setOpen] = React.useState(false);
    let [get_emotion_success, setGetEmotionSuccess] = useState(false)

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
    };
    let listEmotion = useContext(ListEmotion)
    const getListEmotion = async () => {
        let a = await axios({
            method: "GET",
            url: 'http://127.0.0.1:8000/api/emotions/'
        }).catch(err => { console.log(err) })
        console.log(a)
        listEmotion.list = a.data
        setGetEmotionSuccess(true)
    }
    if (Object.keys(listEmotion.list).length === 0){
        getListEmotion()
    }
    
   
    return (
        <div className={classes.root}>
            <div className={classes.exampleWrapper + " emotions" }>
                <SpeedDial
                    
                    ariaLabel="SpeedDial example"
                    className={classes.speedDial }
                    icon={<IconButton aria-label="share">
                    <ThumbUp /> &nbsp; Like
                </IconButton>  }
                    onClose={handleClose}
                    onOpen={handleOpen}
                    open={open}
                    tooltipplacement="top"
                    tooltipopen="top-start"
                >
                    {listEmotion.list.map((action) => (
                        
                        <SpeedDialAction
                            key={action.name}
                            icon={<Avatar src={action.image} />}
                            tooltipTitle={action.name}
                            onClick={handleClose}
                        ></SpeedDialAction>
                    ))}
                </SpeedDial>
               
            </div>
         </div>
    )
}
export default ListEmoji;