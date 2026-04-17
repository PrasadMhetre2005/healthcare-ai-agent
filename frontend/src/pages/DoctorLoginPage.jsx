import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { Mail, Phone, Lock, Stethoscope } from 'lucide-react';
import api from '../services/api';

const DoctorLoginPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loginMethod, setLoginMethod] = useState('email'); // email, phone, or username
  const [credentials, setCredentials] = useState({
    email: '',
    phone: '',
    username: '',
    password: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate
    const loginValue = credentials[loginMethod];
    if (!loginValue || !credentials.password) {
      toast.error('Please fill in all fields');
      return;
    }

    setLoading(true);

    try {
      const loginData = {
        [loginMethod]: loginValue,
        password: credentials.password
      };

      const response = await api.post('/doctors/login', loginData);

      // Store token and doctor info
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('doctor', JSON.stringify(response.data.doctor));
      localStorage.setItem('user_role', 'doctor');

      toast.success('Login successful!');
      
      // Redirect to doctor dashboard
      setTimeout(() => {
        navigate('/doctor-dashboard');
      }, 1000);

    } catch (error) {
      console.error('Login error:', error);
      toast.error(error.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-blue-50 py-12 px-4 flex items-center justify-center">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-gradient-to-br from-blue-600 to-cyan-600 rounded-full p-4">
              <Stethoscope className="w-8 h-8 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Doctor Login</h1>
          <p className="text-gray-600">Access your patient dashboard</p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Login Method Tabs */}
            <div className="flex gap-2 bg-gray-100 p-1 rounded-lg mb-6">
              <button
                type="button"
                onClick={() => setLoginMethod('email')}
                className={`flex-1 py-2 px-4 rounded-md font-semibold transition ${
                  loginMethod === 'email'
                    ? 'bg-white text-blue-600 shadow'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Mail className="w-4 h-4 inline mr-2" />
                Email
              </button>
              <button
                type="button"
                onClick={() => setLoginMethod('phone')}
                className={`flex-1 py-2 px-4 rounded-md font-semibold transition ${
                  loginMethod === 'phone'
                    ? 'bg-white text-blue-600 shadow'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Phone className="w-4 h-4 inline mr-2" />
                Phone
              </button>
              <button
                type="button"
                onClick={() => setLoginMethod('username')}
                className={`flex-1 py-2 px-4 rounded-md font-semibold transition ${
                  loginMethod === 'username'
                    ? 'bg-white text-blue-600 shadow'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Username
              </button>
            </div>

            {/* Login Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                {loginMethod === 'email' && <><Mail className="inline w-4 h-4 mr-2" />Email Address</>}
                {loginMethod === 'phone' && <><Phone className="inline w-4 h-4 mr-2" />Phone Number</>}
                {loginMethod === 'username' && <>Username</>}
              </label>
              <input
                type={loginMethod === 'email' ? 'email' : 'text'}
                name={loginMethod}
                value={credentials[loginMethod]}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
                placeholder={
                  loginMethod === 'email'
                    ? 'doctor@example.com'
                    : loginMethod === 'phone'
                    ? '+1 (555) 123-4567'
                    : 'your_username'
                }
                required
              />
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                <Lock className="inline w-4 h-4 mr-2" />
                Password
              </label>
              <input
                type="password"
                name="password"
                value={credentials.password}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
                placeholder="••••••••"
                required
              />
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded border-gray-300" />
                <span className="text-gray-700">Remember me</span>
              </label>
              <button
                type="button"
                onClick={() => navigate('/forgot-password')}
                className="text-blue-600 hover:text-blue-700 font-semibold"
              >
                Forgot password?
              </button>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-gray-400 disabled:to-gray-400 text-white font-semibold py-3 rounded-lg transition-all transform hover:scale-105 active:scale-95"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>

            {/* Divider */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">New doctor?</span>
              </div>
            </div>

            {/* Register Link */}
            <button
              type="button"
              onClick={() => navigate('/doctor-register')}
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-900 font-semibold py-3 rounded-lg transition"
            >
              Create a Doctor Account
            </button>

            {/* Back to Patient Login */}
            <p className="text-center text-sm text-gray-600">
              Looking for patient login?{' '}
              <button
                type="button"
                onClick={() => navigate('/login')}
                className="text-blue-600 hover:text-blue-700 font-semibold"
              >
                Go to patient login
              </button>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
};

export default DoctorLoginPage;
