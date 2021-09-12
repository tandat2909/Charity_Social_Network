import React from 'react';
import InnerBanner from '../banner/inner_banner';
import BannerImage from '../banner/banner-bottom-shape';
import '../../css/error.css';
import { Link} from 'react-router-dom';


const AuthorizationRequired = () => {
  return (
    <div >
      <InnerBanner></InnerBanner>
      <BannerImage></BannerImage>
      <section id="error" className="w3l-error py-5 text-center">
        <div className="container py-lg-4 py-md-3">
            <div className="error-grid">
                <h1 className="error-title">4<span className="fa fa-heart-o"></span>1</h1>
                <h2>Authorization Required</h2>
                <p className="mt-4">Sorry, we're offline right now to make our site even better. Please, come back later and
                    check what we've been up to.
                </p>
                <Link to="/login" className="btn btn-style btn-outline-primary mt-md-5 mt-4"> Back to login</Link>
            </div>
        </div>
    </section>
    </div>
  )

}
export default AuthorizationRequired;