import React, { Component } from 'react';
import TeamWrap from './team-wrap';



class Team extends Component {
    render() {
        return (
            <section className="w3l-team-main" id="team">
                <div className="team py-5">
                    <div className="container py-lg-5">
                        <div className="title-content text-center">
                            <h3 className="title-big">Happy Volunteers</h3>
                        </div>
                        <div className="team-row mt-md-5 mt-4">
                            <TeamWrap></TeamWrap>


                            <TeamWrap></TeamWrap>


                            <TeamWrap></TeamWrap>


                            <TeamWrap></TeamWrap>


                            <TeamWrap></TeamWrap>


                            <TeamWrap></TeamWrap>


                            <TeamWrap></TeamWrap>


                            <TeamWrap></TeamWrap>


                            <TeamWrap></TeamWrap>


                            <div className="team-apply">
                                <a href="#url" className="team-title m-0"><span className="fa fa-plus-circle d-block mb-3"></span> Apply for Volunteer</a>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}
export default Team;