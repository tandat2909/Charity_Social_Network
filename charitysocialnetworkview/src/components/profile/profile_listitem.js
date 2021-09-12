import React, { Component } from 'react';


const ProfileListItem = () => {
    return (
        <>
            <ListItem>
                <ListItemAvatar>
                    <Avatar>
                        <CakeIcon />
                    </Avatar>
                </ListItemAvatar>
                <ListItemText primary="birthday" secondary={profile.birthday} />
            </ListItem>
            <Divider variant="inset" component="li" />
        </>
    )
}
export default ProfileListItem;