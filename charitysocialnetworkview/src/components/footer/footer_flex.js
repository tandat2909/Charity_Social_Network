import React, { Component } from 'react';


class FooterFlex extends Component{
    render() {
        return(
            <div className="footers14-bottom d-flex">
                      <div className="copyright">
                          <p>© 2020 Save Poor. All rights reserved. Design by <a href="https://w3layouts.com/"
                                  target="_blank" rel = "noreferrer">Quỳnh Quỳnh</a></p>
                      </div>
                      <div className="language-select d-flex">
                          <span className="fa fa-language" aria-hidden="true"></span>
                          <select>
                              <option>English</option>
                              <option>Estonina</option>
                              <option>Deutsch</option>
                              <option>Nederlan;ds</option>
                          </select>
                      </div>
                  </div>
        )
    }
}
export default FooterFlex;