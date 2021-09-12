import React from 'react';
import styled from 'styled-components';
import { UserAddOutlined  } from '@ant-design/icons';
import { Button, Tooltip, Avatar, Form, Input } from 'antd';
import Message from './message';



const HeaderStyled = styled.div`
    display: flex;
    justify-content: space-between;
    height: 56px;
    padding: 0 16px;
    align-items: centre;
    border-bottom: 1px solid red;

    .header{
        &__info {
            display: flex;
            flex-direction: column;
            justify-content: centre;
        }

        &__title{
            margin: 0;
            font-weight: bold; 
        }

        &__description{
            font-size: 12px;
        }
        
    }
`;


const ButtonGroupStyled = styled.div`
    display: flex;  
    align-items: centre;
`;

const WrapperStyled = styled.div`
    height: 100vh;
`;


const MessageListStyled = styled.div`
    max-height: 100%;
    overflow-y: auto;
`;

const ContentStyled = styled.div`
    height: calc(100% - 56px);   
    display: flex; 
    flex-direction: column;
    padding: 11px;
    justify-content: flex-end;
  
`;


const FormStyled = styled(Form)`
    display: flex; 
    align-items: centre;
    justify-content: space-between;
    padding: 2px 2px 2px 0;
    border-bottom: 1px solid red;
    border-radius: 2px;

    .ant-form-item{
        flex: 1;
        margin-bottom: 0;
    }
`;

export default function ChatWindow() {
    return(
        <WrapperStyled>
            <HeaderStyled>
                <div class="header__info">
                    <p class="header__title">room1</p>
                    <span class="header__description">Đây là room 1</span>
                </div>
                <ButtonGroupStyled>
                    <Button icon={<UserAddOutlined />} type="text">Mời</Button>
                    <Avatar.Group size="small" maxCount={2}>
                        <Tooltip title="Q">
                            <Avatar>Q</Avatar>
                        </Tooltip>
                        
                        <Tooltip title="T">
                            <Avatar>T</Avatar>
                        </Tooltip>

                        <Tooltip title="D">
                            <Avatar>D</Avatar>
                        </Tooltip>
                    </Avatar.Group>
                </ButtonGroupStyled>
            </HeaderStyled>
            <ContentStyled>
                <MessageListStyled>
                    <Message text="Test" photoURL={null} displayName="Quynh" createdAt={12122122}></Message>
                    <Message text="Test1" photoURL={null} displayName="Tư dú lép" createdAt={12122122}></Message>
                    <Message text="Test2" photoURL={null} displayName="Đạt lưu đạn" createdAt={12122122}></Message>
                    <Message text="Test3" photoURL={null} displayName="Huy phân hủy" createdAt={12122122}></Message>
                </MessageListStyled>
                <FormStyled>
                    <Form.Item>
                        <Input placeholder="nhập tin nhắn...." bordered={false} autoComplete="off"></Input>
                    </Form.Item>
                    <Button type="primary">Gửi</Button>
                </FormStyled>
            </ContentStyled>
        </WrapperStyled>
    )
}