import React from 'react';
import { Doughnut } from 'react-chartjs-2';

const data = {
  labels: ['No Auction', 'Auction', 'The post has been approved', 'The post has not been approved'],
  datasets: [
    {
      label: '# of Votes',
      data: [12, 19, 3, 5],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        
      ],
      borderWidth: 1,
    },
  ],
};

const DoughnutChart = () => (
  <>
    <div className='header'>
      <h1 className='title'>Article statistics by type</h1>
      
    </div>
    <Doughnut data={data} />
  </>
);

export default DoughnutChart;