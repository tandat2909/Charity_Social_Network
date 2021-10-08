import SearchRight from './search_right';
import Donate from './donate';
import React, {  useContext } from 'react';
import { NavLink, Route } from 'react-router-dom';
import { contexts } from '../../context/context';
import ProfileMenu from './menu_profile';
import ShowMessage from './message';



const MenuLink = ({ label, to, activeOnlyWhenExact }) => {
    return (
        <Route path={to} exact={activeOnlyWhenExact} children={({ match }) => {
            var active = match ? 'active' : '';
            if (label === "Home") {
                return (
                    <li className={"nav-item " + active}>
                        <NavLink to={to} className='nav-link'>{label}</NavLink>
                        <span className="sr-only">(current)</span>
                    </li>
                )
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
const NavItem = () => {

    let context = useContext(contexts)
    let {authorization } = context
    const headerUser = ()=>{
        console.log(authorization)
        if(authorization)
            return(
                <>
                    {/* <MenuLink label="Profile" to="/profile" activeOnlyWhenExact={false}>
                    </MenuLink>
                    <MenuLink label="ChatRoom" to="/chat" activeOnlyWhenExact={false}>
                    </MenuLink> */}
                    <ProfileMenu></ProfileMenu>
                    <ShowMessage></ShowMessage>
                </>
                
            )
        else
            return(
                    <MenuLink label="Login" to="/login" activeOnlyWhenExact={false}>
                    </MenuLink>
            )
        
    }
  
    

    return (
        <ul className="navbar-nav w-100">
            {/* { this.showMenu(menus)} */}
            <MenuLink label="Home" to="/" activeOnlyWhenExact={true}>
            </MenuLink>

            <MenuLink label="About" to="/about" activeOnlyWhenExact={false}>
            </MenuLink>


            <MenuLinkS label="Pages" to="/pages/causes" className='dropdown' data_toggle='dropdown' activeOnlyWhenExact={false}>
                <DropDownMenu className=''>
                    <NavLink className="dropdown-item " to="/pages/causes">Causes</NavLink>
                    <NavLink className="dropdown-item " to="/pages/donate">Donate Now</NavLink>
                </DropDownMenu>
            </MenuLinkS>

            <MenuLinkS label="Blog" to="#" className='dropdown' data_toggle='dropdown' activeOnlyWhenExact={false}>
                <DropDownMenu className=''>
                    <NavLink className="dropdown-item " to="/blog_posts">Blog posts</NavLink>
                    <NavLink className="dropdown-item " to="/blog_single">Blog single</NavLink>
                </DropDownMenu>
            </MenuLinkS>

            <MenuLink label="Contact" to="/contact" activeOnlyWhenExact={false}>
            </MenuLink>
            {console.log(authorization)}
           

           

            <li className="ml-lg-auto mr-lg-0 m-auto">
                {/* <!--/search-right--> */}
                <SearchRight></SearchRight>

            </li>

            <Donate></Donate>
            
            {headerUser()}
            
        </ul>
    )

}

export default NavItem;