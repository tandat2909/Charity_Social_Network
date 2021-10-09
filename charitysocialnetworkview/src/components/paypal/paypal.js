import React, {useContext} from 'react';
import { PayPalButtons } from "@paypal/react-paypal-js";
// import axios from "axios";
import callApi from '../../utils/apiCaller';
import { recerpt } from '../../context/recerpt';
// import toast from "react-hot-toast";


const PayPal = (props) => { 
    let detail = useContext(recerpt)
    console.log("pays   : ", props)
    let payloads = props.payload
    return (
        <div className="card">
            <img src="https://images.unsplash.com/photo-1594498257673-9f36b767286c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1350&q=80" alt="Airtable product" style={{ width: '100%' }} />
            <div className="card-details">
                <h5>{detail.detailRecerpt.item}</h5>
                <p className="price">$ {payloads.amount.value}</p>
                <p>{detail.detailRecerpt.author}</p>
                <PayPalButtons
                    style={{ layout: "horizontal" }}
                    createOrder={(data, actions) => {
                        return actions.order.create({
                            purchase_units: [
                                {
                                    amount: payloads.amount,
                                    custom_id: payloads.custom_id // the name or slug of the thing you're selling
                                },
                            ],
                        });
                    }}
                    onApprove={(data, actions) => {
                        return actions.order.capture().then(function (details) {
                            console.log(details)
                            alert("You winner")
                            // toast.success('Payment completed. Thank you, ' + details.payer.name.given_name + ' ' +details.payer.name.surname)
                            let data = {...details, auction_item_id: props.auction_item_id}
                            let a =  callApi("api/pay/paypal/result/", 'POST', data, null)
                         

                        });
                    }}
                    onCancel={() => 
                        alert("You cancelled the payment. Try again by clicking the PayPal button")
                        // duration: 6000,
                    }
                    onError={(err) => {
                        alert("There was an error processing your payment. If this error please contact support.")
                        // toast.error(
                        //     "There was an error processing your payment. If this error please contact support.", {
                        //     duration: 6000,
                        // });
                    }}
                />
            </div>
        </div>
    )
}
export default PayPal;
