import React from 'react';


const Pagination = (props) => {
    const {pagination, onPageChange} = props
    const {page, limit, totalRow} = pagination
    const handlePageChange = (newPage) =>{
        if(onPageChange){
            onPageChange(newPage)
        }
    }

    const totalPages = Math.ceil(totalRow/limit)

    let items = []
    for(let i = 0; i < totalPages; i++){
        items.push(
            <li  onClick={() => {handlePageChange(i + 1)}}>
                {page === (i + 1) ?  <span aria-current="page"  className="page-numbers current">{i +1}</span> : <a className="page-numbers"  href="#/">{i +1}</a>}
               </li>
        )
    }


        return (
            <div className="pagination-wrapper my-lg-5 mt- py-lg-3 text-center">
            <ul className="page-pagination">
                {page > 1 ? <li onClick={() => handlePageChange(page-1)}><a className="next"  href="#/" ><span className="fa fa-angle-left"></span> Pre</a></li>
                : ""}
                    {items}
                {/* <li onClick={() => handlePageChange(1)}><span aria-current="page"  className="page-numbers current">1</span></li>
                <li  onClick={() => handlePageChange(2)}><a className="page-numbers"  href="#/">2</a></li>
                <li  onClick={() => handlePageChange(3)}><a className="page-numbers"  href="#/">3</a></li>
                <li><a className="page-numbers" href="#/">...</a></li>
                <li><a className="page-numbers" href="#/">15</a></li> */}
                {page < totalPages ? <li onClick={() => handlePageChange(page+1)}><a className="next" href="#/">Next <span className="fa fa-angle-right"></span></a></li>
                : ""}
            </ul>
        </div>
        )
    
}
export default Pagination;