import React, { useContext, useEffect, useState } from 'react';
import { Paper, Avatar } from '@mui/material';
import Grid from '@mui/material/Grid';
import { makeStyles } from '@material-ui/core/styles';
import { contexts } from '../../context/context'
import callApi from '../../utils/apiCaller';
import { List,  Button, Skeleton } from 'antd';


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
}));


const Notification = () => {
    const count = 3;
    let [page, setPage] = useState({
        number: 1,
        next: true
    })
    let [loading, setLoading] = useState({
        initLoading: true,
        loading: false,
        data: [],
        list: [],
    })
   
    const getData = async (pages) => {
        let url = 'api/accounts/notification/?page=' + pages + '&page_size=' + count
        let b = await callApi(url, 'GET', null, null)
        return b
    }
    const classes = useStyles();
    // let dataMess = useContext(contexts)
    // const data = dataMess.dataNotification.results

    useEffect(() => {
        if(loading.initLoading === true){
            getData(page.number).then(res => {
                setLoading({
                    initLoading: false,
                    data: res.data.results,
                    list: res.data.results,
                })
            })
        }
        


    }, [loading])

    const onLoadMore = () => {
    
        if(page.next === true){
            setLoading({
                ...loading, 
                loading: false,
                list : loading.data.concat([...new Array(count)].map(() => ({ loading: true, name: {} })))
            })
            getData(page.number + 1).then(res => {
                const data = loading.data.concat(res.data.results);
                  setLoading(
                    {
                        ...loading,
                        data: data,
                        list: data,
                        loading: false,
                    },
                    () => {
                        window.dispatchEvent(new Event('resize'));
                    },
                );
                
                if(res.data.next !== null){
                     setPage({
                        number: ++page.number,
                            next:true
                        })
                        return
                }
                setPage({...page,
                    next: false
                    })
            })
              
      
        }
    
   
    };



    // const { initLoading, loading, list } = this.state;
    const loadMore =
        !loading.initLoading && !loading.loading ? (
            <div
                style={{
                    textAlign: 'center',
                    marginTop: 12,
                    height: 32,
                    lineHeight: '32px',
                }}
            >
                <Button onClick={onLoadMore}>loading more</Button>
            </div>
        ) : null;
    return (
        <Grid item xs={10} className="container pb-lg-4" style={{ margin: "100px auto" }}>
            <Paper className={classes.paper}>
                <List
                    className="demo-loadmore-list"
                    loading={loading.initLoading}
                    size="large"
                    header={<p class="title-big">Notification</p>}
                    itemLayout="horizontal"
                    loadMore={loadMore}
                    dataSource={loading.list}
                    renderItem={item => (
                        <List.Item
                            actions={[<a key="list-loadmore-edit">edit</a>, <a key="list-loadmore-more">more</a>]}
                        >
                            <Skeleton avatar title={false} loading={item.loading} active>
                                <List.Item.Meta
                                    avatar={<Avatar sx={{ width: 80, height: 80, paddingBottom: "1.1em" }} src="https://banner2.cleanpng.com/20190305/xui/kisspng-megaphone-microphone-portable-network-graphics-com-ferret-video-5c7ec1edbc58f1.6366504315518110537715.jpg" />}
                                    title={<p style={{ fontWeight: "700" }}>{item.title}</p>}
                                    description={<p style={{ fontSize: "16px" }}>{item.message}</p>}
                                />
                                
                            </Skeleton>
                        </List.Item>
                    )}
                />
                
            </Paper>
        </Grid>
    )

}
export default Notification;
