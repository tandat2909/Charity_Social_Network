import React, {useContext} from "react";
import Badge from "@material-ui/core/Badge";
import Avatar from "@material-ui/core/Avatar";
import { makeStyles } from "@material-ui/core/styles";
import IconButton from "@material-ui/core/IconButton";
import PhotoCamera from "@material-ui/icons/PhotoCamera";
import { contexts } from "../../context/context"
import { Image } from 'antd';

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    input: {
        display: 'none',
    },
}));

const Avatars = () => {
    let context = useContext(contexts)
    const classes = useStyles();
    return (
        <Badge
            overlap="circular"
            anchorOrigin={{
                vertical: "bottom",
                horizontal: "right"
            }}
            badgeContent={
                <>
                    <div className={classes.root}>
                        <input accept="image/*" className={classes.input} id="icon-button-file" type="file" />
                        <label htmlFor="icon-button-file">
                            <IconButton  aria-label="upload picture" component="span">
                                <PhotoCamera style={{fontSize: "35px", color: '#aba8a8'}}/>
                            </IconButton>
                        </label>
                    </div>
                </>
            }
        >
            <Avatar style={{ width: "200px", height: "200px", borderRadius: '50%', border: ' 5px solid white' }}>
                <Image
                style={{ width: "200px", height: "200px"}}
                alt={context.dataProfile.last_name}
                src={context.dataProfile.avatar} />
            </Avatar>
        </Badge>
    );
}
export default Avatars;