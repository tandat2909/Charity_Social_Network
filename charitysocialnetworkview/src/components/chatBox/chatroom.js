
import React from 'react';
import SideBar from './sidebar';
import {Row, Col } from 'antd'
import ChatWindow from './chatWindow';

const ChatRoom = () =>{
    return(
        <div>
            <Row>
                <Col span={6}><SideBar></SideBar></Col>
                <Col span={18}><ChatWindow></ChatWindow></Col>
            </Row>
        </div>
    )
}
export default ChatRoom