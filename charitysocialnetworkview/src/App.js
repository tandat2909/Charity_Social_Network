import React, {useContext, useState} from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import WebsiteHeader from './components/menu/menu';
import Home from './components/home/home';
import About from './components/about/about';
import Error from './components/error/errror_404';
import WebsiteFooter from './components/footer/main_footer';
import BlogPost from './components/Blog/Blog_posts';
import BlogSingle from './components/Blog/Blog_Single/Blog_single'
import Contact from './components/contact/contact';
import Logins from './components/login/login2';
import Profile from './components/profile/profile';
import ChatRoom from './components/chatBox/chatroom'
// import AuthProvider from './context/authprovider';
import callApi from './utils/apiCaller';
import {contexts} from './context/context'
import AuthorizationRequired from './components/error/error_401';
import CausesPage from './components/Cause/causes';
import AuctionDetail from './components/Auction/auction';
import Statitical from './components/statitic/Statitical';
// import AppProvider from './context/appProvider';
// import AddRoom from './components/chatBox/AddRoom';
// import InviteMember from './components/chatBox/inviteMember';
import Search from './components/search/search'
import Register from './components/register/register';

const App = () => {
  const [data, setData] = useState(false)
  const context = useContext(contexts)
  const getProfile = async () => {
    console.log("aaaaaa")
    let a = await callApi('api/accounts/profile/', 'GET', null, null)
    let b = await callApi('api/accounts/notification/', 'GET', null, null)
    context.dataProfile = a.data
    context.dataNotification = b.data
    context.authorization = true
    setData(true)
  }
  

console.log(Object.keys(context.dataProfile).length , localStorage.getItem('authorization') )
if(Object.keys(context.dataProfile).length === 0 && localStorage.getItem('authorization') === "true"){
  console.log("ffffff")
  getProfile()

}

  return (
 
    <Router>
    
      {/* <AuthProvider>
        <AppProvider> */}
      <WebsiteHeader />
      <Switch>
        <Route path="/" exact component={Home} ></Route>
        <Route path="/about" component={About}></Route>
        <Route path="/pages/causes" component={CausesPage}></Route>
        <Route path="/blog_posts" component={BlogPost}></Route>
        <Route path="/blog_single/:id" component={(props) => (<BlogSingle id={props} />)} ></Route>
        <Route path="/blog/:id/auction" component={(props) => (<AuctionDetail id={props} />)}></Route>
        <Route path="/contact" component={Contact}></Route>
        <Route path="/login" component={Logins} ></Route>
        <Route path="/register" component={Register} ></Route>
        <Route path="/search" component={Search} ></Route>
        <Route path="/statistic" component={Statitical} ></Route>
        <Route path="/chat" component={ChatRoom}></Route>
        {context.authorization === true ?
          <Switch>
            <Route path="/profile" component={Profile}></Route>
            
            <Route component={Error}></Route>
          </Switch>
          :  <Switch>
              <Route path="/profile" component={AuthorizationRequired}></Route>
              <Route path="/chat" component={AuthorizationRequired}></Route>
              <Route component={Error}></Route>
            </Switch>}
        
      </Switch>
      <WebsiteFooter />
      {/* <InviteMember />
      <AddRoom /> */}
      {/* </AppProvider>
      </AuthProvider> */}
    </Router>

  );
}

export default App;


