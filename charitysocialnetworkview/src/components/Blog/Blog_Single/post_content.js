import React, { useContext} from 'react';
import { NewsPostContextMod } from '../../../context/newspost_mod'
import { Link } from 'react-router-dom';
import {Gavel} from '@material-ui/icons';


const PostContent = () => {
    
    let post = useContext(NewsPostContextMod)


    
    
    const deadline = post.detail.category.id === 1 ? new Date(post.detail.info_auction[0].end_datetime).getTime()  :"";
    
   
    return (
        <>
        {/* {post.detail.description.charAt(0).toUpperCase()} */}
            <p className="alphabet mb-4"><span className="big-letter">{post.detail.description.charAt(0).toUpperCase()}</span>{post.detail.description.slice(1, post.detail.description.lenght)}
            </p>
            <div dangerouslySetInnerHTML={{ __html: post.detail.content }}></div>
            {post.detail.category.id === 1 ? <>
                <div className="submit text-center">
                    <Link to={"/blog/" + `${post.detail.id}` + "/auction"} props={post.detail} className="btn btn-primary btn-style mt-4">
                    <Gavel />Auction </Link>
                </div> 
            

              
            
            {/* <Modal visible={isModalVisible} onOk={postAuction} onCancel={handleCancel} >
            <Card className={classes.Cardroot} style={{height: "300px", overflowY: "scroll"}}>
                    <CardHeader
                        avatar={
                            <Avatar src={post.detail.user.avatar} />
                        }
                        action={
                            <IconButton aria-label="settings">
                                <MoreVert />
                            </IconButton>
                        }
                        title={post.detail.user.username}
                        subheader={dateFormat(post.detail.update_date, "fullDate")}
                    />
                   

                    <CardMedia
                        className={classes.media}
                        image={post.detail.image}
                        title={`${post.detail.user.first_name}` + " " + `${post.detail.user.last_name}`}
                    />
                    <CardContent>
                        <h4>{post.detail.title}</h4>
                        <Typography variant="body2" color="textSecondary" component="p" style={{
                            whiteSpace: "pre-wrap", 
                            textOverflow: "ellipsis", 
                            overflow: "hidden", 
                            WebkitLineClamp: "3",
                            WebkitBoxOrient: "vertical",
                            width: "100%", 
                            display: "block", 
                            display: "-webkit-box",
                            height:"16px*1.3*3",
                            textAlign: "justify"
                            }}>
                            {post.detail.description}
                        </Typography>
                    </CardContent>
                </Card>
                  
               <div>
                    <div className={classes.post} >
                        <Countdown title="Time remaining" value={deadline} format="D day, HH:mm:ss" />
                    </div>
                    <div className={classes.post} >
                        <TextField
                            disabled
                            id="outlined-disabled"
                            label="price_start"
                            defaultValue={post.detail.info_auction[0].price_start}
                            variant="outlined"
                            />
                        <TextField
                            disabled
                            id="outlined-disabled"
                            label="price_start"
                            defaultValue={dateFormat(post.detail.info_auction[0].start_datetime, "fullDate")}
                            variant="outlined"
                            />
                    </div>
                </div>

                <div className={classes.post} >
                    <TextField
                        required
                        id="outlined-required"
                        label="Offer"
                        variant="outlined"
                        fullWidth={true}
                        name="offer"
                        onChange={handleChange}
                        // error={errors.title}
                        // helperText={errors.title ? errors.title : null}
                    />
                </div>
                <div className={classes.post} >
                    <TextField
                        required
                        id="outlined-required"
                        label="Discription (optional)"
                        variant="outlined"
                        fullWidth={true}
                        name="discription"
                        onChange={handleChange}
                        // error={errors.title}
                        // helperText={errors.title ? errors.title : null}
                    />
                </div>
                
            </Modal>

            <Paper elevation={3} style={{height: "2    00px", overflowY: "scroll"}}>
                 <div>
                    <Tooltip title={post.detail.historyauction[0].description} arrow placement="top">
                        <Chip deleteIcon={<DoneIcon />} onDelete={handleDelete} avatar={<Avatar src={post.detail.historyauction[0].user.avatar} />}   label={post.detail.historyauction[0].price}/>
                    </Tooltip>
                    <GreenRadio
                        checked={selectedValue === 'c'}
                        onChange={handleChangeRadio}
                        value="c"
                        name="radio-button-demo"
                        inputProps={{ 'aria-label': 'C' }}
                    />
                </div>
                <div>
                    <Chip deleteIcon={<DoneIcon />} onDelete={handleDelete} avatar={<Avatar src="/static/images/avatar/1.jpg" />}   label="Deletable"/>
                    <GreenRadio
                        checked={selectedValue === 'd'}
                        onChange={handleChangeRadio}
                        value="d"
                        name="radio-button-demo"
                        inputProps={{ 'aria-label': 'D' }}
                    />
                </div>
                <div>
                    <Chip deleteIcon={<DoneIcon />} onDelete={handleDelete} avatar={<Avatar src="/static/images/avatar/1.jpg" />}   label="Deletable"/>
                    <GreenRadio
                        checked={selectedValue === 'd'}
                        onChange={handleChangeRadio}
                        value="d"
                        name="radio-button-demo"
                        inputProps={{ 'aria-label': 'D' }}
                    />
                </div>
                <div>
                    <Chip deleteIcon={<DoneIcon />} onDelete={handleDelete} avatar={<Avatar src="/static/images/avatar/1.jpg" />}   label="Deletable"/>
                    <GreenRadio
                        checked={selectedValue === 'd'}
                        onChange={handleChangeRadio}
                        value="d"
                        name="radio-button-demo"
                        inputProps={{ 'aria-label': 'D' }}
                    />
                </div>
                <div>
                    <Chip deleteIcon={<DoneIcon />} onDelete={handleDelete} avatar={<Avatar src="/static/images/avatar/1.jpg" />}   label="Deletable"/>
                    <GreenRadio
                        checked={selectedValue === 'd'}
                        onChange={handleChangeRadio}
                        value="d"
                        name="radio-button-demo"
                        inputProps={{ 'aria-label': 'D' }}
                    />
                </div>
            </Paper>  */}
            </> : ""}    


                       
        </>
    )

}
export default PostContent;