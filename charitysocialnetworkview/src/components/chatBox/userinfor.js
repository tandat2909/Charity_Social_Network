import { Avatar, Button, Typography} from 'antd';
import React from 'react';
import styled from 'styled-components'
import { auth } from '../firebase/config';

const WrapperStyled = styled.div`
    display: flex;
    justify-content: space-between;
    padding: 12px 16px;
    border-bottom: 1px solid #d08312;

    .usename{
        color: white;
        margin-left: 5;
    }
`;


export default function UserInfor() {
    return(
        <WrapperStyled>
           
            <div >
                <Avatar>Q</Avatar>
                <Typography.Text className="username">ABC</Typography.Text>
            </div>
            <Button ghost onClick={() => auth.signOut()}>Đăng xuất</Button>
        </WrapperStyled>
    )
}