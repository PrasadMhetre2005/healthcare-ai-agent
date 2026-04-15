import React, { useState, useEffect } from 'react';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { LineGraph } from '../components/Charts';
import { healthDataService } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

export const HealthDataPage = () => {
  const { user } = useAuth();
  const [healthRecords, setHealthRecords] = useState([]);
  const [formData, setFormData] = useState({
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    heart_rate: '',
    temperature: '',
    blood_glucose: '',
    weight: '',
    height: '',
    symptoms: '',
    source: 'manual_entry',
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const records = await healthDataService.getRecords(user.id);
        setHealthRecords(records);
      } catch (error) {
        toast.error('Failed to load health data');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user.id]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await healthDataService.logHealthData({
        ...formData,
        blood_pressure_systolic: formData.blood_pressure_systolic ? parseFloat(formData.blood_pressure_systolic) : null,
        blood_pressure_diastolic: formData.blood_pressure_diastolic ? parseFloat(formData.blood_pressure_diastolic) : null,
        heart_rate: formData.heart_rate ? parseFloat(formData.heart_rate) : null,
        temperature: formData.temperature ? parseFloat(formData.temperature) : null,
        blood_glucose: formData.blood_glucose ? parseFloat(formData.blood_glucose) : null,
        weight: formData.weight ? parseFloat(formData.weight) : null,
        height: formData.height ? parseFloat(formData.height) : null,
      });

      toast.success('Health data logged successfully');
      setFormData({
        blood_pressure_systolic: '',
        blood_pressure_diastolic: '',
        heart_rate: '',
        temperature: '',
        blood_glucose: '',
        weight: '',
        height: '',
        symptoms: '',
        source: 'manual_entry',
      });

      // Refresh data
      const records = await healthDataService.getRecords(user.id);
      setHealthRecords(records);
    } catch (error) {
      toast.error('Failed to log health data');
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

  // Prepare chart data
  const chartData = healthRecords.slice(0, 30).reverse().map((record) => ({
    date: new Date(record.recorded_date).toLocaleDateString(),
    heart_rate: record.heart_rate,
    temperature: record.temperature,
    blood_glucose: record.blood_glucose,
  }));

  return (
    <div className="flex bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-64">
        <div className="p-8">
          <Header
            title="Health Data"
            subtitle="Log and track your health metrics"
          />

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Form */}
            <div className="lg:col-span-1">
              <div className="card">
                <h3 className="card-header">Log Health Metrics</h3>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        BP Systolic
                      </label>
                      <input
                        type="number"
                        value={formData.blood_pressure_systolic}
                        onChange={(e) =>
                          setFormData({ ...formData, blood_pressure_systolic: e.target.value })
                        }
                        className="input-field"
                        placeholder="mmHg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        BP Diastolic
                      </label>
                      <input
                        type="number"
                        value={formData.blood_pressure_diastolic}
                        onChange={(e) =>
                          setFormData({ ...formData, blood_pressure_diastolic: e.target.value })
                        }
                        className="input-field"
                        placeholder="mmHg"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Heart Rate
                    </label>
                    <input
                      type="number"
                      value={formData.heart_rate}
                      onChange={(e) => setFormData({ ...formData, heart_rate: e.target.value })}
                      className="input-field"
                      placeholder="bpm"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Temperature
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.temperature}
                      onChange={(e) => setFormData({ ...formData, temperature: e.target.value })}
                      className="input-field"
                      placeholder="°C"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Blood Glucose
                    </label>
                    <input
                      type="number"
                      value={formData.blood_glucose}
                      onChange={(e) => setFormData({ ...formData, blood_glucose: e.target.value })}
                      className="input-field"
                      placeholder="mg/dL"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Weight
                      </label>
                      <input
                        type="number"
                        step="0.1"
                        value={formData.weight}
                        onChange={(e) => setFormData({ ...formData, weight: e.target.value })}
                        className="input-field"
                        placeholder="kg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Height
                      </label>
                      <input
                        type="number"
                        value={formData.height}
                        onChange={(e) => setFormData({ ...formData, height: e.target.value })}
                        className="input-field"
                        placeholder="cm"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Symptoms
                    </label>
                    <input
                      type="text"
                      value={formData.symptoms}
                      onChange={(e) => setFormData({ ...formData, symptoms: e.target.value })}
                      className="input-field"
                      placeholder="Comma-separated symptoms"
                    />
                  </div>

                  <button type="submit" className="w-full btn-primary">
                    Log Metrics
                  </button>
                </form>
              </div>
            </div>

            {/* Charts */}
            <div className="lg:col-span-2 space-y-6">
              {chartData.length > 0 ? (
                <>
                  <LineGraph
                    data={chartData}
                    dataKey="heart_rate"
                    title="Heart Rate Trend"
                    xAxisKey="date"
                  />
                  <LineGraph
                    data={chartData}
                    dataKey="temperature"
                    title="Temperature Trend"
                    xAxisKey="date"
                  />
                  <LineGraph
                    data={chartData}
                    dataKey="blood_glucose"
                    title="Blood Glucose Trend"
                    xAxisKey="date"
                  />
                </>
              ) : (
                <div className="card">
                  <p className="text-gray-600 text-center py-8">
                    No health data yet. Start logging your metrics!
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
