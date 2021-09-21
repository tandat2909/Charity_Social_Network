

import React, {useState, useEffect, useContext} from 'react';
import  {auth} from '../components/firebase/config';
import {Spin} from 'antd';
import { useHistory } from "react-router-dom";

export const AuthContext = React.createContext();

export default function AuthProvider({ children }){
    const [user, setUser] = useState({});
    const [isloading, setIsloading] = useState(true)
    const history = useHistory();
    useEffect(() => {
        const unsubscibed = auth.onAuthStateChanged((data) => {
            console.log(data)
            if(data){
                const{ displayName, email, uid, photoURL } = data 
                setUser({ displayName, email, uid, photoURL })
                setIsloading(false)
                // history.replace("/")
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
        <AuthContext.Provider value={{ user }}>
        {isloading ? <Spin style={{ position: 'fixed', inset: 0 }} /> : children}
      </AuthContext.Provider>
    );
}

;