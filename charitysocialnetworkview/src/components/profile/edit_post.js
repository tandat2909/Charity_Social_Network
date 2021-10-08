import React, { useContext, useState, useRef, createRef} from 'react';
import { NewsPostContextMod } from '../../context/newspost_mod';
import callApi from '../../utils/apiCaller';
import { styled, alpha } from '@mui/material/styles';
import { makeStyles } from '@material-ui/core/styles';
import { Grid, Paper } from '@mui/material';
import InputBase from '@mui/material/InputBase';
import { CKEditor } from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import { DatePicker, Space } from 'antd';
import moment from 'moment';
import dateFormat from 'dateformat';
import Alert from '@mui/material/Alert';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'left',
        color: theme.palette.text.secondary,
        margin: 15
    },
    div: {
        margin: "10px",

    },
    label: {
        color: "orange",
        fontSize: "20px"
    },
    error:{
        color: "red",
        fontWeight: "600",
        fontFamily: "sans-serif",
        }
}));

const BootstrapInput = styled(InputBase)(({ theme }) => ({
    'label + &': {
        //   marginTop: theme.spacing(3),
    },
    '& .MuiInputBase-input': {
        borderRadius: 4,
        position: 'relative',
        backgroundColor: theme.palette.mode === 'light' ? '#fcfcfb' : '#2b2b2b',
        border: '1.5px solid #9b8d8d3d ',
        fontSize: 18,
        padding: '10px 12px',
        transition: theme.transitions.create([
            'border-color',
            'background-color',
            'box-shadow',
        ]),
        // Use the system font instead of the default Roboto font.
        fontFamily: [
            '-apple-system',
            'BlinkMacSystemFont',
            '"Segoe UI"',
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
            '"Apple Color Emoji"',
            '"Segoe UI Emoji"',
            '"Segoe UI Symbol"',
        ].join(','),
        '&:focus': {
            boxShadow: `${alpha("#FFEB3B", 0.4)} 0 0 0 0.3rem`,
            borderColor: "#FF5722",
        },

    },

}));


