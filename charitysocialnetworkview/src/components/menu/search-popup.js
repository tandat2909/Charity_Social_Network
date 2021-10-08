
import React, { useState, useContext} from 'react';
import { NewsPostContextMod } from '../../context/newspost_mod';
import callApi from '../../utils/apiCaller';


const SearchPopup = () => {
    let listSearch = useContext(NewsPostContextMod)

    let [valueSearch, setValueSearch] = useState({
        search: ""
    })
    const handleChange = (event) => {
        const target = event.target;
        const {name, value} = target;
        setValueSearch({...valueSearch,
                [name]: value,
            });

        
    }
    const Search = async() =>{
        let url = 'api/newspost/?search=' + valueSearch.search
        let b = await callApi(url, 'GET', null, null)
        listSearch.results = b.data
        listSearch.search = true
    }

    return (
        <div id="search" className="pop-overlay">
            <div className="popup">
                <h4 className="mb-3">Search here</h4>
                <form >
                    <input type="search" placeholder="Enter Keyword" name="search" required="required" autoFocus=""  onChange={handleChange}/>
                    <button type="submit" className="btn btn-style btn-primary" onClick={Search}>Search</button>
                </form>
            </div>
            <a className="close" href="#close">×</a>
        </div>
        )
  
}

export default SearchPopup;