import React from 'react';
import { AlertCircle, AlertTriangle, Info } from 'lucide-react';

export const Alert = ({ type = 'info', title, message, onClose }) => {
  const styles = {
    info: 'bg-blue-50 border-blue-200 text-blue-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    danger: 'bg-red-50 border-red-200 text-red-800',
    success: 'bg-green-50 border-green-200 text-green-800',
  };

  const icons = {
    info: Info,
    warning: AlertTriangle,
    danger: AlertCircle,
    success: AlertCircle,
  };

  const Icon = icons[type];

  return (
    <div className={`card border-l-4 ${styles[type]}`}>
      <div className="flex items-start gap-4">
        <Icon className="w-6 h-6 mt-1 flex-shrink-0" />
        <div className="flex-1">
          {title && <h3 className="font-semibold mb-1">{title}</h3>}
          <p>{message}</p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 flex-shrink-0"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
};
