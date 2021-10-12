import React, { useContext, useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { statistical } from '../../context/statistical';

const rand = () => Math.floor(Math.random() * 255);



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
  const thong = useContext(statistical);
  const genData = () => ({
    labels: ['9', '10'],
    datasets: [
      {
        type: 'line',
        label: 'posts',
        borderColor: `rgb(${rand()}, ${rand()}, ${rand()})`,
        borderWidth: 2,
        fill: false,
        data: thong.noAuction.data.posts,
      },
      {
        type: 'bar',
        label: 'emotions',
        backgroundColor: `rgb(${rand()}, ${rand()}, ${rand()})`,
        data: thong.noAuction.data.emotions,
        borderColor: 'white',
        borderWidth: 2,
      },
      {
        type: 'bar',
        label: 'comment',
        backgroundColor: `rgb(${rand()}, ${rand()}, ${rand()})`,
        data: thong.noAuction.data.comment,
      },
    ],
  });
  const [data, setData] = useState(genData());

  useEffect(() => {
    const interval = setInterval(() => setData(genData()), 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <div className='header'>
        <h1 className='title'>Thống kê của loại không đấu giá</h1>
        
      </div>
      <Bar data={data} options={options} />
    </>
  );
};

export default Crazy;