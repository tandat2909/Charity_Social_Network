import SearchRight from './search_right';
import Donate from './donate';
import React, {Component} from 'react';
import { Link } from 'react-router-dom';


class NavItem extends Component {
  render() {
    return (
        <ul className="navbar-nav w-100">
            <li className="nav-item @@home__active">
                <Link className="nav-link" to="/">Home <span className="sr-only">(current)</span></Link>
            </li>
            <li className="nav-item @@about__active">
                <Link className="nav-link" to="/about">About</Link>
            </li>
            <li className="nav-item dropdown @@pages__active">
                <Link className="nav-link dropdown-toggle" to="/" id="navbarDropdown1" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Pages<span className="fa fa-angle-down"></span>
                </Link>
                <div className="dropdown-menu" aria-labelledby="navbarDropdown1">
                    <Link className="dropdown-item @@causes__active" to="/causes">Causes</Link>
                    <Link className="dropdown-item @@donate__active" to="/donate">Donate Now</Link>
                    <Link className="dropdown-item @@error__active" to="/error">404 Error page</Link>
                    <Link className="dropdown-item" to="/landing-single">Landing page</Link>
                </div>
            </li>
            <li className="nav-item dropdown active">
                <Link className="nav-link dropdown-toggle" to="/" id="navbarDropdown1" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Blog<span className="fa fa-angle-down"></span>
                </Link>
                <div className="dropdown-menu" aria-labelledby="navbarDropdown1">
                <Link className="dropdown-item @@b__active" to="/blog">Blog posts</Link>
                <Link className="dropdown-item active" to="/blog-single">Blog single</Link>
                </div>
            </li>
            <li className="nav-item @@contact__active">
                <Link className="nav-link" to="/contact">Contact</Link>
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