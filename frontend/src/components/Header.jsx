import React from 'react';

export const Header = ({ title, subtitle }) => {
  return (
    <div className="mb-8">
      <h1 className="text-4xl font-bold text-gray-900">{title}</h1>
      {subtitle && <p className="text-gray-500 mt-2">{subtitle}</p>}
    </div>
  );
};
