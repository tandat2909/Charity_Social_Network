import React, { useContext } from "react";
// import Badge from "@material-ui/core/Badge";
import NotificationsActiveIcon from '@material-ui/icons/NotificationsActive';
import { Menu, Dropdown, Badge, Card, Button } from "antd";
import "antd/dist/antd.css";
import { contexts } from '../../context/context'
import dateFormat from 'dateformat';
import Dialog from '@material-ui/core/Dialog';
import MenuItem from '@mui/material/MenuItem';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import callApi from '../../utils/apiCaller';
import { Link } from 'react-router-dom';

export default function ShowMessage() {
  let dataMess = useContext(contexts)
  const [open, setOpen] = React.useState(false);
  const [mess, setMess] = React.useState({});


  const Notification = (props = dataMess.dataNotification) => 
    props.results && props.results.map((item, index) => {
      return (
        <>
          <Menu.Item
            id={item.id}
            key={item.id}
            active={item.active}
            // style={{ height: "300px", overflowY: "inherit" }}
            onClick={() => {OpenDialog(item.id)}}
          >
            <Badge.Ribbon text={item.new === true ? "new" : "old"} color={item.new === true ? "green" : "purple"}>
              <Card type="inner" title={item.title} size="small" >
                <span style={{
                            whiteSpace: "pre-wrap", 
                            textOverflow: "ellipsis", 
                            overflow: "hidden", 
                            WebkitLineClamp: "3",
                            WebkitBoxOrient: "vertical",
                            // width: "100%", 
                            display: "block", 
                            // display: "-webkit-box",
                            height:"16px*1.3*3",
                            textAlign: "justify"}}  >
                  {item.message}
                  </span>
              </Card>
            </Badge.Ribbon>
          </Menu.Item>
          
        </>
      )
    });

  

  const OpenDialog = (props) => {
    let read ={new: false}
    let url = 'api/accounts/notification/?id=' + props + ''
    let b = callApi(url, 'PATCH', read, null)

    setOpen(true);
    // setMess(dataMess.dataNotification.results[props])
    for(let i = 0; i < dataMess.dataNotification.results.length; i++){
        if(dataMess.dataNotification.results[i].id == props){
          setMess(dataMess.dataNotification.results[i])
        }
    }
    console.log(props)
    console.log(mess)
  };

  const CloseDialog = (props) => {
    // let read ={new: false}
    // let url = 'api/accounts/notification/?id=' + props + ''
    // let b = callApi(url, 'PATCH', read, null)
    setOpen(false);
  };


  const Delete = async(props) =>{
    console.log(props)
    let url = 'api/accounts/notification/?id=' + props + ''
    let b = await callApi(url, 'DELETE', null, null).then(res => {
      if (res.status === 204) {
        alert("bạn đã xóa thông báo thành công")
        CloseDialog()
    }
  }).catch(err => {alert(err.response.data)})
  }

  const menu = (
    <Menu style={{ width: "320px", height: "400px", overflowY: "scroll"}}>
      <MenuItem> <Link to='/notification' className="blog-desc-big">See all notifications</Link></MenuItem>
      {Notification()}
    </Menu>
  );

  return (
    <div style={{ margin: "20px 10px" }}>
      <Dropdown overlay={menu} placement="bottomCenter" arrow>
        <Badge color="secondary" count={dataMess.dataNotification.count} overflowCount={10} showZero>
          <NotificationsActiveIcon color="secondary" style={{ fontSize: 30, color: "blue" }} />
        </Badge>
      </Dropdown>
        <Dialog open={open} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title">{mess.title}</DialogTitle>
        <DialogContent>
          <DialogContentText>
              Notification: {mess.message} 
          </DialogContentText>
          <DialogContentText>
              Time: {dateFormat(mess.created_date, "dd-mm-yyyy HH:MM:ss TT")}, id: {mess.id}
          </DialogContentText>

        </DialogContent>
        <DialogActions>
          <Button onClick={() =>{CloseDialog(mess.id)}} color="primary">
            Cancel
          </Button>
          <Button onClick={() => {Delete(mess.id)}} color="primary">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}