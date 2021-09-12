import React, { useContext } from 'react';
import AuthorContact from './author_contact'
import {NewsPostContextMod} from "../../../../context/newspost_mod"


const AuthorInfor = () => {
    let inforUsser = useContext(NewsPostContextMod)
        return (
            <div className="col-md-9 mt-md-0 mt-4">
                <h3 className="mb-3 title">{`${inforUsser.detail.user.last_name}` + ' ' + `${inforUsser.detail.user.first_name}`}</h3>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident, sed et excepturi.
                    Distinctio fugit odit? Fugit ipsam. Lorem ipsum dolor sit. Phasellus lacinia id, sunt in
                    culpa quis.
                </p>
                <AuthorContact></AuthorContact>
            </div>
        )
    
}
export default AuthorInfor;