import React, { useContext } from 'react';
import AuthorContact from './author_contact'
import {NewsPostContextMod} from "../../../../context/newspost_mod"


const AuthorInfor = () => {
    let inforUsser = useContext(NewsPostContextMod)
        return (
            <div className="col-md-9 mt-md-0 mt-4">
                <h3 className="mb-3 title">Winner</h3>
                <h5 className="mb-3 title">User name: {inforUsser.detail.info_auction.receiver.username}</h5>
                <p>Name: {`${inforUsser.detail.info_auction.receiver.last_name}` + ' ' + `${inforUsser.detail.info_auction.receiver.first_name}`}
                </p>
                <p>Win with price: {inforUsser.detail.info_auction.price_received}</p>
                <AuthorContact></AuthorContact>
            </div>
        )
    
}
export default AuthorInfor;