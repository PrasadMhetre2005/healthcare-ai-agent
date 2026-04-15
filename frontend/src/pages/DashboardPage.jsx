import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { MetricCard } from '../components/MetricCard';
import { Alert } from '../components/Alert';
import { Heart, Activity, Droplet, Thermometer, MessageCircle } from 'lucide-react';
import { healthDataService, alertService } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

export const DashboardPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [latestHealth, setLatestHealth] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Get latest health data
        const health = await healthDataService.getLatest(user.id);
        setLatestHealth(health);

        // Get unresolved alerts
        const alertsData = await alertService.getUnresolved(user.id);
        setAlerts(alertsData);
      } catch (error) {
        toast.error('Failed to load dashboard data');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user.id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="flex bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-64">
        <div className="p-8">
          {/* Healthcare AI Branding */}
          <div className="mb-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center gap-4">
              <div className="bg-white/20 p-3 rounded-lg">
                <Heart className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">Healthcare AI</h1>
                <p className="text-blue-100">Your Personal Health Monitoring & AI Assistant</p>
              </div>
            </div>
          </div>

          <Header
            title={`Welcome back, ${user.username}`}
            subtitle="Here's your latest health summary"
          />

          {/* Healthcare AI Consultant Button */}
          <div className="mb-8">
            <button
              onClick={() => navigate('/consultant')}
              className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-lg p-6 shadow-lg transition-all transform hover:scale-105 flex items-center justify-center gap-3"
            >
              <MessageCircle className="w-6 h-6" />
              <span className="text-lg font-semibold">Chat with Healthcare AI Consultant</span>
            </button>
          </div>

          {/* Alerts Section */}
          {alerts.length > 0 && (
            <div className="mb-8 space-y-2">
              {alerts.map((alert) => (
                <Alert
                  key={alert.id}
                  type={alert.severity === 'critical' ? 'danger' : 'warning'}
                  title={alert.title}
                  message={alert.message}
                />
              ))}
            </div>
          )}

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {latestHealth ? (
              <>
                <MetricCard
                  title="Blood Pressure"
                  value={`${latestHealth.blood_pressure_systolic}/${latestHealth.blood_pressure_diastolic}`}
                  unit="mmHg"
                  status={latestHealth.blood_pressure_systolic > 140 ? 'critical' : 'normal'}
                  icon={Heart}
                />
                <MetricCard
                  title="Heart Rate"
                  value={latestHealth.heart_rate}
                  unit="bpm"
                  status={latestHealth.heart_rate > 100 ? 'warning' : 'normal'}
                  icon={Activity}
                />
                <MetricCard
                  title="Blood Glucose"
                  value={latestHealth.blood_glucose}
                  unit="mg/dL"
                  status={latestHealth.blood_glucose > 200 ? 'critical' : 'normal'}
                  icon={Droplet}
                />
                <MetricCard
                  title="Temperature"
                  value={latestHealth.temperature}
                  unit="°C"
                  status={latestHealth.temperature > 37.5 ? 'warning' : 'normal'}
                  icon={Thermometer}
                />
              </>
            ) : (
              <p className="col-span-4 text-gray-600">No health data available yet</p>
            )}
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="card-header">Quick Actions</h3>
              <div className="space-y-3">
                <a href="/health-data" className="block btn btn-primary text-center">
                  Log Health Data
                </a>
                <a href="/insights" className="block btn btn-secondary text-center">
                  View Insights
                </a>
              </div>
            </div>

            <div className="card">
              <h3 className="card-header">Last Updated</h3>
              {latestHealth && (
                <p className="text-gray-600">
                  {new Date(latestHealth.recorded_date).toLocaleString()}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
