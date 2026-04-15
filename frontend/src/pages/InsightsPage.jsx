import React, { useState, useEffect } from 'react';
import { Sidebar } from '../components/Sidebar';
import { Header } from '../components/Header';
import { Lightbulb, Sparkles } from 'lucide-react';
import { recommendationService } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

export const InsightsPage = () => {
  const { user } = useAuth();
  const [insights, setInsights] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchInsights();
  }, [user.id]);

  const fetchInsights = async () => {
    try {
      setLoading(true);
      const insightsData = await recommendationService.getInsights(user.id);
      setInsights(insightsData.insights);

      const recsData = await recommendationService.getRecommendations(user.id);
      setRecommendations(recsData);
    } catch (error) {
      toast.error('Failed to load insights');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRecommendations = async () => {
    try {
      setGenerating(true);
      await recommendationService.generateRecommendations(user.id);
      toast.success('Recommendations generated successfully');
      await fetchInsights();
    } catch (error) {
      toast.error('Failed to generate recommendations');
      console.error(error);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  const getCategoryIcon = (category) => {
    const icons = {
      lifestyle: '🏃',
      medication: '💊',
      appointment: '📅',
      diet: '🥗',
      exercise: '🏋️',
      general: '⚕️',
    };
    return icons[category] || '💡';
  };

  return (
    <div className="flex bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-64">
        <div className="p-8">
          <Header
            title="Health Insights & Recommendations"
            subtitle="AI-powered analysis of your health data"
          />

          {/* Insights Section */}
          <div className="card mb-8 border-l-4 border-blue-500">
            <div className="flex items-start gap-4">
              <Lightbulb className="w-8 h-8 text-blue-600 flex-shrink-0 mt-1" />
              <div className="flex-1">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Your Health Insights</h3>
                <div className="prose prose-sm max-w-none text-gray-700 bg-blue-50 p-4 rounded">
                  {insights ? (
                    <p className="whitespace-pre-wrap">{insights}</p>
                  ) : (
                    <p className="text-gray-600">No insights available yet. Log more health data to get AI-powered analysis.</p>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Recommendations Section */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-gray-900">Recommended Actions</h3>
              <button
                onClick={handleGenerateRecommendations}
                disabled={generating}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                {generating ? 'Generating...' : 'Generate New'}
              </button>
            </div>

            {recommendations.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {recommendations.map((rec) => (
                  <div key={rec.id} className="card">
                    <div className="flex items-start gap-4">
                      <span className="text-3xl">{getCategoryIcon(rec.category)}</span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h4 className="font-semibold text-gray-900">{rec.title}</h4>
                          <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                            rec.priority === 'high'
                              ? 'bg-red-100 text-red-800'
                              : rec.priority === 'medium'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-green-100 text-green-800'
                          }`}>
                            {rec.priority.toUpperCase()}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-3">{rec.description}</p>
                        <div className="text-xs text-gray-500 bg-gray-50 p-2 rounded">
                          <strong>Why:</strong> {rec.reason}
                        </div>
                        <div className="mt-3 flex items-center gap-2 text-xs text-gray-500">
                          <span className="px-2 py-1 bg-gray-100 rounded capitalize">
                            {rec.category}
                          </span>
                          <span className="px-2 py-1 bg-gray-100 rounded">
                            {rec.generated_by}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="card">
                <p className="text-gray-600 text-center py-8">
                  No recommendations yet. Generate personalized recommendations for you!
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
