import React, { useContext, useState } from 'react';
import { Menu, MenuItem, Avatar } from '@material-ui/core';
import { NavLink, Route, Link } from 'react-router-dom';
import { contexts } from "../../context/context"
import { withStyles } from '@material-ui/core/styles';
import Badge from '@material-ui/core/Badge';
import callApi from '../../utils/apiCaller';
import { useHistory } from "react-router-dom";
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';




const StyledBadge = withStyles((theme) => ({
  badge: {
    backgroundColor: '#44b700',
    color: '#44b700',
    boxShadow: `0 0 0 2px ${theme.palette.background.paper}`,
    '&::after': {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      borderRadius: '50%',
      animation: '$ripple 1.2s infinite ease-in-out',
      border: '1px solid currentColor',
      content: '""',
    },
  },
  
  '@keyframes ripple': {
    '0%': {
      transform: 'scale(.8)',
      opacity: 1,
    },
    '100%': {
      transform: 'scale(2.4)',
      opacity: 0,
    },
  },
}))(Badge);

export default function ProfileMenu() {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [open, setOpen] = React.useState(false);
  const [passWords, setPassWord] = React.useState({
    password: '',
    password_new: '',
    password_confirm: '',
  });
  
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };


  const OpenDialog = () => {
    setOpen(true);
  };

  const CloseDialog = () => {
    setOpen(false);
  };

  const MenuLink = ({ label, to, activeOnlyWhenExact }) => {
    return (
      <Route path={to} exact={activeOnlyWhenExact} children={({ match }) => {
        var active = match ? 'active' : '';
        if (label === "Home") {
          return (
            <li className={"nav-item " + active}>
              <NavLink to={to} className='nav-link'>{label}</NavLink>
              <span className="sr-only">(current)</span>
            </li>
          )
        }
        return (
          <li className={"nav-item " + active}>
            <NavLink to={to} className='nav-link'>{label}</NavLink>
          </li>
        )
      }}
      ></Route>
    )
  }

  const [errors, setErrors] = useState({});


  const validate = (fieldValues = passWords) =>{
    let temp = { ...errors }
    if('password_new' in fieldValues)
        temp.password_new =  (/$^|(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}/).test(fieldValues.password_new) ? "" : 
        "Mật khẩu tối thiểu tám ký tự, ít nhất một ký tự hoa, một ký tự viết thường, một số và một ký tự đặc biệt"
    if('password' in fieldValues) {
        temp.password =  fieldValues.password ? "" : "Do not leave this field blank"
    }
    if('password_confirm' in fieldValues) 
      temp.password_confirm =  (/$^|(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}/).test(fieldValues.password_confirm) ? "" : 
      "Mật khẩu tối thiểu tám ký tự, ít nhất một ký tự hoa, một ký tự viết thường, một số và một ký tự đặc biệt"
    setErrors({
        ...temp
    })
    if (fieldValues === passWords)
        return Object.passWords(temp).every(x => x == "")
    

}


const handleChange = (event) => {
  const target = event.target;
  const {name, value} = target;
 
  setPassWord({...passWords,
          [name]: value,
      });
  validate({ [name]: value })
}


  let history = useHistory()
  let logout = () => {

    context.authorization = false
    callApi('api/accounts/logout/', 'GET', null, null).then(res => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('scope')
      localStorage.removeItem('expires_in')
      localStorage.removeItem('token_type')
      localStorage.removeItem('refresh_token')
      localStorage.setItem('authorization', false);
    })

    history.replace("/login")


  }
  let context = useContext(contexts)


  const changePassword = () =>{
    
    let patch = {...passWords}
    let p = callApi('api/accounts/change_password/', 'PATCH', patch, null).then(res => {
      if (res.status === 200 || res.status === 201) {
          alert("Bạn đã thay đổi mật khẩu thành công")
      }
        CloseDialog()
        logout()

      
  }).catch((err) => {
    console.log(err.response.data)
    alert(err.response.data.password)
    alert(err.response.data.password_new)
    alert(err.response.data.password_confirm)
  })
  }

  return (
    <div style={{ margin: "15px 0" }}>
      <StyledBadge
        overlap="circular"
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        variant="dot"
      >
        <Avatar onClick={handleClick} alt="Remy Sharp" src={context.dataProfile.avatar} ></Avatar>
      </StyledBadge>


      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}

      >
        <MenuItem onClick={handleClose}>
          <MenuLink label="Profile" to="/profile" activeOnlyWhenExact={false}>
          </MenuLink>
        </MenuItem>
        <MenuItem onClick={OpenDialog}>Change Password</MenuItem>
        <MenuItem><Link to="/statistic">Statistic</Link></MenuItem>
        <MenuItem onClick={logout}>Logout</MenuItem>
        <MenuItem ><Link to="/list_recerpt">pay</Link></MenuItem>
      </Menu>

      {/* 
      change password */}

      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title">Change Password</DialogTitle>
        <DialogContent>
          <DialogContentText>
                Note: when you change your password you need to login again
          </DialogContentText>
          <div style={{margin: '10px'}}>
            <TextField
              label="Current password"
              variant="outlined"
              type="text"
              fullWidth
              name="password"
              error={errors.password}
              helperText={errors.password ? errors.password : null}
              onChange={handleChange}
            />
          </div>
          <div style={{margin: '10px'}}>
            <TextField
              label="A new password"
              variant="outlined"
              type="text"
              fullWidth
              name="password_new"
              onChange={handleChange}
              error={errors.password_new}
              helperText={errors.password_new ? errors.password_new : null}
            />
          </div>
          <div style={{margin: '10px'}}>
            <TextField
              label="Enter a new password"
              variant="outlined"
              type="text"
              fullWidth
              name="password_confirm"
              onChange={handleChange}
              error={errors.password_confirm}
              helperText={errors.password_confirm ? errors.password_confirm : null}
            />
          </div>

        </DialogContent>
        <DialogActions>
          <Button onClick={CloseDialog} color="primary">
            Cancel
          </Button>
          <Button onClick={()=>{changePassword()}} color="primary">
            Subscribe
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
