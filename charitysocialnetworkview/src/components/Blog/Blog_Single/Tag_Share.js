import React, { useContext, useState,useEffect } from 'react';
import { NewsPostContextMod } from '../../../context/newspost_mod'
import { ListEmotion } from '../../../context/emotion';
import axios from 'axios';
import callApi from '../../../utils/apiCaller';
import { Modal, Tabs, Tooltip, Input } from 'antd';
import { contexts } from '../../../context/context'
import { report } from '../../../context/report'
import { useHistory } from "react-router-dom";
import { Badge, List, ListSubheader, ListItem,ListItemText, ListItemSecondaryAction, Checkbox, TextArea} from '@material-ui/core';
import AvatarGroup from '@material-ui/lab/AvatarGroup';
import { withStyles } from '@material-ui/core/styles';
import { makeStyles } from '@material-ui/core/styles';
import Avatar from '@mui/material/Avatar';


const SmallAvatar = withStyles((theme) => ({
    root: {
      width: 30,
      height: 30,
     
    },
  }))(Avatar);

  const useList = makeStyles((theme) => ({
    root: {
        width: '100%',
        margin: "0 auto",
        backgroundColor: theme.palette.background.paper,
    },
}));

const TagAndShare = () => {
    let hashTag = useContext(NewsPostContextMod)
    let listEmotion = useContext(ListEmotion)
    let context = useContext(contexts)
    let listReport = useContext(report)
    let [get_emotion_success, setGetEmotionSuccess] = useState(false)
    let [post_emotion_success, setPostEmotionSuccess] = useState(false)
    let history = useHistory()
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [isModalRepost, setIsModalRepost] = useState(false);
    let [checkBoxValue, setCheckBoxValue] = useState()
    let [contentReport, setContentReport] = useState()
    let [emotion, setEmotion] = useState([])

    const list = useList();
    const { TabPane } = Tabs;
    const { TextArea } = Input;

    const handleChangeCheckbox = (event) => {
        setCheckBoxValue(event.target.value);
    }

    const handleChangeContent = (event) => {
        setContentReport(event.target.value);
    }


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

    const renderEmotion = (props = listEmotion.list) =>{

        let emotion_of_user = listEmotion.emotion?.data?.filter(i => i.user.id === context.dataProfile.id)[0]
        console.log(emotion_of_user,context.dataProfile.id)

        return props && props.map((emotionItem) => {
            if(emotionItem.id === emotion_of_user?.type){
                return(
                    <Tooltip title={emotionItem.name} placement="top">
                        <Avatar sx={{ width: 60, height: 60, paddingBottom: "1.1em"}} src={emotionItem.image} onClick={() => { postEmotion(emotionItem.id) }} />
                    </Tooltip>
                )
            
            }
            else{
                return (
                    <Tooltip title={emotionItem.name} placement="top">
                        <Avatar sx={{ width: 45, height: 45 }} src={emotionItem.image} onClick={() => { postEmotion(emotionItem.id) }} />
                    </Tooltip>
                )
            }
        })

    }
        


    const getEmotionOfPost = async () => {
        let url = 'api/newspost/' + hashTag.detail.id + '/get_emotion_post/'
        let a = await callApi(url, 'GET', null, null)
        listEmotion.emotion = a.data
        setEmotion(a.data.results)
        setPostEmotionSuccess(true)
        console.log("tông: ", listEmotion.emotion.statistical.length)
    }

    useEffect(() => {
        getEmotionGroup()
    },[emotion])



    //thống kê người thả emotion cho bài viết
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
                    {listEmotion.emotion.data && listEmotion.emotion.data.filter(d => d.type == emotionItem.id).map(res => {
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
                                    <Avatar src={res.user.avatar} >{(res.user.username).slice(0, 1)}</Avatar>
                                </Badge>

                                {res.user.username} 
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
                <Avatar src={emotionItem.image} sx={{ width: 50, height: 50 }}>
                </Avatar>
            )
        }
        )


    const getListReport = async() => {
        let a = await callApi("api/optionreport/", 'GET', null, null)
        listReport.list = a.data.results
    }
    const showListReport = () =>
        listReport.list && listReport.list.map((item, index) => {
            return (
                <ListItem dense button key={item.id} >
                        <ListItemText primary={(index + 1) + '. ' + item.content} />
                        <ListItemSecondaryAction>
                            <Checkbox  edge="end"
                                checked ={parseInt(checkBoxValue) === item.id}
                                onChange={handleChangeCheckbox}
                                value={item.id}
                                name="content"
                                inputProps={{ 'aria-label': item.id }}
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
            )
        })



    const ReportPost = async() => {
        // console.log("id bài viết: ",hashTag.detail.id)
        if(checkBoxValue === undefined){
            alert("bạn cần chọn lí do để report")
        }
        else{
            let report = {"reason" : parseInt(checkBoxValue), "content" : contentReport}
            let url = 'api/newspost/' + hashTag.detail.id + '/report/'
            let a = await callApi(url, 'POST', report, null).then(res => {
                if (res.status === 200 || res.status === 201)
                    alert("bạn đã report bài viết thành công")
            }).catch(err => {console.log(err)})
            setIsModalRepost(false)
        }
    }

    getListReport()
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
                <div class="buttons-singles">
                    <h4>Report:</h4>
                        <a href="#blog-share" onClick={() => {setIsModalRepost(true)}}><span class="fas fa-user-cog" aria-hidden="true" style={{fontSize: "25px"}}></span></a>
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

            <Modal title="Repost Post" visible={isModalRepost}  onCancel={() => {setIsModalRepost(false)}} onOk={ReportPost}>
                <List 
                    subheader={
                        <ListSubheader>
                            <p>Thông tin bài viết</p>
                            <div style={{margin: "15px auto"}}>
                                <h4 style={{color: "#ff5200"}}>{hashTag.detail.title}</h4>
                                <p style={{color: "#808080ad", fontSize: "14px"}}>Được tạo bởi {hashTag.detail.user.username}</p>
                            </div>
                            {/* <Avatar src={hashTag.detail.user.avatar} /> */}
                            <h5 style={{color: "red"}}>Hãy chọn vấn đề</h5>
                            
                        </ListSubheader>
                        } 
                    className={list.root} style={{  margin: "0 auto"}}>
                    {showListReport()}
                </List>
                <TextArea
                    className="form-control-single" 
                    placeholder="Description" 
                    rows={2}
                    spellCheck="false" 
                    style={{backgroundColor:"#dcd4d433"}}
                    onChange={handleChangeContent}
                    >
                        </TextArea>
            </Modal>
        </>
    )

}
export default TagAndShare;