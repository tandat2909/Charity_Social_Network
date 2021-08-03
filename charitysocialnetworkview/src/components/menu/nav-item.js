import SearchRight from './search_right';
import Donate from './donate';
import React, { Component } from 'react';
import { NavLink, Route } from 'react-router-dom';


const MenuLink = ({ label, to, activeOnlyWhenExact }) => {
    return (
        <Route path={to} exact={activeOnlyWhenExact} children={({ match }) => {
            var active = match ? 'active' : '';
            if(label === "Home")
                {

                }
            return (
                <li className={"nav-item " + active}>
                    <NavLink to={to} className='nav-link'>{label}</NavLink>
                </li>
            )
        }}
        ></Route>
    )
}

const MenuLinkS = (pros) => {
    return (
        <Route path={pros.to} exact={pros.activeOnlyWhenExact} children={({ match }) => {
            let active = match ? ' active' : '';

            return (
                <NavItems className={pros.className + active} label={pros.label} to={pros.to} data_toggle={pros.data_toggle}>{pros.children}</NavItems>
            )
        }}
        ></Route>
    )
}
const NavItems = (pros) => {

    const is_dropdown = (b = false) => {
        if (b) {
            return pros.data_toggle === 'dropdown'
        }
        return pros.data_toggle === 'dropdown' ? 'dropdown' : ''

    }
    console.log(pros.className)
    return (
        <li className={"nav-item " + pros.className}  >
            <NavLink className={"nav-link "}
                to={pros.to}
                exact={pros.exact}
                role={pros.role}
                data-toggle={pros.data_toggle}
                aria-haspopup="true"
                aria-expanded="false"
            >
                {pros.label}
                {is_dropdown() ? <span className="fa fa-angle-down"></span> : ''}

            </NavLink>
            {pros.children}
        </li>
    )
}

const DropDownMenu = (pros) => {
    return (
        <div className={"dropdown-menu " + pros.className} >
            {pros.children}
        </div>
    )
}
class NavItem extends Component {
    render() {
        return (
            <ul className="navbar-nav w-100">
                {/* <MenuLink label="About" to="/" activeOnlyWhenExact={true}>
                    
                </MenuLink> */}
                <li className="nav-item @@home__active active" >
                    <NavLink className="nav-link" to="/#" exact >Home <span className="sr-only">(current)</span></NavLink>
                </li>
                {/* <MenuLink label="About" to="/about" activeOnlyWhenExact={false}>
                </MenuLink> */}
                <li className="nav-item @@about__active">
                <NavLink className="nav-link" to="/about">About</NavLink>
            </li>

                {/* <MenuLinkS label="test" to="/test" className='dropdown' data_toggle='dropdown' activeOnlyWhenExact={true}>

                    <DropDownMenu className=''>
                        <NavLink className="dropdown-item " to="/test/causes">Causes</NavLink>
                        <NavLink className="dropdown-item " to="/donate">Donate Now</NavLink>
                    </DropDownMenu>
                </MenuLinkS> */}


                {/* <NavItems classname="dropdown">
                    <NavLink className="nav-link"
                        to="/"
                        exact
                        role="button"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                    >
                        Menutest
                        <span className="fa fa-angle-down"></span>
                    </NavLink>
                    <DropDownMenu>
                        <NavLink className="dropdown-item " to="/causes">Causes</NavLink>
                        <NavLink className="dropdown-item " to="/donate">Donate Now</NavLink>
                    </DropDownMenu>
                </NavItems> */}


                <li className="nav-item dropdown @@pages__active">
                    <NavLink className="nav-link dropdown-toggle" to="/" id="navbarDropdown11" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Pages<span className="fa fa-angle-down"></span>
                    </NavLink>
                    <div className="dropdown-menu" aria-labelledby="navbarDropdown1">
                        <NavLink className="dropdown-item @@causes__active" to="/causes">Causes</NavLink>
                        <NavLink className="dropdown-item @@donate__active" to="/donate">Donate Now</NavLink>
                        <NavLink className="dropdown-item @@error__active" to="/error">404 Error page</NavLink>
                        <NavLink className="dropdown-item" to="/landing-single">Landing page</NavLink>
                    </div>
                </li>
                <li className="nav-item dropdown active">
                    <NavLink className="nav-link dropdown-toggle" to="/" id="navbarDropdown1" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Blog<span className="fa fa-angle-down"></span>
                    </NavLink>
                    <div className="dropdown-menu" aria-labelledby="navbarDropdown1">
                        <NavLink className="dropdown-item @@b__active" to="/blog">Blog posts</NavLink>
                        <NavLink className="dropdown-item active" to="/blog-single">Blog single</NavLink>
                    </div>
                </li>
                <li className="nav-item @@contact__active">
                    <NavLink className="nav-link" to="/contact">Contact</NavLink>
                </li>
                <li className="ml-lg-auto mr-lg-0 m-auto">
                    {/* <!--/search-right--> */}
                    <SearchRight></SearchRight>

                </li>

                <Donate></Donate>
            </ul>
        )
    }
}

export default NavItem;