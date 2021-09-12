import { Button, Collapse, Typography } from 'antd';
import React from 'react';
import styled from 'styled-components';
import { PlusSquareOutlined  } from '@ant-design/icons'
       

const {Panel} = Collapse;

const PanelStyled = styled(Panel)`
    &&& {
        .ant-collapse-header, p{
            color: #795548;
        }
        .ant-collapse-content-box{
            padding: 0 40px;
        }
        .add-room{
            padding: 0;
        }
    }
`;

const LinkStyled = styled(Typography.Link)`
    display: block;
    margin-bottom: 5px;
    color: #795548;
`;

export default function RoomList() {
    return(
        <Collapse defaultActiveKey={['1']}>
            <PanelStyled header="Danh sách các phòng" key='1'>
                <LinkStyled>Room1</LinkStyled>
                <LinkStyled>Room2</LinkStyled>
                <LinkStyled>Room3</LinkStyled>
                <Button type='text' icon={<PlusSquareOutlined />} class="add-room">Thêm phòng</Button>
            </PanelStyled>
        </Collapse>

    )
}