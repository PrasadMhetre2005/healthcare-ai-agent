import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export const LineGraph = ({ data, dataKey, title, xAxisKey = 'date' }) => {
  return (
    <div className="card">
      <h3 className="card-header">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey={dataKey} stroke="#0ea5e9" isAnimationActive />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export const BarGraph = ({ data, dataKey, title, xAxisKey = 'date' }) => {
  return (
    <div className="card">
      <h3 className="card-header">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey={dataKey} fill="#0ea5e9" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
