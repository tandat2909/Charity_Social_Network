import React, { useContext } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { statistical } from '../../context/statistical';

const data = {
  
  labels: ['No Auction', 'Auction', ],
  datasets: [
    {
      label: '# of Votes',
      data: [10,3],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
      
        
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
      ],
      borderWidth: 1,
    },
  ],
};

const DoughnutChart = () => {
  const thong = useContext(statistical);
  const data = {
  
    labels: ['No Auction', 'Auction', ],
    datasets: [
      {
        label: '# of Votes',
        data: [thong.noAuction.total,thong.auction.total],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
        
          
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };
  
  return(
  <>
    <div className='header'>
      <h1 className='title'>tổng phần trăm của đấu giá và không đấu giá</h1>
      
    </div>
    <Doughnut data={data} />
  </>
  )
}
;

export default DoughnutChart;