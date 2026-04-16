import React from 'react';
import { Heart, Home, AlertCircle, Lightbulb, BarChart3, LogOut, MessageCircle } from 'lucide-react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (href) => location.pathname === href;

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
    <div className="w-64 bg-gradient-to-b from-blue-600 via-blue-700 to-blue-800 text-white h-screen flex flex-col fixed left-0 top-0 shadow-2xl">
      {/* Logo */}
      <div className="p-6 border-b-2 border-blue-500/50 bg-black/10 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-white/20 rounded-lg">
            <Heart className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">HealthCare AI</h1>
            <p className="text-xs text-blue-200">Smart Monitoring</p>
          </div>
        </div>
      </div>

      {/* User Info */}
      <div className="p-6 border-b-2 border-blue-500/50 bg-white/5">
        <p className="text-xs text-blue-200 font-medium">Logged in as</p>
        <p className="font-bold text-lg text-white mt-1">{user?.username}</p>
        <div className="mt-3 inline-block px-3 py-1 bg-blue-500/30 rounded-full text-xs font-semibold text-blue-100 capitalize">
          {user?.role}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {/* AI Assistant Section */}
        <div className="mb-6">
          <p className="text-xs text-blue-200 uppercase font-bold px-4 mb-3 mt-4 tracking-wider">🤖 AI Assistant</p>
          {aiNavItems.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium ${
                isActive(item.href)
                  ? 'bg-white/20 text-white shadow-lg border border-white/30'
                  : 'hover:bg-blue-500/40 text-blue-50 hover:text-white'
              }`}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              <span>{item.label}</span>
              {isActive(item.href) && (
                <div className="ml-auto w-2 h-2 bg-white rounded-full animate-pulse" />
              )}
            </Link>
          ))}
        </div>

        {/* Health Monitoring Section */}
        <div className="border-t-2 border-blue-500/30 pt-4">
          <p className="text-xs text-blue-200 uppercase font-bold px-4 mb-3 tracking-wider">📊 Health Monitoring</p>
          {baseNavItems.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 font-medium ${
                isActive(item.href)
                  ? 'bg-white/20 text-white shadow-lg border border-white/30'
                  : 'hover:bg-blue-500/40 text-blue-50 hover:text-white'
              }`}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              <span>{item.label}</span>
              {isActive(item.href) && (
                <div className="ml-auto w-2 h-2 bg-white rounded-full animate-pulse" />
              )}
            </Link>
          ))}
        </div>
      </nav>

      {/* Logout */}
      <div className="p-4 border-t-2 border-blue-500/50 bg-black/10">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 bg-red-600 hover:bg-red-700 rounded-xl transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
        >
          <LogOut className="w-5 h-5 flex-shrink-0" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
};
