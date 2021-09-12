import React, { Component } from 'react';


class TeamWrap extends Component {
    render() {
        return (
            <div className="team-wrap">
                <div className="team-member text-center">
                    <div className="team-img">
                        <img src={process.env.PUBLIC_URL + '/images/team1.jpg'} alt="" className="radius-image img-fluid" />
                    </div>
                    <a href="#url" className="team-title">Luke jacobs</a>
                    <p>Volunteers</p>
                </div>
            </div>
        )
    }
}
export default TeamWrap;