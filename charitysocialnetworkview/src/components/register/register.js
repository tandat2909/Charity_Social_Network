import { MenuItem} from '@material-ui/core';
import React, { useState, createRef} from 'react';
import { makeStyles, styled,  } from "@material-ui/core/styles";
import TextField from '@mui/material/TextField';
import Alert from '@mui/material/Alert';
import callApi from '../../utils/apiCaller';
import { useHistory } from "react-router-dom";


const useStylesUpdate = makeStyles((theme) => ({
    root: {
        margin: theme.spacing(1),
        
    },
    div: {
        margin : "20px",
    
    }
}));

const ValidationTextField = styled(TextField)({
    '& input:valid + fieldset': {
        color:'white',
        borderColor: '#ffc107',
        borderWidth: 3,
    },
    '& input:invalid + fieldset': {
        color:'white',
      borderColor: 'red',
      borderWidth: 3,
    },
    '& input:valid:focus + fieldset': {
      borderLeftWidth: 6,
      borderColor: '#e4195e',
      padding: '4px !important', // override inline-style
    },
    // '& label:valid:focus + fieldset': {
    //     color: '#e4195e',
      
    //   },
    "& .MuiInputBase-root": {

        "& input": {
        color: "white",
        },
        
      },
      "& .MuiInputLabel-root": { 
        "& label": {
            color: "white",
            }
      },
      "& .css-14s5rfu-MuiFormLabel-root-MuiInputLabel-root": {
        color: "white"
      },
      "& .css-1kty9di-MuiFormLabel-root-MuiInputLabel-root": {
        color: "white", 
        fontSize: "18px",
      },

  });


//   const styles = withStyles((theme) => ({
//     root: {
//         "& .MuiInputBase-root": {
//             "& input": {
//             color: "white",
//             }
//           }
//     }
//   }))(TextField);

//   const styles = theme => ({
//     multilineColor:{
//         color:'white'
//     }
// });

