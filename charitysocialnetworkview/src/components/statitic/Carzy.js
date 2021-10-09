import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';

const rand = () => Math.floor(Math.random() * 255);

const genData = () => ({
  labels: ['9', '10'],
  datasets: [
    {
      type: 'line',
      label: 'posts',
      borderColor: `rgb(${rand()}, ${rand()}, ${rand()})`,
      borderWidth: 2,
      fill: false,
      data: [4, 6],
    },
    {
      type: 'bar',
      label: 'emotions',
      backgroundColor: `rgb(${rand()}, ${rand()}, ${rand()})`,
      data: [0,0],
      borderColor: 'white',
      borderWidth: 2,
    },
    {
      type: 'bar',
      label: 'comment',
      backgroundColor: `rgb(${rand()}, ${rand()}, ${rand()})`,
      data: [0,0],
    },
  ],
});

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

const Crazy = () => {
  const [data, setData] = useState(genData());

  useEffect(() => {
    const interval = setInterval(() => setData(genData()), 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <div className='header'>
        <h1 className='title'>Crazy Chart</h1>
        
      </div>
      <Bar data={data} options={options} />
    </>
  );
};

export default Crazy;