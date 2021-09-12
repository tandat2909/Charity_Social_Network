
import React, { Component } from 'react';


class LightDark extends Component {


    render() {


        let changeTheme = () => {
            document.documentElement.setAttribute('data-theme', 
                document.documentElement.getAttribute('data-theme') === "light"? "dark":"light");
          
        }
        return (
            <div className="mobile-position" >

                <nav className="navigation">
                    <div className="theme-switch-wrapper" >
                        <label className="theme-switch" htmlFor="checkbox">
                            <input type="checkbox" id="checkbox" />
                            <div className="mode-container" onClick={() => changeTheme()}>
                                <i className="gg-sun"></i>
                                <i className="gg-moon"></i>
                            </div>
                        </label>
                    </div>
                </nav>
            </div>
        )
    }
}

export default LightDark;