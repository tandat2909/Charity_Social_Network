
import React, { useContext, useState } from 'react';
import ListSubheader from '@mui/material/ListSubheader';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import { makeStyles } from "@material-ui/core/styles";
import { contexts } from "../../context/context"
import callApi from '../../utils/apiCaller';
import { Dialog, DialogContent, DialogContentText, DialogTitle, Slide} from '@mui/material';
import { Image } from 'antd';


const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper,
  },
  imageList: {
    width: 500,
    height: 450,
  },
  imageListDialog: {
    width: 600,
    height: 450,
  }
}));

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});
const ListImage = () => {

  let context = useContext(contexts)
  const [reload, setReload] = useState(false);
  const classes = useStyles();
  const getListImage = async () => {
    let url = 'api/newspost/get-all-image-post-user/' + context.dataProfile.id + '/?page_size=9'
    let url2 = 'api/newspost/get-all-image-post-user/' + context.dataProfile.id + '/'
    let a = await callApi(url, 'GET', null, null)
    let b = await callApi(url2, 'GET', null, null)
    context.imagePost = a.data.results
    context.imagePostAll = b.data.results
    console.log("list img: ", context.imagePost)
    setReload(true)
  }
  if (context.imagePost.length === 0)
    getListImage()



    const [open, setOpen] = useState(false);

    const handleClickOpen = () => {
      setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
    };

    
  return (
    <>
      <div className={classes.root}>
        <ImageList rowHeight={160} className={classes.imageList} cols={3}>
          <ImageListItem key="Subheader" cols={1} style={{ height: 'auto' }}>
            <ListSubheader component="div">Image</ListSubheader>
          </ImageListItem>
          <ImageListItem key="Subheader" cols={2} style={{ height: 'auto' }}>
            <ListSubheader component="div" onClick={handleClickOpen}>All</ListSubheader>
          </ImageListItem>
          {context.imagePost.length > 0 && context.imagePost.map((item) =>
            <ImageListItem key={item.id} cols={1} >
              <img src={item.image} alt={item.image} />
            </ImageListItem>
          )
          }
        </ImageList>
      </div>


      <Dialog
        fullWidth
        open={open}
        TransitionComponent={Transition}
        keepMounted
        onClose={handleClose}
        aria-describedby="alert-dialog-slide-description"
      >
        <DialogTitle>{"Thư viện ảnh"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-slide-description">
            <ImageList sx={{height: 450 }} variant="woven" cols={4} gap={8}>
                {context.imagePostAll.length > 0 && context.imagePostAll.map((item) =>
                <ImageListItem key={item.id} cols={1} >
                  <img 
                     src={`${item.image}?w=161&fit=crop&auto=format`}
                     srcSet={`${item.image}?w=161&fit=crop&auto=format&dpr=2 2x`}
                     alt={item.image}
                     loading="lazy"
                  />
                </ImageListItem>
              )
              }
            </ImageList>
          </DialogContentText>
        </DialogContent>
      </Dialog>
    </>
  );
}
export default ListImage;