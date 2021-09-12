import React, { useState } from 'react';
// import PropTypes from 'prop-types';

// Pagination.propTypes = {
//     pagination: propTypes.object.isRequest,
//     onPageChange: propTypes.func
// }

// Pagination.defaultProps = {
//     onPageChange: null,
// }

const Pagination = (props) => {
    const {pagination, onPageChange} = props
    const {page, limit, totalRow} = pagination
    const handlePageChange = (newPage) =>{
        if(onPageChange){
            onPageChange(newPage)
        }
    }

    const totalPages = Math.ceil(totalRow/limit)

        return (
            <div className="pagination-wrapper my-lg-5 mt- py-lg-3 text-center">
            <ul className="page-pagination">
                {page > 1 ? <li onClick={() => handlePageChange(page-1)}><a className="next"  ><span className="fa fa-angle-left"></span> Pre</a></li>
                : ""}
                
                <li onClick={() => handlePageChange(1)}><span aria-current="page"  className="page-numbers current">1</span></li>
                <li  onClick={() => handlePageChange(2)}><a className="page-numbers" >2</a></li>
                <li  onClick={() => handlePageChange(3)}><a className="page-numbers" >3</a></li>
                <li><a className="page-numbers" href="#url">...</a></li>
                <li><a className="page-numbers" href="#url">15</a></li>
                {page < totalPages ? <li onClick={() => handlePageChange(page+1)}><a className="next" >Next <span className="fa fa-angle-right"></span></a></li>
                : ""}
            </ul>
        </div>
        )
    
}
export default Pagination;