import React, { useContext} from 'react';
import dateFormat from 'dateformat';
import {
     List, ListItem, ListItemText, ListItemAvatar, Avatar, Divider
}
from "@material-ui/core";
import {
    Event, Person, Cake, ContactMail, Home, Phone, Wc,
}
from '@material-ui/icons';
import { contexts } from "../../context/context"


const ListProfile = (props) => {    
    const context = useContext(contexts)
    // let [data,setData] = useState("")
    // const [status, setStatus] = useState(context.dataProfile);
    let date = dateFormat(context.dataProfile.date_joined, "fullDate")
    // let setDataProfile = () =>{
    //     setData(statusProfile)
    //     console.log("ádsd",data)
    //     return data
    // }

    // useEffect(()=>{
    //     if(data !== props.action)
    //         setData(props.action)
    // },[])
   
    
    return (
        <List>
            
            <ListItem>
                <ListItemAvatar>
                    <Avatar>
                        <Cake />
                    </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Birthday" secondary={dateFormat(context.dataProfile.birthday, "fullDate")} ></ListItemText>
            </ListItem>
            <Divider variant="inset" component="li" />
            <ListItem>
                <ListItemAvatar>
                    <Avatar>
                        <ContactMail />
                    </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Email" secondary={context.dataProfile.email} />
            </ListItem>
            <Divider variant="inset" component="li" />
            <ListItem>
                <ListItemAvatar>
                    <Avatar>
                        <Person />
                    </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Name" secondary={`${context.dataProfile.first_name}` + " " + `${context.dataProfile.last_name}`} />
            </ListItem>
            <Divider variant="inset" component="li" />
            <ListItem>
                <ListItemAvatar>
                    <Avatar>
                        <Event />
                    </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Date join" secondary={date} />
            </ListItem>
            <Divider variant="inset" component="li" />
            <ListItem>
                <ListItemAvatar>
                    <Avatar>
                        <Home />
                    </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Address" secondary={context.dataProfile.address} />
            </ListItem>
            <Divider variant="inset" component="li" />
            <ListItem>
                <ListItemAvatar>
                    <Avatar>
                        <Phone />
                    </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Phone number" secondary={context.dataProfile.phone_number} />
            </ListItem>
            <Divider variant="inset" component="li" />
            <ListItem>
                <ListItemAvatar>
                    <Avatar>
                        <Wc />
                    </Avatar>
                </ListItemAvatar>
                <ListItemText primary="Gender" secondary={context.dataProfile.gender} />
            </ListItem>
            <Divider variant="inset" component="li" />

        </List>
    )
}


export default ListProfile;