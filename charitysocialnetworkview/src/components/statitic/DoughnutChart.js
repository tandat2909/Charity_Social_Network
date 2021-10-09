import React from 'react';
import { Doughnut } from 'react-chartjs-2';

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

const DoughnutChart = () => (
  <>
    <div className='header'>
      <h1 className='title'>Article statistics by type</h1>
      
    </div>
    <Doughnut data={data} />
  </>
);

export default DoughnutChart;