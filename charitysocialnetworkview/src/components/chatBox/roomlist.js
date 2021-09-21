import { Button, Collapse, Typography } from 'antd';
import React, { useContext, useMemo } from 'react';
import styled from 'styled-components';
import { PlusSquareOutlined  } from '@ant-design/icons'
import useFirestore from '../../hook/useFireStore';
import { AuthContext } from '../../context/authprovider';
import { AppContext } from '../../context/appProvider';
       

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
    const {rooms, setIsAddRoomVisible, setSelectedRoomId} = useContext(AppContext)
    console.log("lits:", {rooms})

    const handleAddRoom = () => {
        setIsAddRoomVisible(true);
      };


    return(
        <Collapse defaultActiveKey={['1']}>
            <PanelStyled header="Danh sách các phòng" key='1'>
                {
                    rooms.map(room => <LinkStyled key={room.id} onClick={() => setSelectedRoomId(room.id)}>{room.name}</LinkStyled>)
                }
                {/* <LinkStyled>Room1</LinkStyled>
                <LinkStyled>Room2</LinkStyled>
                <LinkStyled>Room3</LinkStyled> */}
                <Button type='text' icon={<PlusSquareOutlined />} class="add-room" onClick={handleAddRoom}>Thêm phòng</Button>
            </PanelStyled>
        </Collapse>

    )
}