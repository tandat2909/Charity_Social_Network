import React, { Component } from 'react';



class AuthorContact extends Component {
    render() {
        return (
            <ul className="author-icons mt-4">
                <li><a className="facebook" href="#url">{null}<span className="fa fa-facebook" aria-hidden="true"></span></a> </li>
                <li><a className="twitter" href="#url">{null}<span className="fa fa-twitter" aria-hidden="true"></span></a></li>
                <li><a className="linkedin" href="#url">{null}<span className="fa fa-linkedin" aria-hidden="true"></span></a></li>
                <li><a className="github" href="#url">{null}<span className="fa fa-github" aria-hidden="true"></span></a>
                </li>
                <li><a className="dribbble" href="#url">{null}<span className="fa fa-dribbble" aria-hidden="true"></span></a></li>
            </ul>
        )
    }
}
export default AuthorContact;