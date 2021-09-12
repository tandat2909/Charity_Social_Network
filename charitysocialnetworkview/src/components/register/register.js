import React, { Component } from 'react';

class Register extends Component {
    render() {
        return (
            <>
                <div className="header">
                    <h1>Save Poor Register</h1>
                </div>
                <div className="w3-main">

                    <div className="about-bottom main-agile book-form">
                        <div className="alert-close"> </div>
                        <h2 className="tittle">Register Here</h2>
                        <form action="#" method="post">
                            <div className="form-date-w3-agileits">
                                <label> Name </label>
                                <input type="text" name="name" placeholder="Your Name" required="" />
                                <label> Email </label>
                                <input type="email" name="email" placeholder="Your Email" required="" />
                                <label> Password </label>
                                <input type="password" name="password" placeholder="Your Password" required="" />
                                <label> CONFIRM Password </label>
                                <input type="password" name="password" placeholder="Confirm Password" required="" />
                            </div>
                            <div className="make wow shake">
                                <input type="submit" value="Register" />
                            </div>
                        </form>
                    </div>

                </div>
            </>
        )
    }
}
export default Register;
