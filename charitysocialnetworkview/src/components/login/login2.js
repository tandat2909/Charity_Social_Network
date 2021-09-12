import React, { useState,useContext } from 'react';
import './../../css/logins_style.css';
import axios from 'axios';
import qs from 'qs';
import { useHistory } from "react-router-dom";
import {contexts} from '../../context/context'
import callApi from '../../utils/apiCaller';
import firebase, { auth} from '../firebase/config';
import { Button } from '@material-ui/core';


const fbProvider = new firebase.auth.FacebookAuthProvider()

const Logins = (props) => {

   const context = useContext(contexts)
 

    let [credentials, setcredentials] = useState({
        username:"",
        password:"", 
        // isLogin : localStorage.getItem('access_token') != null
    })
    
    let history = useHistory()
    let login = async event => {
        try{
            let payload = {
                client_id: 'fMsSJ477u9nT7yy0ZUexLKyMTVcrOzBGXyKIX97C',
                client_secret: '1avszJ6kjnWNQ4bDKtA3a5k4oN79cEnGKOuYwlVcHeZp2XwDoaYMLB6pPsh5rWtOXMf4EwlFwyBPkQiUtsg4AzqIgqoivB9G6NiWlDpIyJDUUam2DBDSLRfzH5Kvf97d',
                grant_type: 'password',
                ...credentials,
            }      
            console.log(payload)
            let res = await axios({
                method: 'POST',
                url: 'http://127.0.0.1:8000/o/token/',
                headers: { 'content-type': 'application/x-www-form-urlencoded' },
                data: qs.stringify(payload)
            });
            console.log(res)
            if (res.status === 200) {
                console.log('thanh cong')
                console.log(res);
                
                localStorage.setItem('access_token', res.data.access_token);
                localStorage.setItem('expires_in', res.data.expires_in);
                localStorage.setItem('refresh_token', res.data.refresh_token);
                localStorage.setItem('token_type', res.data.token_type);
                localStorage.setItem('scope', res.data.scope);
                localStorage.setItem('authorization', true);
                console.log(res.data.access_token);
                // this.setState({status_login:true})
               
                context.authorization = true
                history.replace("/profile")
                
                console.log(context.authorization)
                return
            }
            //   history.replace("/login")
            console.log("đăng nhập thất bại")
            // this.setState({ status_login: false })
        }catch(e){
            console.log(e)
        }
       

    }

    let inputChanged = event => {
        console.log(event.target.name + "-" + event.target.value)
    
        credentials[event.target.name]=event.target.value
        
        // cred[] = ;
        // this.setState({ credentials: cred })
    }

  

    const handleFBLogin = () =>{
        auth.signInWithPopup(fbProvider)
    }
    
    return (
        <>
            
           
            <div className="img js-fullheight" style={{ backgroundImage: 'url(images/banner1.jpg)' }}>
                <section className="ftco-section">
                    <div className="container">
                        <div className="row justify-content-center">
                            <div className="col-md-6 text-center mb-5">
                                <h2 className="heading-section">Save Poor</h2>
                            </div>
                        </div>
                        <div className="row justify-content-center">
                            <div className="col-md-6 col-lg-4" style={{ padding: "30px 15px", borderRadius: "5%", backgroundColor: "#191717ad" }}>
                                <div className="login-wrap p-0">
                                    <h3 className="mb-4 text-center">Have an account?</h3>
                                    <div className="signin-form" >
                                        <div className="form-group-login">
                                            <input type="text" className="form-control-login" placeholder="Username" required onChange={(e) => inputChanged(e)} name='username' />
                                        </div>
                                        <div className="form-group-login">
                                            <input id="password-field" type="password" className="form-control-login" placeholder="Password" onChange={(e) => inputChanged(e)} required name='password' />
                                            <span toggle="#password-field" className="fa fa-fw fa-eye field-icon toggle-password"></span>
                                        </div>
                                        <div className="form-group-login">
                                            <button type="submit" className="form-control-login btn-login btn-primary-login submit px-3"
                                                style={{ backgroundColor: "orange", width: "100%" }} onClick={() => login()} >Sign In</button>
                                        </div>
                                        {/* <div className="form-group-login d-md-flex">
                                                <div className="w-50">
                                                    <label className="checkbox-wrap-login checkbox-primary-login">Remember Me
                                                        <input type="checkbox" checked />
                                                        <span className="checkmark-login"></span>
                                                    </label>
                                                </div>
                                                <div className="w-50 text-md-right">
                                                    <a className="login" href="#" style={{color: "#fff"}}>Forgot Password</a>
                                                </div>
                                            </div> */}
                                    </div >
                                    <p className="w-100 text-center">&mdash; Or Sign In With &mdash;</p>
                                    <div className="social d-flex text-center">
                                        <Button onClick={handleFBLogin}> Facebook</Button>
                                        
                                        <a className="login" href="#/" className="px-2 py-2 ml-md-1 rounded"><span className="ion-logo-twitter mr-2"></span> Twitter</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </>
    );

}
export default Logins;