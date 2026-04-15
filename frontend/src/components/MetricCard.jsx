import React from 'react';

export const MetricCard = ({ title, value, unit, change, status = 'normal', icon: Icon }) => {
  const statusStyles = {
    normal: 'border-l-4 border-green-500',
    warning: 'border-l-4 border-yellow-500',
    critical: 'border-l-4 border-red-500',
  };

  const changeStyles = {
    up: 'text-red-600',
    down: 'text-green-600',
    neutral: 'text-gray-600',
  };

  return (
    <div className={`card ${statusStyles[status]}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-gray-900">{value}</span>
            <span className="text-gray-500 text-sm">{unit}</span>
          </div>
          {change && (
            <p className={`text-sm mt-2 ${changeStyles[change.direction]}`}>
              {change.direction === 'up' ? '↑' : change.direction === 'down' ? '↓' : '→'} {change.value}%
            </p>
          )}
        </div>
        {Icon && <Icon className="w-8 h-8 text-gray-400" />}
      </div>
    </div>
  );
};