const EditPost = (props) => {
    const { RangePicker } = DatePicker;
    const classes = useStyles();
    let detailPost = useContext(NewsPostContextMod)
    let [get_post_success, setGetPostSuccess] = useState(false)
    const [errors, setErrors] = useState({});
    const [post, setPost] = React.useState({
      
    });
    let [messages, setMessages] = useState();
    let date = createRef()
    let image = useRef()

    const GetDetailPost = async () => {
        let url = 'api/newspost/' + props.id.match.params.id + '/'
        let a = await callApi(url, 'GET', null, null).catch(err => { console.log(err) })
        console.log(a)
        detailPost.detail = a.data
        setGetPostSuccess(true)
    }
    if (Object.keys(detailPost.detail).length === 0 || detailPost.detail.id !== props.id.match.params.id) {
        GetDetailPost()
    }


    const validate = (fieldValues = post) =>{
        let temp = { ...errors }
        if('image' in fieldValues) {
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
        if (fieldValues === post)
            return Object.post(temp).every(x => x === "")
        

    }

    const hashTags = (props = detailPost.detail.hashtag) =>
        props && props.map((hashTagItem) => {
            return (
                "#" + `${hashTagItem.name}`
            )
        })
    const handleChange = (event) => {
        console.log("image: ", image.current.getElementsByTagName('input')[0].files[0])
        let input_image = image.current.getElementsByTagName('input')[0]
        const target = event.target;
        const {name, value} = target;
        if(  name !== null && name === 'hashtag')
        {
            setPost({...post,
                hashtag: value.split('#')})
        }   
        // if(name === 'image'){
        //     // console.log(target.files[0])
        //     setPost({...post,
        //         [name]: input_image.files[0],
        //     });
        //     validate({ [name]: value })
        // }
        setPost({...post,
                    [name]: value,
                });
        validate({ [name]: value })
    }
    // const handleChangeImage = (event) => {
    //     setPost({...post,
    //         price_start: event,

    //     })
    // }
    const renderImages = (file) => {
        let file_image = image.current.getElementsByTagName('input')[0].files[0]
        let source = URL.createObjectURL(file_image)
        return <img className="radius-image-full img-fluid mb-5"  style={{ width: "100%" }} src={source} alt="img" />;
       
    }
    const handleChangeDate = (event) => {
        setPost({...post,
            start_datetime: dateFormat(event[0]._d,"yyyy-mm-dd h:MM:ss"),
            end_datetime: dateFormat(event[1]._d,"yyyy-mm-dd h:MM:ss"), 
        
        })
    }
    const handleCkEditor = (event, editor) =>{
        let data = editor.getData();
        setPost({...post,
            content: data
        })
      
    }
    const patchPost = async() => {
            
        let update = {...post}
        let form = new FormData()

        Object.keys(update).forEach((key) =>  {
            if(key === 'hashtag'){
                for(let i = 0; i < update[key].length; i++)
                form.append('hashtag', update[key][i])
            }
            else
                form.append(key,update[key])
        })
        let input_image = image.current.getElementsByTagName('input')[0].files[0]
        form.append('image', input_image)
        let header = {'content-type': 'multipart/form-data'}
        let url = 'api/newspost/' + props.id.match.params.id + '/'
        let p = await callApi(url, 'PATCH', form, header).then(res => {
            if (res.status === 200 || res.status === 201) {
                alert("bạn đã sửa bài thành công")
            }
            
        }).catch(err => {console.log(err.response.data)
            if(err.response.data.start_date)
            {
                setMessages("Ngày bắt đầu phải lớn hơn hoặc bằng ngày hiện tại")
            }
        
        })
    }

    return (
        <>
            {Object.keys(detailPost.detail).length !== 0 ?
                <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                    <Grid item xs={8} className="container pb-lg-4" style={{ margin: "100px auto" }}>
                        <Paper className={classes.paper}>
                        {messages ? <Alert severity="error">{messages}</Alert> : ""}
                            <h4>{detailPost.detail.title}</h4>
                            <div className={classes.div}>
                                <label className={classes.label}>Title</label>
                                <BootstrapInput
                                    name="title"
                                    autoFocus
                                    type="text"
                                    id="outlined-basic"
                                    variant="outlined"
                                    defaultValue={detailPost.detail.title}
                                    fullWidth
                                    onChange={handleChange}
                                />
                                {errors.title ? <label className={classes.error}>{errors.title}</label> : ""}
                            </div>
                            <div className={classes.div}>
                                <label className={classes.label}>Description</label>
                                <BootstrapInput
                                    name="description"
                                    autoFocus
                                    type="text"
                                    id="outlined-basic"
                                    multiline
                                    variant="outlined"
                                    defaultValue={detailPost.detail.description}
                                    fullWidth
                                    onChange={handleChange}
                                />
                                {errors.description ? <label className={classes.error}>{errors.description}</label> : ""}
                            </div>
                            {detailPost.detail.category.id === 1 ? <>
                            <div className={classes.div}>
                                <label className={classes.label}>StartDay - EndDay</label>
                                <Space direction="vertical" size={12} style={{ width: "100%" }}>
                                    <RangePicker
                                        onChange ={handleChangeDate}  
                                        ref={date} 
                                        defaultValue={[moment(new Date(detailPost.detail.info_auction.start_datetime), "YYYY-MM-DD HH:mm:ss"), moment(new Date(detailPost.detail.info_auction.end_datetime),"YYYY-MM-DD HH:mm:ss")]}    
                                        format="YYYY-MM-DD HH:mm:ss" />
                                </Space>

                            </div>

                            <div className={classes.div}>
                            <label className={classes.label}>Price</label>
                                <BootstrapInput
                                    name="price_start"
                                    autoFocus
                                    type="number"
                                    id="outlined-basic"
                                    multiline
                                    variant="outlined"
                                    defaultValue={detailPost.detail.info_auction.price_start}
                                    fullWidth
                                     onChange={handleChange}

                                />
                            </div>
                            </> : ""}
                            <div className={classes.div}>
                                <label className={classes.label}>Image</label>
                                <BootstrapInput
                                    name="image"
                                    autoFocus
                                    type="file"
                                    id="outlined-basic"
                                    variant="outlined"
                                    fullWidth
                                    ref={image}
                                    onChange={handleChange}
                                />
                                {errors.image ? <label className={classes.error}>{errors.image}</label> : ""}
                                <div style={{ width: "20%", margin: "10px 0" }}>
                                    {post.image ? renderImages(post.image) : 
                                    <img src={detailPost.detail.image} className="radius-image-full img-fluid mb-5" alt="" style={{ width: "100%" }} /> }
                                </div>

                            </div>

                            <div className={classes.div}>
                                <label className={classes.label}>HashTag</label>
                                <BootstrapInput
                                    name="hashtag"
                                    autoFocus
                                    type="text"
                                    id="outlined-basic"
                                    variant="outlined"
                                    defaultValue={hashTags()}
                                    fullWidth
                                    error={errors.hashtag}
                                    helperText={errors.hashtag ? errors.hashtag : null}
                                    onChange={handleChange}

                                />
                                {errors.hashtag ? <label className={classes.error}>{errors.hashtag}</label> : ""}
                            </div>
                            <div className={classes.div}>
                                <label className={classes.label}>Content</label>
                                <CKEditor
                                    editor={ClassicEditor}
                                    data={detailPost.detail.content}
                                    config={{
                                        ckfinder: {

                                            uploadUrl: 'http://localhost:8000/api/newspost/ckeditor/upload/'
                                        },
                                        headers: { 'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token') }
                                    }}
                                name="content"
                                onChange={handleCkEditor}

                                />

                            </div>
                            <div style={{width: "50%", margin: "0 auto"}}>
                                <button className="btn btn-style btn-primary ml-lg-3 mr-lg-2" style={{width: "100%"}} onClick={patchPost}>Update</button>
                            </div>
                            
                        </Paper>

                    </Grid>


                </Grid>
                : ""}

        </>
    )
}
export default EditPost;