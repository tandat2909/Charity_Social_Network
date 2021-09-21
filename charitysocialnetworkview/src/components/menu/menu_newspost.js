import React, { useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';
import {EventBusy, EventNote, Gavel, EventAvailable, BorderAll} from '@material-ui/icons';


const useStyles = makeStyles({
  root: {
    width: 500,
  },
});

export default function MenuCategory(props) {
  const classes = useStyles();
  const [value, setValue] = useState(0);

    






  return (
    <BottomNavigation
      value={value}
      onChange={(event, newValue) => {
        setValue(newValue);
      }}
      showLabels
      className={classes.root}
    >
        <BottomNavigationAction onClick={()=>props.onClickMenu('all')} label="All" icon={<BorderAll />} />
        <BottomNavigationAction onClick={()=>props.onClickMenu('auction')} label="Auction" icon={<Gavel />} />
        <BottomNavigationAction onClick={()=>props.onClickMenu('noauction')} label="No Auction" icon={<EventNote />} />
        <BottomNavigationAction onClick={()=>props.onClickMenu('eventavailable')} label="EventAvailable" icon={<EventAvailable/>} />
        <BottomNavigationAction onClick={()=>props.onClickMenu('eventbusy')} label="EventBusy" icon={<EventBusy/>} />
    </BottomNavigation>
  );
}
