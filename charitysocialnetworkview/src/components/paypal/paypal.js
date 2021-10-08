import React from 'react';
import { PayPalButtons } from "@paypal/react-paypal-js";
import axios from "axios";
// import toast from "react-hot-toast";


const PayPal = (props) => {
    console.log("pays   : ", props)
    let payloads = props.payload
    return (
        <div className="card">
            <img src="https://images.unsplash.com/photo-1594498257673-9f36b767286c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1350&q=80" alt="Airtable product" style={{ width: '100%' }} />
            <div className="card-details">
                <h1>Airtable Product</h1>
                <p className="price">$ {payloads.amount.value}</p>
                <p>Some information about the product</p>
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
                            let auction_item_id = 2
                            // axios({
                            //     method:"POST",
                            //     url: "http://localhost:8000/api/pay/paypal/result/",
                            //     headers: {
                            //       Authorization: "Bearer UaUKZZu23LQCneJTPtItcaScI56Gif"
                            //     },
                            //     data:{...details, auction_item_id:auction_item_id}
                                
                            // })

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
