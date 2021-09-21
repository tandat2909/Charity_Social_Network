import { Avatar, Button, Typography} from 'antd';
import React, { useContext, useEffect } from 'react';
import styled from 'styled-components'
import { AuthContext } from '../../context/authprovider';
import { auth, db } from '../firebase/config';

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
    
    const {user: {
        displayName, 
        photoURL
    }} = useContext(AuthContext)
    return(
        <WrapperStyled>
           
            <div >
                <Avatar src={photoURL}>{photoURL ? "" : displayName?.charAt(0).toUpperCase()}</Avatar>
                <Typography.Text className="username">{displayName}</Typography.Text>
            </div>
            <Button ghost onClick={() => auth.signOut()}>Đăng xuất</Button>
        </WrapperStyled>
    )
}