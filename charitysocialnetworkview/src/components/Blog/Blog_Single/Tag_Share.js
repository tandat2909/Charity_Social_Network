import React, { useContext, useState } from 'react';
import { NewsPostContextMod } from '../../../context/newspost_mod'
import { ListEmotion } from '../../../context/emotion';
import axios from 'axios';
import callApi from '../../../utils/apiCaller';
import { Modal, Tabs, Tooltip } from 'antd';
import { contexts } from '../../../context/context'
import { useHistory } from "react-router-dom";
import {Avatar, Badge} from '@material-ui/core';
import AvatarGroup from '@material-ui/lab/AvatarGroup';
import { makeStyles, withStyles } from '@material-ui/core/styles';

const SmallAvatar = withStyles((theme) => ({
    root: {
      width: 30,
      height: 30,
     
    },
  }))(Avatar);

const TagAndShare = () => {
    let hashTag = useContext(NewsPostContextMod)
    let listEmotion = useContext(ListEmotion)
    let context = useContext(contexts)
    let [get_emotion_success, setGetEmotionSuccess] = useState(false)
    let history = useHistory()
    const [isModalVisible, setIsModalVisible] = useState(false);


    const { TabPane } = Tabs;

    const hashTags = (props = hashTag.detail.hashtag) =>
        props && props.map((hashTagItem) => {
            return (
                <a href="#blog-tag">{"#" + `${hashTagItem.name}`}</a>
            )
        })

    const showModal = () => {
        setIsModalVisible(true);
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const getListEmotion = async () => {
        let a = await axios({
            method: "GET",
            url: 'http://127.0.0.1:8000/api/emotions/'
        }).catch(err => { console.log(err) })
        console.log(a)
        listEmotion.list = a.data
        setGetEmotionSuccess(true)
    }

    const postEmotion = async (id) => {
        if (context.authorization) {
            let url = 'api/newspost/' + hashTag.detail.id + '/emotions/?emotion_type=' + id
            let a = await callApi(url, 'PATCH', null, null).then(res => {
                if (res.status === 200 || res.status === 201)
                    alert("bạn thả emotion cho bài viết thành công")
            })
        }
        else {
            history.replace("/login")
        }

    }

    const renderEmotion = (props = listEmotion.list) =>
        props && props.map((emotionItem) => {
            return (

                <Tooltip title={emotionItem.name} placement="top">
                    <Avatar  src={emotionItem.image} onClick={() => { postEmotion(emotionItem.id) }} />
                </Tooltip>
            )
        })

    const getEmotionOfPost = async () => {
        let url = 'api/newspost/' + hashTag.detail.id + '/get_emotion_post/'
        let a = await callApi(url, 'GET', null, null)
        listEmotion.emotion = a.data
        setGetEmotionSuccess(true)
        console.log("tông: ", listEmotion.emotion.statistical.length)
    }

    const getEmotionOfType = () =>
        listEmotion.emotion.statistical && listEmotion.emotion.statistical.map((emotionItem) => {
            return (
                <TabPane
                    tab={
                        <span style={{ fontSize: "30px", display: "flex" }}>
                            <Avatar src={emotionItem.image} />
                            {emotionItem.amount}
                        </span>
                    }
                    key={emotionItem.id}
                >
                    {listEmotion.emotion.data.filter(d => d.emotion_type == emotionItem.id).map(res => {
                        return (
                            <div style={{ margin: "5px", fontSize: "15px", display: "flex" }}>
                                <Badge
                                    overlap="circular"
                                    anchorOrigin={{
                                        vertical: 'bottom',
                                        horizontal: 'right',
                                    }}
                                    badgeContent={<SmallAvatar alt="Remy Sharp" src={emotionItem.image} />}
                                >
                                    <Avatar src={res.author.avatar} >{(res.author.username).slice(0, 1)}</Avatar>
                                </Badge>

                                
                                {res.author.username}
                            </div>
                        )
                    }

                    )}
                </TabPane>
            )
        }
        )





    const getEmotionGroup = () =>
        listEmotion.emotion.statistical && listEmotion.emotion.statistical.map((emotionItem) => {
            return (
                <Avatar src={emotionItem.image}>

                </Avatar>
            )
        }
        )

    getListEmotion()
    getEmotionOfPost()
    return (
        <>
            <div className="d-grid left-right mt-5 pb-md-5">
                <div className="buttons-singles tags">
                    <h4>Tags :</h4>
                    {hashTags()}
                    {/* <a href="#blog-tag">Disaster Relief</a> */}
                </div>
                
            </div>
            <div className="container">
                <div  style={{ display: "flex" }}>
                        <div style={{ display: "flex" }}>{renderEmotion()}</div>
                </div>
                <div style={{ float:"right", position:"relative", top: "-40px",display: "flex"}}>
                            <AvatarGroup>
                                {getEmotionGroup()}
                            </AvatarGroup>
                            <h5 onClick={showModal} style={{margin: "auto"}}>  {Object.keys(listEmotion.emotion).length !== 0 ? listEmotion.emotion.data.length : 0} emotion</h5>
                        </div>
                        {/* <a href="#blog-share"><EmojiEmotions /></a> */}
            </div>
            <hr />
            <Modal visible={isModalVisible} onCancel={handleCancel}>
                <Tabs defaultActiveKey="2">
                    {getEmotionOfType()}
                </Tabs>,

            </Modal>
        </>
    )

}
export default TagAndShare;