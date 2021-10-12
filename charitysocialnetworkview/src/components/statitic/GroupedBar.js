import React, { useContext } from 'react';
import { Bar } from 'react-chartjs-2';
import { statistical } from '../../context/statistical';




const options = {
  scales: {
    yAxes: [
      {
        ticks: {
          beginAtZero: true,
        },
      },
    ],
  },
};

const GroupedBar = () => {
  const thong = useContext(statistical);
  console.log("auction: ", thong.auction)
const data = {
  labels: ['9', '10'],
  datasets: [
    {
      label: 'posts',
      data: thong.auction.data.posts,
      backgroundColor: 'rgb(255, 99, 132)',
    },
    {
      label: 'emotions',
      data: thong.auction.data.emotions,
      backgroundColor: 'rgb(54, 162, 235)',
    },
    {
      label: 'comment',
      data: thong.auction.data.comment,
      backgroundColor: 'rgb(75, 192, 192)',
    },
    
  ],
};
return(<>
  <div className='header'>
    <h1 className='title'>Thống kê của loại đấu giá</h1>
  </div>
  <Bar data={data} options={options} />
</>)
  
};

export default GroupedBar;