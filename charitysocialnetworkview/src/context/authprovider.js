

import React, {useState, useEffect, useContext} from 'react';
import  {auth} from '../components/firebase/config';
import {Spin} from 'antd';
import { useHistory } from "react-router-dom";

export const AuthContext = React.createContext({
    user:null
});

export default function AuthProvider(props){
    let f = useContext(AuthContext)
    const [isloading, setIsloading] = useState(true)
    const history = useHistory();
    useEffect(() => {
        const unsubscibed = auth.onAuthStateChanged((data) => {
            console.log(data)
            if(data){
                const{ displayName, email, uid, photoURL } = data 
                f.user = { displayName, email, uid, photoURL }
                setIsloading(false)
                history.push('/')
                return;
            }
            setIsloading(false)
            history.push('/login')
        })

        return () => {
            unsubscibed();
        }

    }, [])
    


    return(
        <>
            {isloading ? <Spin /> : props.children}
        </>
    );
}

;