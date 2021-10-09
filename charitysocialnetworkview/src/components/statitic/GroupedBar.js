import React from 'react';
import { Bar } from 'react-chartjs-2';

const data = {
  labels: ["9", "10"],
  datasets: [
    {
      label: 'posts',
      data: [2,1],
      backgroundColor: 'rgb(255, 99, 132)',
    },
    {
      label: 'emotions',
      data: [3,0],
      backgroundColor: 'rgb(54, 162, 235)',
    },
    {
      label: 'comment',
      data: [25,0],
      backgroundColor: 'rgb(75, 192, 192)',
    },
    
  ],
};

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

const GroupedBar = () => (
  <>
    <div className='header'>
      <h1 className='title'>Post type statistics by month</h1>
    </div>
    <Bar data={data} options={options} />
  </>
);

export default GroupedBar;