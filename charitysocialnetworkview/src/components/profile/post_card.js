import React, { useContext, useState, createRef } from 'react';
import { makeStyles } from "@material-ui/core/styles";
import {
     CardContent, Avatar, CardHeader, Card, IconButton,
     TextField, MenuItem, Button
}
    from "@material-ui/core";
import {
    MoreVert
}
    from '@material-ui/icons';

import { contexts } from "../../context/context"
import { CKEditor } from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import callApi from '../../utils/apiCaller';
import { InputNumber } from 'antd';
import { DatePicker, Space } from 'antd';
import dateFormat from 'dateformat';
import moment from 'moment';
import {MyCustomUploadAdapterPlugin} from '../../utils/ckeditor_upload_image';

const useStylesCard = makeStyles((theme) => ({

    media: {
        height: 0,
        paddingTop: '56.25%', // 16:9
    },
    expand: {
        transform: 'rotate(0deg)',
        marginLeft: 'auto',
        transition: theme.transitions.create('transform', {
            duration: theme.transitions.duration.shortest,
        }),
    },
    expandOpen: {
        transform: 'rotate(180deg)',
    },
    avatar: {
        backgroundColor: 'red[500]',
    },
    post: {
        margin: "20px auto"
    },
    button: {
        '& > *': {
            margin: theme.spacing(1),
          },
    }
}));

