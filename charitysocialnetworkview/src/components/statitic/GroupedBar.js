import React from 'react';
import { Bar } from 'react-chartjs-2';

const data = {
  labels: ['1', '2', '3', '4', '5', '6'],
  datasets: [
    {
      label: 'No Auction',
      data: [12, 19, 3, 5, 2, 3],
      backgroundColor: 'rgb(255, 99, 132)',
    },
    {
      label: 'Auction',
      data: [2, 3, 20, 5, 1, 4],
      backgroundColor: 'rgb(54, 162, 235)',
    },
    {
      label: 'The post has been approved',
      data: [3, 10, 13, 15, 22, 30],
      backgroundColor: 'rgb(75, 192, 192)',
    },
    {
        label: 'The post has not been approved',
        data: [3, 10, 13, 15, 22, 30],
        backgroundColor: 'rgb(245, 245, 89)',
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