const Register = () => {
    const classes = useStylesUpdate();
    const [value, setValue] = useState(new Date());
    const [confirm, setConfirm] = useState()
    const [showAlert, setShowAlert] = useState(false)
    const image = createRef()
    const [profile, setProfile] = useState({
        username: "",
        password: "",
        first_name: "",
        last_name: "",
        nick_name: "",
        phone_number: "",
        address: "",
        avatar: "",
        gender: "",
        birthday: "",
    });
    let history = useHistory()

    const [errors, setErrors] = useState({});

    const validate = (fieldValues = profile) =>{
        let temp = { ...errors }
        if('username' in fieldValues) 
        temp.username =  fieldValues.username ? "" : "Do not leave this field blank"

        if('password' in fieldValues) 
        temp.password =  fieldValues.password ? "" : "Do not leave this field blank"
        if('confirm_password' in fieldValues) 
        temp.confirm_password =  fieldValues.confirm_password ? "" : "Do not leave this field blank"
        // if('confirm_password' in fieldValues) 
        // {
        //     if(fieldValues.confirm_password)
        //     {
        //         if(fieldValues.confirm_password !== fieldValues.password)
        //         {
        //             console.log("password có hk", fieldValues.password)
        //             temp.confirm_password = "confirm chưa đúng"
        //         }
        //         else
        //             temp.confirm_password = ""
        //     }
            
        // }
        // else
        //     temp.confirm_password = "Do not leave this field blank"
        
        if('nick_name' in fieldValues) 
        temp.nick_name =  fieldValues.nick_name ? "" : "Do not leave this field blank"
        if('birthday' in fieldValues)
            temp.birthday =  fieldValues.birthday ? "" : "this field is required."
        if('email' in fieldValues) 
            temp.email =  (/$^|.+@.+..+/).test(fieldValues.email) ? "" : "this field is required."
        if('avatar' in fieldValues) {
            temp.avatar =  fieldValues.avatar ? "" : "Do not leave this field blank"
        }
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
       if(event.target.name !== "confirm_password")
       {
            setProfile({...profile,
                [name]: value,
            });
       }
       else{
           setConfirm(event.target.value)
       }
        validate({ [name]: value })
    }


    const handleSubmit = async (event) => {
        if(confirm !== profile.password){
            setShowAlert(true)
        }
        else{
        let post = {...profile}
        let input_image = image.current.getElementsByTagName('input')[0]
        
        let formData = new FormData();
        Object.keys(post).forEach((key) =>  {
            if(key !== 'avatar'){
                formData.append(key,post[key])
            }
            else
                formData.append("avatar", input_image.files[0])
        })
        
        console.log("dữ liêu: ", input_image.files[0])
        let header = { 'content-type': 'multipart/form-data' }
        
    
        let p = await callApi('api/accounts/', 'POST', formData, header).then(res => {
          if (res.status === 200 || res.status === 201) {
            alert("bạn đã đăng nhập thành công")
            history.replace("/login")
          }
    
        }).catch(err => {console.log(err.response)})
    }
      };
    

        return (
            <>
                <div style={{ backgroundImage: 'url(images/banner4.jpg)', backgroundRepeat: "no-repeat", width: "100%"}}>
                    <div className="container" style={{width: "50%"}}>
                    <p style={{textAlign: "center", padding: "20px 0", color: "orange", fontSize: "50px"}}>Save Poor</p>
                            <h2 style={{textAlign: "center", padding: "20px 0", color: "#e4195e"}}>Register Here</h2>

                            {showAlert === true ? <Alert severity="error">mật khẩu chưa đúng</Alert> : ""}
                        <div style={{width: "100%", padding: "30px ", backgroundColor:"#544f4f6b", borderRadius: "30px"}}>
                            
                        <div className={classes.div}>
                            <ValidationTextField
                                name="username"
                                autoFocus 
                                type="text"
                                id="outlined-basic" 
                                label="Username" 
                                variant="outlined"  
                                fullWidth
                                error={errors.username}
                                helperText={errors.username ? errors.username : null}
                                onChange={handleChange}
                              
                                />
                        </div>  
                        <div className={classes.div} style={{display: "flex"}}>
                            <ValidationTextField 
                                name="password"
                                autoFocus 
                                type="password"
                                id="outlined-basic" 
                                label="Password" 
                                variant="outlined"  
                                fullWidth 
                                style={{margin: "0 10px", color: "white", borderColor: "white"}}
                                error={errors.password}
                                helperText={errors.password ? errors.password : null}
                                onChange={handleChange}
                                
                                />
                            <ValidationTextField 
                                name="confirm_password"
                                autoFocus 
                                type="password"
                                id="outlined-basic" 
                                label="Confirm password" 
                                variant="outlined" 
                                fullWidth 
                                style={{margin: "0 10px"}}
                                error={errors.confirm_password}
                                helperText={errors.confirm_password ? errors.confirm_password : null}
                                onChange={handleChange}/>
                        </div>
                        
                        <div className={classes.div} style={{display: "flex"}}>
                            <ValidationTextField 
                                name="first_name"
                                autoFocus
                                type="text"
                                id="outlined-basic" 
                                label="First name" 
                                variant="outlined" 
                                fullWidth 
                                style={{margin: "0 10px"}}
                                onChange={handleChange}
                                error={errors.first_name}
                                helperText={errors.first_name ? errors.first_name : null}
                                // color='white'

                                
                                />
                            <ValidationTextField 
                                name="last_name"
                                autoFocus
                                type="text"
                                id="outlined-basic" 
                                label="Last name" 
                                variant="outlined" 
                                fullWidth 
                                style={{margin: "0 10px"}}
                                onChange={handleChange}
                                error={errors.last_name}
                                helperText={errors.last_name ? errors.last_name : null}/>
                        </div>
                    
                        <div className={classes.div} style={{display: "flex"}}>
                    
                            <ValidationTextField 
                                name="birthday"
                                autoFocus
                                id="outlined-basic" 
                                label="Birthday" 
                                type="date" 
                                InputLabelProps={{
                                    shrink: true,
                                    }}
                                variant="outlined"  
                                fullWidth 
                                style={{margin: "0 10px"}}
                                onChange={handleChange}
                                error={errors.birthday}
                                helperText={errors.birthday ? errors.birthday : null}
                                />
                            <ValidationTextField 
                                name="phone_number"
                                autoFocus
                                type="text"
                                id="outlined-basic" 
                                label="Phone number" 
                                variant="outlined" 
                                fullWidth 
                                style={{margin: "0 10px"}}
                                onChange={handleChange}
                                error={errors.phone_number}
                                helperText={errors.phone_number ? errors.phone_number : null}
                                />
                            <ValidationTextField 
                                name="gender"
                                autoFocus
                                id="outlined-basic" 
                                label="Gender" 
                                type="text" 
                                select 
                                variant="outlined" 
                                fullWidth 
                                style={{margin: "0 10px"}}
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
                            </ValidationTextField>
                        </div>
        

                        <div className={classes.div}>
                            <ValidationTextField
                                name="address"
                                autoFocus
                                type="text" 
                                id="outlined-basic" 
                                label="Address" 
                                variant="outlined" 
                                fullWidth
                                onChange={handleChange}
                                error={errors.address}
                                helperText={errors.address ? errors.address : null}/>
                        </div>
                        <div className={classes.div}>
                            <ValidationTextField 
                                name="avatar"
                                autoFocus
                                id="outlined-basic" 
                                label="Avatar" 
                                ref={image}
                                type="file"  
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                variant="outlined" 
                                fullWidth
                                onChange={handleChange}
                                error={errors.avatar}
                                helperText={errors.avatar ? errors.avatar : null}
                                />
                        </div>
                        
                        <div className={classes.div}>
                            <ValidationTextField 
                                name="nick_name"
                                autoFocus
                                id="outlined-basic" 
                                label="Nick name" 
                                variant="outlined" 
                                fullWidth
                                onChange={handleChange}
                                error={errors.nick_name}
                                helperText={errors.nick_name ? errors.nick_name : null}/>
                        </div>
                        <div style={{margin: "10px auto", width: "40%"}}>
                            <button className="btn btn-style btn-primary ml-lg-3 mr-lg-2" style={{ width: "100%"}} onClick={handleSubmit}>Contained</button>
                        </div>
                            </div>
                    </div>
                    
                </div>
            </>
        )
    
}
export default Register;