const PostCard = (props) => {
    const classes = useStylesCard();
    const context = useContext(contexts)
    const [state, setState] = React.useState({
        category: '',
        image: '',
        title: '',
        description: '',
        hashtag: '', 
        content: '',
    });
    
    const validate = (fieldValues = state) =>{
        let temp = { ...errors }
        if('category' in fieldValues)
            temp.category =  fieldValues.category ? "" : "this field is required."
        if('image' in fieldValues) {
            console.log(fieldValues.image)  
            temp.image =  fieldValues.image ? "" : "Do not leave this field blank"
        }
        if('title' in fieldValues) 
            temp.title =  fieldValues.title ? "" : "this field is required."
        if('description' in fieldValues) 
            temp.description =  fieldValues.description ? "" : "Do not leave this field blank"
        if('hashtag' in fieldValues) 
        temp.hashtag =  fieldValues.hashtag ? "" : "Do not leave this field blank"
        
        
        setErrors({
            ...temp
        })
        if (fieldValues === state)
            return Object.state(temp).every(x => x === "")
        

    }

    const image = createRef()
    const date = createRef()
    const [errors, setErrors] = useState({});

    const handleChange = (event) => {
        // console.log(event)
        // console.log(event[0]._d.getDate())
        const target = event.target;
        const {name, value} = target;
        if(name === 'hashtag' && name !== null)
        {
            setState({...state,
                hashtag: value.split('#')})
        }
        else
            setState({...state,
                    [name]: value,
                });
        
        validate({ [name]: value })
        
    }
    const handleCkEditor = (event, editor) =>{
        const data = editor.getData();
        setState({...state,
            content: data
        })
        console.log(data)
    }
    const handleChangeDate = (event) => {
        setState({...state,
            start_datetime: dateFormat(event[0]._d,"yyyy-mm-dd h:MM:ss"),
            end_datetime: dateFormat(event[1]._d,"yyyy-mm-dd h:MM:ss"), 
        
        })
    }
    const handleChangePrice = (event) => {
        setState({...state,
            price_start: event,

        })
    }

    //không cho chọn những ngày trước 
    const disabledDate = (current) => {
        return current && current < moment().endOf('day');
    }
    //không cho chọn những giờ trước của ngày hiện tại
    

    // const disabledRangeTime = (current) => {
    //     return current && current < moment().endOf('hours');
    //   }

    const submitHandle = (e) =>{
        e.preventDefault()
        console.log(state)
    }

    const resetForm = () => {
        setState({
            category: '',
            image: '',
            title: '',
            description: '', 
            hashtag: '',
            content: '',

        });
        setErrors({})
    }

    const auction = () =>{
        const { RangePicker } = DatePicker;
        if(state.category === 1)
            return(
                <>
                     <div className={classes.post}>
                        <label style={{color : "#a5a2a2", font: "small"}}>StartDay - EndDay</label>
                        <Space direction="vertical" size={12} style={{width: "100%"}}>
                            <RangePicker  
                                onChange ={handleChangeDate}  
                                disabledDate={disabledDate} 
                                // disabledTime={disabledRangeTime}
                                ref={date} 
                                showTime={{
                                    hideDisabledOptions: true,
                                    defaultValue: [moment('00:00:00', 'HH:mm:ss'), moment('11:59:59', 'HH:mm:ss')],
                                }}
                                format="YYYY-MM-DD HH:mm:ss" />
                        </Space> 
                    </div>
                    <div className={classes.post}>
                        <label style={{color : "#a5a2a2", font: "small"}}>Price</label>
                        <InputNumber
                            min={1}
                            style={{width: "100%"}}
                            formatter={value => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',' +'vnd')}
                            parser={value => value.replace(/\$\s?|(,*)/g, '')}
                            onChange ={handleChangePrice}
                            />
                    </div>
                   
                </>
            )
    }

    const postNews = async () => {
        let post = {...state}
        let form = new FormData()
        Object.keys(post).forEach((key) =>  {
            if(key === 'hashtag'){
                for(let i = 0; i < post[key].length; i++)
                form.append('hashtag', post[key][i])
            }
            else
                form.append(key,post[key])
        })
       
        // console.log(image.current,image.current.getElementsByTagName('input'))
        let input_image = image.current.getElementsByTagName('input')[0]
        // console.log("date current: ",date.current)
        // console.log("date",date)
        // let start_date = date.current.getElementsByTagName('input')[0].value
        // let end_date = date.current.getElementsByTagName('input')[1].value
        // console.log(start_date)
        // console.log(end_date)
        // console.log(input_image)
        form.append('image', input_image.files[0])
        // // form.append('start_datetime', start_date)
        // form.append('end_datetime', end_date)
            
        let header = {'content-type': 'multipart/form-data'}
    
        let p = await callApi('api/newspost/', 'POST', form, header).then(res => {
            if (res.status === 200 || res.status === 201) {
                alert("bạn đã đăng bài thành công")
                resetForm()
            }
            
        })
        
        
        
    }


    return (
        <Card className={classes.Cardroot}>
            <CardHeader
                avatar={
                    <Avatar src={context.dataProfile.avatar} />
                }
                action={
                    <IconButton aria-label="settings">
                        <MoreVert />
                    </IconButton>
                }
                title={`${context.dataProfile.first_name}` + ' '+ `${context.dataProfile.last_name}`}


            />

            <CardContent>

                <form  onSubmit={submitHandle} style={{ width: "100%" }} >
                
                    <div className={classes.post}>
                        <TextField
                            id="outlined-select-currency"
                            select
                            label="Category"
                            // defaultValue="No auction"
                            fullWidth={true}
                            variant="outlined"
                            name="category"
                            onChange={handleChange}
                            error={errors.category}
                            helperText={errors.category ? errors.category : null}
                        >
                            <MenuItem value="">
                                <em>None</em>
                            </MenuItem>
                            <MenuItem key={1} value={1} >
                                Auction
                            </MenuItem>
                            <MenuItem key={2} value={2} >
                                No auction
                            </MenuItem>
                        </TextField>
                    </div>

                    {auction()}

                    <div className={classes.post} >
                        <TextField  type="file" 
                               accept="image/*"
                                variant="outlined"
                                placeholder="ảnh"
                                fullWidth={true}    
                                name="image"
                                // value={state.image}
                                ref={image}
                                onChange={handleChange}
                                error={errors.image}
                                helperText={errors.image ? errors.image : null}
                                />
                        
                    </div>
                    <div className={classes.post}>
                        <TextField
                            required
                            id="outlined-required"
                            label="Title"
                            variant="outlined"
                            fullWidth={true}
                            name="title"
                            // value={state.title}
                            onChange={handleChange}
                            error={errors.title}
                            helperText={errors.title ? errors.title : null}
                        />
                    </div>
                    <div className={classes.post}>
                        <TextField
                            id="outlined-required"
                            label="Hash Tag"
                            variant="outlined"
                            fullWidth={true}
                            name="hashtag"
                            // value={state.title}
                            onChange={handleChange}
                            error={errors.hashtag}
                            helperText={errors.hashtag ? errors.hashtag : "for example: #A #B #c"}
                        />
                    </div>
                    <div className={classes.post}>
                        <TextField
                            id="outlined-multiline-static"
                            label="Description"
                            placeholder="Description"
                            multiline
                            rows={4}
                            variant="outlined"
                            fullWidth={true}
                            name="description"
                            // value={state.description}
                            onChange={handleChange}
                            error={errors.description}
                            helperText={errors.description ? errors.description : null}
                        />
                    </div>

                    <div className={classes.post}>
                        <CKEditor
                            editor={ClassicEditor}
                            data={state.content}
                            // onInit={editor => {
                            //     // You can store the "editor" and use when it's needed.
                            //     console.log('Editor is ready to use!', editor);
                            // }}
                            
                        
                            config={{
                                // extraPlugins: [ MyCustomUploadAdapterPlugin ],
                                ckfinder: {
                                   
                                    uploadUrl: 'http://localhost:8000/api/newspost/ckeditor/upload/'
                                },
                                headers:{'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')}
                            }}
                            name="content"
                            onChange={handleCkEditor}
                            
                        />
                    </div>
                    
                   

                    <div className={classes.button}>
                        <Button variant="contained" color="primary" type='submit' onClick={postNews}>
                            Submit
                        </Button>
                        <Button variant="outlined" type="reset" color="primary" onClick={resetForm} >
                            Reset
                        </Button>
                    </div>
                </form>
                
            </CardContent>
            
        </Card >
    )
}

export default PostCard;