import React, { useContext, useState } from 'react';
import callApi from '../../utils/apiCaller';
import dateFormat from 'dateformat';
import ListCard from './list_card';
import { NewsPostContext } from '../../context/newspost'
import { Paper } from '@material-ui/core';


export const NewsPosts = (props) => {

    return props.results.map((postItem, index) => {

        return (
            <Paper style={{marginBottom:"30px"}}>
                <ListCard
                    id={postItem.id}
                    key={postItem.id}
                    title={postItem.title}
                    hashTag={postItem.hashtag}
                    category={postItem.category.id}
                    dateCreate={dateFormat(postItem.created_date, "fullDate")}
                    description={postItem.description}
                    image={postItem.image}>

                </ListCard>
            </Paper>)
    });

}

export const GetNewsAllUser = async (nav_link, change) => {
    let contextNewAll = useContext(NewsPostContext)
    let p = null
    console.log("GetNewsAllUser:nav_link: " + nav_link)
    if (nav_link === 'all') {

        p = await callApi('api/newspost/user/?ordering=-created_date', 'GET', null, null)
    }

    if (nav_link === 'auction') {
        p = await callApi('api/newspost/user/?category=1', 'GET', null, null)
    }

    if (nav_link === 'noauction') {
        p = await callApi('api/newspost/user/?category=2', 'GET', null, null)
    }
    if (nav_link === 'eventavailable') {
        p = await callApi('api/newspost/user/?browser=1', 'GET', null, null)
    }
    if (nav_link === 'eventbusy') {
        p = await callApi('api/newspost/user/?browser=0', 'GET', null, null)
    }
    contextNewAll.result = p.data.results
    // console.log('GetNewsAllUser:', contextNewAll)
    change()
}




export const NewsPostAllUser = (props) => {
    // state vs props thay đổi thì render lại
    let contextNewAll = useContext(NewsPostContext)
    let [navLinkCurrent, setNavLinkCurrent] = useState('')
    console.log("NewsPostAllUser:nav_link: " + props.nav_link)
    const get_post = () => {
        setNavLinkCurrent(props.nav_link)
    }

    if (navLinkCurrent !== props.nav_link) {
        GetNewsAllUser(props.nav_link, get_post)

    }

    return (
        <NewsPosts results={contextNewAll.result} />
    )
}
