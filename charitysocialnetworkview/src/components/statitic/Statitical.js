import React, {useContext} from 'react';
import DoughnutChart from './DoughnutChart';
import GroupedBar from './GroupedBar';
import Polar from './Polar';
import Crazy from './Carzy';
import { makeStyles } from '@material-ui/core/styles';
import {Paper, Grid, Avatar} from '@material-ui/core';
import {EventBusy, EventNote, Gavel, EventAvailable} from '@material-ui/icons';
import callApi from '../../utils/apiCaller';
import moment from 'moment';
import { statistical } from '../../context/statistical';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        
    },
    large: {
        width: theme.spacing(7),
        height: theme.spacing(7),
        margin: "0 auto"
      },
    tong: {
        margin: "10px auto"
    }
}));


const Statitical = () => {
    const classes = useStyles();
    let thong = useContext(statistical);
    const totalStaticial = async() => {
        let year = moment().format('YYYY')
        let url = "api/statistical/post/"+ year + "/"
        let au =  await callApi(url, 'GET', null, null)
        // const noAuction = await callApi("api/newspost/user/?category=2", 'GET', null, null)
       thong.total = au.data
    }
    totalStaticial()

    const category = () =>{
        thong.total && thong.total.filter(d => d.category.id === 1 ).map(res => {
            thong.auction = res
        })
        thong.total && thong.total.filter(d => d.category.id === 2 ).map(res => {
            thong.noAuction = res
        })
    }
        category()
    return (
        <>
            <Paper className="container" style={{marginTop: "150px"}}>
                <Grid container spacing={3}>
                    <Grid item xs={6} sm={3}>
                        <Paper className={classes.paper} elevation={3} style={{margin: "30px auto", borderRadius: "10%", backgroundColor: "#67caca"}}>
                            <div style={{margin: "20px auto"}}>
                                <div className={classes.tong}>
                                    <Avatar className={classes.large} style={{backgroundColor: "#2d9898"}}><Gavel /></Avatar>
                                </div>
                                <h2 className={classes.tong}>{thong.auction.total} Bài</h2>
                                <h5 className={classes.tong}>Auction</h5>
                            </div>
                        </Paper>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                    <Paper className={classes.paper} elevation={3} style={{margin: "30px auto", borderRadius: "10%", backgroundColor: "#f5f559"}}>
                            <div style={{margin: "20px auto"}}>
                                <div className={classes.tong}>
                                    <Avatar className={classes.large} style={{backgroundColor: "#e8bd39"}}><EventNote /></Avatar>
                                </div>
                                <h2 className={classes.tong}>{thong.noAuction.total} Bài</h2>
                                <h5 className={classes.tong}>No auction</h5>
                            </div>
                        </Paper>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                    <Paper className={classes.paper} elevation={3} style={{margin: "30px auto", borderRadius: "10%", backgroundColor: "#8bc34a"}}>
                            <div style={{margin: "20px auto"}}>
                                <div className={classes.tong}>
                                    <Avatar className={classes.large} style={{backgroundColor: "#4caf50"}}><EventAvailable /></Avatar>
                                </div>
                                {thong.auction && thong.noAuction ? <h2 className={classes.tong}>{thong.auction.data.emotions.length + thong.noAuction.data.emotions.length} emtions</h2>: ""}
                                
                                <h5 className={classes.tong}>emtions</h5>
                            </div>
                        </Paper>
                    </Grid>
                    <Grid item xs={6} sm={3}>
                    <Paper className={classes.paper} elevation={3} style={{margin: "30px auto", borderRadius: "10%", backgroundColor: "#f4433691"}}>
                            <div style={{margin: "20px auto"}}>
                                <div className={classes.tong}>
                                    <Avatar className={classes.large} style={{backgroundColor: "#e91e6382"}}><EventBusy /></Avatar>
                                </div>
                                {thong.auction && thong.noAuction ? <h2 className={classes.tong}>{thong.auction.data.comment?.length + thong.noAuction.data.comment?.length} comments</h2>: ""}
                                
                                <h5 className={classes.tong}>comments</h5>
                            </div>
                        </Paper>
                    </Grid>
                </Grid>
           
                <Grid container spacing={3}>

                    <Grid item xs={12} sm={8}>
                        <Paper className={classes.paper}><GroupedBar ></GroupedBar></Paper>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <Paper className={classes.paper}><DoughnutChart></DoughnutChart></Paper>
                    </Grid>
                </Grid>
                <Grid container spacing={3}>

                    <Grid item xs={12} sm={7}>
                        <Paper className={classes.paper}><Crazy></Crazy></Paper>
                    </Grid>
                    <Grid item xs={12} sm={5}>
                        <Paper className={classes.paper}><Polar></Polar></Paper>
                    </Grid>
                </Grid>

            </Paper>
        </>
    )

}
export default Statitical;