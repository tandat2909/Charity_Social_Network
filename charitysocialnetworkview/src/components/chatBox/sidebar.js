import { Col, Row } from 'antd';
import React from 'react';
import RoomList from './roomlist';
import UserInfor from './userinfor';
import styled from 'styled-components'

const SidebarStyled = styled.div`
    background: #f19814;
    color: white;
    height: 100vh;
`;

export default function SideBar() {
    
    return(
        <SidebarStyled>
            <Row>
                <Col span={24}><UserInfor></UserInfor></Col>
                <Col span={24}><RoomList></RoomList></Col>
            </Row>
        </SidebarStyled>
    )
}
