import axios from 'axios';
import * as Config from './../constants/config';

export default function callApi(endpoint, method = "GET", body, headers){
  console.log({...headers,
    'Authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')
  },)
    return axios({
        method: method,
        headers: {...headers,
          'authorization': localStorage.getItem('token_type') + ' ' + localStorage.getItem('access_token')
        },
        url: `${Config.API_URL}/${endpoint}`,
        data: body
      })
};