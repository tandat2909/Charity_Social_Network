import React from 'react';
import VisibilityIcon from '@material-ui/icons/Visibility';
import dateFormat from 'dateformat';

const CausesItem = (props) => {

    return (

        <div className="col-lg-4 col-md-6 causes-grid">
            <div className="causes-grid-info">
                <a href="#cause" className="cause-title-wrap">
                    <div style={{display: "flex"}}>
                    <p className="title">{props.category.name} </p> <VisibilityIcon/>
                   </div>
                    <h4 className="cause-title">{props.title}
                    </h4>
                    <p className="counter-inherit">
                        {dateFormat(props.dateCreate, "fullDate")}
                    </p>
                </a>
                <div style={{width: "100%", height:"30%"}}>
                <img src={props.image}  
                    alt="" /></div>
            </div>
        </div>

    )

}
export default CausesItem;