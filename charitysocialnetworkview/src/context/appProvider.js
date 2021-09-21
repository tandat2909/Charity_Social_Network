import React, {useState, useMemo, useContext} from 'react';
// import  {auth} from '../components/firebase/config';
// import {Spin} from 'antd';
// import { useHistory } from "react-router-dom";
import useFirestore from '../hook/useFireStore';
import { AuthContext } from './authprovider';

export const AppContext = React.createContext();

export default function AppProvider(props){

    const [isAddRoomVisible, setIsAddRoomVisible] = useState(false);
    const [selectedRoomId, setSelectedRoomId] = useState('');
    const [isInviteMemberVisible, setIsInviteMemberVisible] = useState(false);

    // let a = useContext(AppContext)
    const {user: {uid}} = useContext(AuthContext)

    //trong collection rooms cần có name, description, member[]

    const roomsCondition = useMemo(() => {
        return {
            fieldName: 'members',
        operator: 'array-contains',
        compareValue: uid
        }
    }, [uid])

    const rooms = useFirestore('rooms', roomsCondition)

     const selectedRoom = useMemo(() => rooms.find((room) => room.id === selectedRoomId) || {}, [rooms, selectedRoomId])

    const usersCondition = React.useMemo(() => {
        return {
          fieldName: 'uid',
          operator: 'in',
          compareValue: selectedRoom.members,
        };
      }, [selectedRoom.members]);

    const members = useFirestore('users', usersCondition);
    // a.rooms = rooms
    console.log({rooms})
    return(
       
        <AppContext.Provider value={{
            rooms,
            isAddRoomVisible,
            setIsAddRoomVisible,
            selectedRoomId,
            setSelectedRoomId,
            selectedRoom,
            members,
            isInviteMemberVisible, 
            setIsInviteMemberVisible
               }}>
            {props.children}
        </AppContext.Provider>
       
    );
}