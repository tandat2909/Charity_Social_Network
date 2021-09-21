import React, { useState, useContext} from 'react';
import {Button, TextField, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, MenuItem} from '@material-ui/core';
import {Create} from '@material-ui/icons';
import { makeStyles } from "@material-ui/core/styles";
import { contexts } from "../../context/context"
import dateFormat from 'dateformat';
import callApi from '../../utils/apiCaller';
  
const useStylesUpdate = makeStyles((theme) => ({
    root: {
        margin: theme.spacing(1),
        // height: '200px',
        // overflowY : 'scroll',
        
    },
    div: {
        margin : "10px",
    }
}));

const UpdateProfile = (props) => {
    const classes = useStylesUpdate();
    const infor = useContext(contexts)
    const [open, setOpen] = useState(false);
    const [errors, setErrors] = useState({});
    const [profile, setProfile] = React.useState({
   
    });
    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };
   

    const validate = (fieldValues = profile) =>{
        let temp = { ...errors }
        if('birthday' in fieldValues)
            temp.birthday =  fieldValues.birthday ? "" : "this field is required."
        if('date_joined' in fieldValues) {
            temp.date_joined =  fieldValues.date_joined ? "" : "Do not leave this field blank"
        }
        if('email' in fieldValues) 
            temp.email =  (/$^|.+@.+..+/).test(fieldValues.email) ? "" : "this field is required."
        if('gender' in fieldValues) 
            temp.gender =  fieldValues.gender ? "" : "Do not leave this field blank"
        if('first_name' in fieldValues) 
        temp.first_name =  fieldValues.first_name ? "" : "Do not leave this field blank"
        if('last_name' in fieldValues) 
        temp.last_name =  fieldValues.last_name ? "" : "Do not leave this field blank"
        if('address' in fieldValues) 
        temp.address =  fieldValues.address ? "" : "Do not leave this field blank"
        if('phone_number' in fieldValues) 
        temp.phone_number =  fieldValues.phone_number.length == 10 && fieldValues.phone_number ? "" : 
        "10 numbers required and Do not leave this field blank"
        
        setErrors({
            ...temp
        })
        if (fieldValues === profile)
            return Object.profile(temp).every(x => x == "")
        

    }
   
    const handleChange = (event) => {
        const target = event.target;
        const {name, value} = target;
       
        setProfile({...profile,
                [name]: value,
            });
        validate({ [name]: value })
    }

    const updateProfile = async() =>{
       
            
        let update = {...profile}
        let url = 'api/accounts/' + `${infor.dataProfile.id}` + '/'
        console.log(url)
        let p = await callApi(url, 'PATCH', update, null).then(res => {
            if (res.status === 200 || res.status === 201) {
                alert("bạn đã sửa thành công")
                handleClose()
            }
            else
                alert("bạn đã sửa thất bại")
            infor.dataProfile = res.data
            props.update()
            
        })
       


       
    }

    return (
        <div>
            <Button
                onClick={handleClickOpen}
                color="default"
                startIcon={<Create />}
                style={{fontSize: 'small'}}
                // ghost={true}
            >
                Update
            </Button>
            <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title" >
                <DialogTitle id="form-dialog-title">User Information</DialogTitle>
                <DialogContent>
                   
                    <DialogContentText className={classes.root}>
                        <form >
                            <div className={classes.div}>
                                <TextField
                                    style={{width: "45%", marginRight: "5%"}}
                                    label="Birthday"
                                    type="date"
                                    defaultValue={dateFormat(infor.dataProfile.birthday, "yyyy-mm-dd")}
                                    onChange={handleChange}
                                    variant="outlined"
                                    InputLabelProps={{
                                    shrink: true,
                                    }}
                                    name="birthday"
                                    error={errors.birthday}
                                    helperText={errors.birthday ? errors.birthday : null}
                                />
                            
                        
                                <TextField
                                    style={{width: "45%", marginRight: "5%"}}
                                    label="Date join"
                                    type="date"
                                    variant="outlined"
                                    defaultValue={dateFormat(infor.dataProfile.date_joined, "yyyy-mm-dd")}
                                    InputLabelProps={{
                                    shrink: true,
                                    }}
                                    onChange={handleChange}
                                    name="date_joined"
                                    error={errors.date_joined}
                                    helperText={errors.date_joined ? errors.date_joined : null}
                                />
                            </div>

                            <div className={classes.div}>
                                <TextField
                                    autoFocus
                                    margin="dense"
                                    label="Email Address"
                                    variant="outlined"
                                    defaultValue={infor.dataProfile.email}
                                    type="email"
                                    fullWidth
                                    onChange={handleChange}
                                    name="email"
                                    error={errors.email}
                                    helperText={errors.email ? errors.email : null}
                                />
                            </div>
                            <div className={classes.div}>
                                <TextField
                                    name="gender"
                                    label="Gender"
                                    type="text"
                                    select
                                    variant="outlined"
                                    defaultValue={infor.dataProfile.gender === 'women' ? 'women' : 'men'}
                                    fullWidth
                                    onChange={handleChange}
                                    error={errors.gender}
                                    helperText={errors.gender ? errors.gender : null}
                                >
                                    
                                    <MenuItem value="">
                                        <em>Orther</em>
                                    </MenuItem>
                                    <MenuItem key={1} value='women' >
                                        Women
                                    </MenuItem>
                                    <MenuItem key={2} value='men' >
                                        Men
                                    </MenuItem>
                                </TextField>
                            </div>
                            <div className={classes.div}>
                                <TextField
                                    name="first_name"
                                    autoFocus
                                    label="First Name"
                                    type="text"
                                    defaultValue={infor.dataProfile.first_name}
                                    fullWidth
                                    variant="outlined"
                                    onChange={handleChange}
                                    error={errors.first_name}
                                    helperText={errors.first_name ? errors.first_name : null}
                                />
                            </div>
                            <div className={classes.div}>
                                <TextField
                                    name="last_name"
                                    autoFocus
                                    label="Last Name"
                                    type="text"
                                    defaultValue={infor.dataProfile.last_name}
                                    fullWidth
                                    variant="outlined"
                                    onChange={handleChange}
                                    error={errors.last_name}
                                    helperText={errors.last_name ? errors.last_name : null}
                                />
                            </div>
                            <div className={classes.div}>
                                <TextField
                                    name="address"
                                    label="adress"
                                    type="text"
                                    defaultValue={infor.dataProfile.address}
                                    variant="outlined"
                                    fullWidth
                                    onChange={handleChange}
                                    error={errors.address}
                                    helperText={errors.address ? errors.address : null}
                                />
                            </div>
                            <div className={classes.div}>
                                <TextField
                                    name="phone_number"
                                    label="PhoneNumber"
                                    type="text"
                                    defaultValue={infor.dataProfile.phone_number}
                                    variant="outlined"
                                    fullWidth
                                    onChange={handleChange}
                                    error={errors.phone_number}
                                    helperText={errors.phone_number ? errors.phone_number : null}
                                />
                            </div>
                            
                        </form>
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={updateProfile} color="primary">
                        Update
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}

export default UpdateProfile;