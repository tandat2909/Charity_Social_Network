import React, { useContext, useEffect, useState } from 'react';
import { List, Card } from 'antd';
import Grid from '@mui/material/Grid';
import { makeStyles } from '@material-ui/core/styles';
import { Paper } from '@mui/material';
import { AccountBalanceWallet, Storefront, CheckCircle } from '@material-ui/icons';
import { Link } from 'react-router-dom';
import Checkbox from '@mui/material/Checkbox';
import { recerpt } from '../../context/recerpt';
import callApi from '../../utils/apiCaller';
import dateFormat from 'dateformat';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'left',
        color: theme.palette.text.secondary,
        margin: 15
    },
    complete: {
        backgroundColor: "#ff9800"
    },
    uncomplete: {
        backgroundColor: "green"
    }
}));

const List_Recerpt = () => {
    let [color, setColor] = useState()
    let list = useContext(recerpt)
    const label = { inputProps: { 'aria-label': 'Checkbox demo' } };
    const classes = useStyles();
    const listData = [];
    for (let i = 0; i < 3; i++) {
        listData.push({
            href: 'https://ant.design',
            title: `tên đấu giá ${i}`,
            description:
                'tên đấu giá',
            content:
                'tiền',
        });
    }

    const getListOrder = async () => {
        let a = await callApi("api/auction/order/", 'GET', null, null)
        list.listRecerpt = a.data
    }
    if (list.listRecerpt.length === 0)
        getListOrder()


    return (

        <Grid item xs={10} className="container pb-lg-4" style={{ margin: "100px auto" }}>
            <Paper className={classes.paper} elevation={3}>
                <List
                    itemLayout="vertical"
                    size="large"
                    dataSource={list.listRecerpt}
                    footer={
                        <div className="submit text-right">
                            <Link to="/" className="btn btn-primary btn-style mt-4">
                                <AccountBalanceWallet />Pay </Link>
                        </div>
                    }

                    renderItem={item => (
                        <List.Item
                            key={item.id}
                        >
                            <Link to={'recerpt/' + `${item.id}`} >
                                {item.transaction === null ?
                                    <Card
                                        headStyle={{ backgroundColor: "#ff9800" }}
                                        bordered={true}
                                        hoverable={true}
                                        title={
                                            <>
                                            <div style={{ display: "flex" }}>
                                                {item.transaction !== null ? <CheckCircle style={{ margin: "12px 0", backgroundColor: "yellow"}} /> :
                                                    <Checkbox edge="start"
                                                        {...label}
                                                        value="{postItem.id}"
                                                        name="history_auction"
                                                        inputProps={{ 'aria-label': 'controlled' }}
                                                    />}
                                                <p style={{ padding: "10px 0", fontSize: "20px", color: "black" }}><Storefront />NhuQuynh@123</p>
                                            </div>
                                             {item.transaction !== null ? <p style={{ padding: "10px 0" }}>{item.transaction.status}</p> : ""}
                                            </>
                                        }
                                    >
                                        <List.Item.Meta

                                            avatar={
                                                <img
                                                    width={150}
                                                    alt="logo"
                                                    src={item.image}
                                                />
                                            }
                                            title={<a href={item.item} style={{ color: "#ff9800", fontSize: "20px" }}>{item.item}</a>}
                                            description={<div>
                                                <p>Chiến thắng với giá: {item.price}</p>
                                                <p>thời gian chiến thắng: {dateFormat(item.time_win, "yyyy-mm-dd HH:mm:ss")}</p>
                                                <p>thời gian đấu giá: {dateFormat(item.time_offer, "yyyy-mm-dd HH:mm:ss")}</p>
                                            </div>}
                                        />
                                    </Card> 
                                    :
                                    <Card
                                        headStyle={{ backgroundColor: "green" }}
                                        bordered={true}
                                        hoverable={true}
                                        title={
                                            <div style={{ display: "flex" }}>
                                                <div style={{ display: "flex" }}>
                                                    {item.transaction !== null ? <CheckCircle  style={{ margin: "12px 0" , color: "yellow"}} /> :
                                                        <Checkbox edge="start"
                                                            {...label}
                                                            value="{postItem.id}"
                                                            name="history_auction"
                                                            inputProps={{ 'aria-label': 'controlled' }}
                                                        />}
                                                    <p style={{ padding: "10px 0", fontSize: "20px", color: "black" }}><Storefront />NhuQuynh@123</p>
                                                    
                                                </div>
                                                <div style={{position: "absolute", right: "5px"}}>{item.transaction !== null ? <p style={{ padding: "10px 10px", color: "yellow"}}>{item.transaction.status} !</p> : ""}</div>
                                            </div>
                                        }
                                    >
                                        <List.Item.Meta

                                            avatar={
                                                <img
                                                    width={150}
                                                    alt="logo"
                                                    src={item.image}
                                                />
                                            }
                                            title={<a href={item.item} style={{ color: "#ff9800", fontSize: "20px" }}>{item.item}</a>}
                                            description={<div>
                                                <p>Chiến thắng với giá: {item.price}</p>
                                                <p>thời gian chiến thắng: {dateFormat(item.time_win, "yyyy-mm-dd HH:mm:ss")}</p>
                                                <p>thời gian đấu giá: {dateFormat(item.time_offer, "yyyy-mm-dd HH:mm:ss")}</p>
                                            </div>}
                                        />
                                    </Card>
                                }
                            </Link>
                        </List.Item>
                    )}
                />

            </Paper>
        </Grid>
    )
}
export default List_Recerpt;
