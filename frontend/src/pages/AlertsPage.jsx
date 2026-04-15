import React, { useState, useEffect } from 'react';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Alert } from '../components/Alert';
import { AlertCircle, CheckCircle } from 'lucide-react';
import { alertService } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

export const AlertsPage = () => {
  const { user } = useAuth();
  const [allAlerts, setAllAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
  }, [user.id]);

  const fetchAlerts = async () => {
    try {
      const alerts = await alertService.getAlerts(user.id);
      setAllAlerts(alerts);
    } catch (error) {
      toast.error('Failed to load alerts');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleResolveAlert = async (alertId) => {
    try {
      await alertService.resolveAlert(alertId);
      toast.success('Alert marked as resolved');
      await fetchAlerts();
    } catch (error) {
      toast.error('Failed to resolve alert');
      console.error(error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  const unresolved = allAlerts.filter((a) => !a.is_resolved);
  const resolved = allAlerts.filter((a) => a.is_resolved);

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'danger';
      case 'high':
        return 'warning';
      default:
        return 'info';
    }
  };

  return (
    <div className="flex bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-64">
        <div className="p-8">
          <Header
            title="Health Alerts"
            subtitle="Monitor your health alerts and notifications"
          />

          {/* Unresolved Alerts */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Active Alerts</h3>
            {unresolved.length > 0 ? (
              <div className="space-y-3">
                {unresolved.map((alert) => (
                  <div key={alert.id} className="card border-l-4 border-red-500">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-4 flex-1">
                        <AlertCircle className="w-6 h-6 text-red-600 mt-1 flex-shrink-0" />
                        <div>
                          <h4 className="font-semibold text-gray-900">{alert.title}</h4>
                          <p className="text-gray-600 mt-1">{alert.message}</p>
                          <div className="mt-2 flex items-center gap-2">
                            <span className="text-xs text-gray-500">
                              {new Date(alert.created_at).toLocaleString()}
                            </span>
                            <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                              alert.severity === 'critical'
                                ? 'bg-red-100 text-red-800'
                                : alert.severity === 'high'
                                ? 'bg-yellow-100 text-yellow-800'
                                : 'bg-blue-100 text-blue-800'
                            }`}>
                              {alert.severity.toUpperCase()}
                            </span>
                          </div>
                        </div>
                      </div>
                      <button
                        onClick={() => handleResolveAlert(alert.id)}
                        className="btn btn-secondary flex-shrink-0"
                      >
                        Resolve
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="card">
                <p className="text-gray-600 text-center py-8">✓ No active alerts</p>
              </div>
            )}
          </div>

          {/* Resolved Alerts */}
          {resolved.length > 0 && (
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Resolved Alerts</h3>
              <div className="space-y-3">
                {resolved.map((alert) => (
                  <div key={alert.id} className="card border-l-4 border-green-500 opacity-75">
                    <div className="flex items-start gap-4">
                      <CheckCircle className="w-6 h-6 text-green-600 mt-1 flex-shrink-0" />
                      <div>
                        <h4 className="font-semibold text-gray-900">{alert.title}</h4>
                        <p className="text-gray-600 mt-1">{alert.message}</p>
                        <div className="mt-2 text-xs text-gray-500">
                          Resolved at {new Date(alert.resolved_at).toLocaleString()}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
