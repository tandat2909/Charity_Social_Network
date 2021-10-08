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
import { Alert, Button, Statistic } from 'antd';
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
    const [loadAlert, setLoadAlert] = useState(false);
    const [auction, setAuction] = useState({
        offer: ""
    });
    const [price, setPrice] = useState({
        price: ""
    });

    const [selectedValue, setSelectedValue] = React.useState();

  const handleChangeRadio = (event) => {
    console.log(event)
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
        setPrice({
            ...price,
            [name]: value,
        })
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
            }).catch(err => {console.log(err.response)})
        }
        else {
            history.replace("/login")
        }
        
        // setShowButton(true)
        setLoadAlert(true)
        setIsModalVisible(false);
    }

    const patchAuction = async () => {
        // setBlocked(false)
        let au = { ...auction }
        let url = 'api/newspost/' + props.id.match.params.id + '/offer/'
        let a = await callApi(url, 'PATCH', au, null).then(res => {
            if (res.status === 200 || res.status === 201)
                alert("bạn đã sửa giá thành công")
        })
       
        // showOfferAgaint()
        // console.log("auction: ", url)
        setIsModalVisible(false);
        
        
    }
    const deleteAuction = async () => {

        let url = 'api/historyauction/' + detailPost.detail.historyauction[0].id + '/'
        let a = await callApi(url, 'DELETE', null, null).then(res => {
            if (res.status === 204)
                alert("bạn đã xóa giá thành công")
        })
        
        // console.log("auction: ", url)
        setLoadAlert(false)
        setIsModalVisible(false);
        
    }

    const setAuctionWinner = async() => {
        if(selectedValue === undefined){
            alert("bạn cần chọn người chiến thắng")
        }
        else{
            let winner = {"history_auction" : parseInt(selectedValue)}
            let url = 'api/newspost/' + props.id.match.params.id + '/set_auctioneer_winning/'
            let a = await callApi(url, 'PATCH', winner, null).then(res => {
                if (res.status === 200 || res.status === 201)
                    alert("bạn đã thiết lập người chiến thắng thành công")
            })
        }
    }

    const showHistory = () => 
        detailPost.detail.historyauction && detailPost.detail.historyauction.map((postItem) => {

            return(
                
                    <ListItem dense button key={"itemHistory"+postItem.id} >
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
                                checked ={parseInt(selectedValue) === postItem.id}
                                onChange={handleChangeRadio}
                                value={postItem.id}
                                name="history_auction"
                                inputProps={{ 'aria-label': postItem.id }}
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                
            )
            })

    const showOfferAgaint = () => {
        return(
            <Alert message="Bạn đã offer cho bài viết này với giá " type="info" showIcon style={{margin: 5}} closable
                action={
                    <Button size="small" type="primary" onClick={() => {setShowButton(true); setIsModalVisible(true)}}>
                        Offer Againt
                    </Button>
                }/> 
        )    
    }
    console.log("profile: ", context.dataProfile)
    console.log("bai: ", detailPost.detail)
    return (
        <>
            <InnerBanner title="Auction"></InnerBanner>
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
                                            <p style={{ color: "black", fontSize: "1.3em" }}>{detailPost.detail.info_auction.price_start} VNĐ</p>
                                            <p style={{ color: "black" }}>{dateFormat(detailPost.detail.info_auction.start_datetime, "dd-mm-yyyy  HH:MM:ss")} </p>
                                            <p style={{ color: "black" }}>{dateFormat(detailPost.detail.info_auction.end_datetime, "dd-mm-yyyy  HH:MM:ss")} </p>
                                            <p style={{ color: "black" }}>{`${detailPost.detail.user.last_name}` + ' ' + `${detailPost.detail.user.first_name}`}  </p>
                                            {detailPost.detail.historyauction.length > 0 ? <p style={{ color: "black" }}>{detailPost.detail.historyauction.length}  people</p> : ""}
                                            <p style={{ color: "black" }}><Countdown value={new Date(detailPost.detail.info_auction.end_datetime).getTime()} format="D day, HH:mm:ss" valueStyle={{ color: '#ef0d18' }} /></p>

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
                        {detailPost.detail.historyauction.length > 0  || loadAlert === true ? 
                            <Alert message={'Bạn đã offer cho bài viết này với giá '  }type="info" showIcon style={{margin: 5}} closable
                                action={
                                    <Button size="small" type="primary" onClick={() => {setShowButton(true); setIsModalVisible(true)}}>
                                        Offer Againt
                                    </Button>
                                }/>  : ""}

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
                                    <button className="btn btn-style btn-primary" onClick={patchAuction} style={{ textAlign: "right", margin: "0 10px", backgroundColor: "green", borderColor: "#298627", display: "flex" }}><Edit /> Edit</button>
                                    <button className="btn btn-style btn-primary" onClick={deleteAuction} style={{ textAlign: "right", margin: "0 10px", backgroundColor: "red", borderColor: "#f50426", display: "flex" }}><DeleteForever /> Delete</button></> : ""}
                            </Paper> : ""}
                            {detailPost.detail.historyauction.length > 0 && context.dataProfile.id === detailPost.detail.user.id
                             ? <Paper className={classes.paper} elevation={3}>
                                <List subheader={<ListSubheader><h3>History Auction</h3></ListSubheader>} className={list.root} style={{height: "200px", overflowY: "scroll",  margin: "30px auto"}}>
                                    {showHistory()}
                                </List>
                                <button className="btn btn-style btn-primary" style={{ margin: "15px auto"}} onClick={setAuctionWinner}>Submit</button></Paper>
                                 : ""}
                        </Grid>
                    </Grid> : ""}
                </>
    )

}
            export default AuctionDetail;