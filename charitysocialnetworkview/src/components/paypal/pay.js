import { PayPalScriptProvider } from "@paypal/react-paypal-js";
// import { Toaster } from "react-hot-toast";
// import { Payment } from './components/Payment'
import { useState, useEffect } from "react";
import callApi from "../../utils/apiCaller";
import PayPal from "./paypal";


const Pay = () =>{
   
  
  let [data, setData] = useState({
        amount: {
          // currency_code:string
          value: 5
        },
        custom_id: "chó đạt"
      //   client_id: string
        
      })
//   useEffect(() => {

//     if (data === undefined) {
//         let pay =  await callApi("api/pay/info-payment/2/", 'GET', null, null).then(res => {
//             if (res.status === 200 || res.status === 201) {
//                 alert("bạn đã duyệt bài thành công")
//                 setData(res.data)
//             }
//             else    
//                 alert("bạn đã sửa thất bại")
          
            
//         })
//     // }
//     //   axios({
//     //     method: "GET",
//     //     url: "http://localhost:8000/api/pay/info-payment/2/",
//     //     headers: {
//     //       Authorization: "Bearer UaUKZZu23LQCneJTPtItcaScI56Gif"
//     //     }
//     //   }).then(res => {
//     //     console.log(res.data)
//     //     setData(res.data)
//     //   })
//     }
//   }, [data, setData])
  let render = () =>
    data === undefined ? <></> : <PayPalScriptProvider options={{ "client-id": "AVH5Y-MbuPj2BhIGTqye7D9GBip0PDfYVSOn87AVZUx4VVJ88CVxgrCOkcCERyWsF2nAnsrqKOpwrgVv" }}>
      {/* {console.log(data.client_id)} */}

      {/* <Toaster position="top-center" /> */}
      <PayPal payload = {data} />
    </PayPalScriptProvider>

  return render()
    
  
}
export default Pay;