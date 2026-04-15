import React from 'react';
import { Heart, Home, AlertCircle, Lightbulb, BarChart3, LogOut, MessageCircle } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const baseNavItems = [
    { icon: Home, label: 'Dashboard', href: '/dashboard' },
    { icon: BarChart3, label: 'Health Data', href: '/health-data' },
    { icon: AlertCircle, label: 'Alerts', href: '/alerts' },
    { icon: Lightbulb, label: 'Insights', href: '/insights' },
  ];

  const aiNavItems = [
    { icon: MessageCircle, label: 'Healthcare AI', href: '/consultant' },
  ];

  return (
    <div className="w-64 bg-gradient-to-b from-blue-600 to-blue-800 text-white h-screen flex flex-col fixed left-0 top-0">
      {/* Logo */}
      <div className="p-6 border-b border-blue-500">
        <div className="flex items-center gap-3">
          <Heart className="w-8 h-8" />
          <h1 className="text-2xl font-bold">HealthCare AI</h1>
        </div>
        <p className="text-blue-100 text-sm mt-2">Monitoring System</p>
      </div>

      {/* User Info */}
      <div className="p-6 border-b border-blue-500">
        <p className="text-sm text-blue-100">Logged in as</p>
        <p className="font-semibold text-lg">{user?.username}</p>
        <p className="text-sm text-blue-200 capitalize">{user?.role}</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-6 space-y-2 overflow-y-auto">
        {/* AI Assistant Section */}
        <div>
          <p className="text-xs text-blue-200 uppercase font-semibold px-4 mb-3 mt-2">AI Assistant</p>
          {aiNavItems.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-500 transition-colors duration-200 bg-blue-500/30"
            >
              <item.icon className="w-5 h-5" />
              <span>{item.label}</span>
            </Link>
          ))}
        </div>

        {/* Health Monitoring Section */}
        <div className="mt-6 pt-6 border-t border-blue-500">
          <p className="text-xs text-blue-200 uppercase font-semibold px-4 mb-3">Health Monitoring</p>
          {baseNavItems.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-500 transition-colors duration-200"
            >
              <item.icon className="w-5 h-5" />
              <span>{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>

      {/* Logout */}
      <div className="p-6 border-t border-blue-500">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 bg-red-600 hover:bg-red-700 rounded-lg transition-colors duration-200"
        >
          <LogOut className="w-5 h-5" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
};
