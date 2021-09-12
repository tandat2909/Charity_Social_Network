import React, { useContext, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Paper, Grid, TextField, List, ListItem, ListItemAvatar, Avatar, ListItemText, Tooltip, ListSubheader, Radio,
    ListItemSecondaryAction} 
from '@material-ui/core';
import InnerBanner from '../banner/inner_banner';
import BannerImage from '../banner/banner-bottom-shape';
import { NewsPostContextMod } from '../../context/newspost_mod'
import callApi from '../../utils/apiCaller'
import dateFormat from 'dateformat';
import { Statistic } from 'antd';
import { contexts } from '../../context/context'
import { useHistory } from "react-router-dom";
import { Gavel, DeleteForever, Edit } from '@material-ui/icons';
import { withStyles } from '@material-ui/core/styles';
import { green } from '@material-ui/core/colors';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        margin: 15
    },
}));

const useList = makeStyles((theme) => ({
    root: {
        width: '80%',
        margin: "0 auto",
        backgroundColor: theme.palette.background.paper,
    },
}));

const GreenRadio = withStyles({
    root: {
      color: green[400],
      '&$checked': {
        color: green[600],
      },
    },
    checked: {},
  })((props) => <Radio color="default" {...props} />);

const AuctionDetail = (props) => {
    const classes = useStyles();
    const list = useList();
    let detailPost = useContext(NewsPostContextMod)
    let context = useContext(contexts)
    let history = useHistory()

    let [get_post_success, setGetPostSuccess] = useState(false)
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isShowButton, setShowButton] = useState(false);
    const [isBlocked, setBlocked] = useState(false);
    const [auction, setAuction] = useState({
        offer: ""
    });

    const [selectedValue, setSelectedValue] = React.useState('a');

  const handleChangeRadio = (event) => {
    setSelectedValue(event.target.value);
  };
    const { Countdown } = Statistic;
    // let url = 'http://localhost:8000/api/newspost/' + props.id.match.params.id + '/'
    const GetDetailPost = async () => {
        let url = 'api/newspost/' + props.id.match.params.id + '/'
        // console.log(url)
        let a = await callApi(url, 'GET', null, null).catch(err => { console.log(err) })
        console.log(a)
        detailPost.detail = a.data
        setGetPostSuccess(true)
    }

    if (Object.keys(detailPost.detail).length === 0 || detailPost.detail.id !== props.id.match.params.id) {
        GetDetailPost()
        //setGetPostSuccess(false)
    }

    const handleChange = (event) => {
        const target = event.target;
        const { name, value } = target;
        setAuction({
            ...auction,
            [name]: value,
        });
    }

    const showOffer = () => {
        setIsModalVisible(true);
    };
    const postAuction = async () => {

        if (context.authorization) {
            let au = { ...auction }
            let url = 'api/newspost/' + props.id.match.params.id + '/offer/'
            let a = await callApi(url, 'PATCH', au, null).then(res => {
                if (res.status === 200 || res.status === 201)
                    alert("bạn đã đấu giá thành công")
            })
        }
        else {
            history.replace("/login")
        }
        // console.log("auction: ", url)
        setShowButton(true)
        setBlocked(true)
    }

    const patchAuction = async () => {

        // if (context.authorization) {
        //     let au = { ...auction }
        //     let url = 'api/newspost/' + props.id.match.params.id + '/offer/'
        //     let a = await callApi(url, 'PATCH', au, null).then(res => {
        //         if (res.status === 200 || res.status === 201)
        //             alert("bạn đã đấu giá thành công")
        //     })
        // }
        // else {
        //     history.replace("/login")
        // }
        // // console.log("auction: ", url)
        // setShowButton(true)
        setBlocked(false)
    }

    const showHistory = () => 
        detailPost.detail.historyauction && detailPost.detail.historyauction.map((postItem) => {
            return(
                
                    <ListItem dense button>
                        <ListItemAvatar>
                            <Tooltip title={`${postItem.user.last_name}` + ' ' + `${postItem.user.first_name}`} arrow placement="top">
                                <Avatar src={postItem.user.avatar}>
                                </Avatar>
                                </Tooltip>
                        </ListItemAvatar>
                        <ListItemText primary={postItem.user.username} secondary="Jan 9, 2014" />
                        <ListItemText primary={postItem.price} />
                        <ListItemSecondaryAction>
                            <GreenRadio  edge="end"
                            checked={selectedValue === 'c'}
                            onChange={handleChangeRadio}
                            value={postItem.id}
                            name="radio-button-demo"
                            inputProps={{ 'aria-label': 'C' }}
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                
            )
            })

    return (
        <>
            <InnerBanner></InnerBanner>
            <BannerImage></BannerImage>
            {Object.keys(detailPost.detail).length !== 0 ?
                <Grid container>

                    <Grid className="container pb-lg-4" style={{ margin: "50px auto" }}>

                        <Paper className={classes.paper}  >
                            <h4>{detailPost.detail.title}</h4>
                            <div style={{ display: "flex" }}>
                                <Grid item sm={4} xs={12} style={{ margin: "30px 10px" }}>
                                    <Paper className={classes.paper}>
                                        <div style={{ width: "100%" }}>
                                            <img src={detailPost.detail.image} style={{ width: "100%" }} />
                                        </div>
                                    </Paper>
                                </Grid>
                                <Grid item sm={6} xs={12} style={{ margin: "30px 20px" }}>
                                    <div style={{ display: "flex" }}>

                                        <Grid item sm={6} xs={12} style={{ textAlign: "left" }}>
                                            <p>Price start: </p>
                                            <p>Start datetime: </p>
                                            <p>End datetime: </p>
                                            <p>Author: </p>
                                            {detailPost.detail.historyauction.length > 0 ? <p>Number of people who bid: </p>: ""}
                                            <p style={{ margin: "5px 0" }}>Time remaining: </p>
                                        </Grid>
                                        <Grid item sm={6} xs={12} style={{ textAlign: "left" }}>
                                            <p style={{ color: "black", fontSize: "1.3em" }}>{detailPost.detail.info_auction[0].price_start} VNĐ</p>
                                            <p style={{ color: "black" }}>{dateFormat(detailPost.detail.info_auction[0].start_datetime, "dd-mm-yyyy  HH:MM:ss")} </p>
                                            <p style={{ color: "black" }}>{dateFormat(detailPost.detail.info_auction[0].end_datetime, "dd-mm-yyyy  HH:MM:ss")} </p>
                                            <p style={{ color: "black" }}>{`${detailPost.detail.user.last_name}` + ' ' + `${detailPost.detail.user.first_name}`}  </p>
                                            {detailPost.detail.historyauction.length > 0 ? <p style={{ color: "black" }}>{detailPost.detail.historyauction.length}  people</p> : ""}
                                            <p style={{ color: "black" }}><Countdown value={new Date(detailPost.detail.info_auction[0].end_datetime).getTime()} format="D day, HH:mm:ss" valueStyle={{ color: '#ef0d18' }} /></p>

                                        </Grid>

                                    </div>
                                    <Grid item sm={12} xs={12} style={{ textAlign: "justify" }}>
                                        <p
                                            style={{
                                                whiteSpace: "pre-wrap",
                                                textOverflow: "ellipsis",
                                                overflow: "hidden",
                                                WebkitLineClamp: "3",
                                                WebkitBoxOrient: "vertical",
                                                width: "100%",
                                                display: "block",
                                                display: "-webkit-box",
                                                height: "16px*1.3*3",
                                                textAlign: "justify"
                                            }}
                                        >Description: <span style={{ fontStyle: "italic", color: "#655858b5" }}>{detailPost.detail.description}</span></p>
                                    </Grid>

                                    <button className="btn btn-style btn-primary" style={{ textAlign: "right", margin: "15px 0" }} onClick={showOffer}><Gavel /> Auction</button>
                                </Grid>

                            </div>
                        </Paper>
                        {isModalVisible === true ?
                            <Paper className={classes.paper} style={{ display: "flex" }} >
                                <TextField
                                    required
                                    disabled={isBlocked}
                                    border="1px solid red"
                                    id="outlined-required"
                                    label="Offer"
                                    variant="outlined"
                                    fullWidth={true}
                                    name="offer"
                                    onChange={handleChange}
                                // error={errors.title}
                                // helperText={errors.title ? errors.title : null}
                                />
                                {isShowButton === true ? "" : <button className="btn btn-style btn-primary" style={{ textAlign: "right", margin: "0 10px" }} onClick={postAuction}>Submit</button>}
                                {isShowButton === true ? <>
                                    <button className="btn btn-style btn-primary" onClick={patchAuction} style={{ textAlign: "right", margin: "0 10px", backgroundColor: "green", borderColor: "#298627" }}><Edit /> Edit</button>
                                    <button className="btn btn-style btn-primary" style={{ textAlign: "right", margin: "0 10px", backgroundColor: "red", borderColor: "#f50426" }}><DeleteForever /> Delete</button></> : ""}
                            </Paper> : ""}
                            {detailPost.detail.historyauction.length > 0 ? 
                                <List subheader={<ListSubheader>History Auction</ListSubheader>} className={list.root} style={{height: "200px", overflowY: "scroll"}}>
                                    {showHistory()}
                                </List>
                                 : ""}
                        </Grid>
                    </Grid> : ""}
                </>
    )

}
            export default AuctionDetail;