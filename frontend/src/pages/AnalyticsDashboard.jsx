import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import analyticsAPI from '../services/analytics';
import PerformanceChart from '../components/PerformanceChart';

export default function AnalyticsDashboard() {
  const user = useSelector(state => state.auth.user);
  
  const [dashboardStats, setDashboardStats] = useState(null);
  const [performanceByTopic, setPerformanceByTopic] = useState([]);
  const [weakAreas, setWeakAreas] = useState(null);
  const [strongAreas, setStrongAreas] = useState(null);
  const [scoreTrend, setScoreTrend] = useState(null);
  const [accuracyVsSpeed, setAccuracyVsSpeed] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [examTypePerformance, setExamTypePerformance] = useState([]);
  const [studySuggestions, setStudySuggestions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);

      const [
        stats,
        performance,
        weak,
        strong,
        trend,
        speedAcc,
        recs,
        examType,
        study
      ] = await Promise.all([
        analyticsAPI.getDashboardStats(),
        analyticsAPI.getPerformanceByTopic(),
        analyticsAPI.getWeakAreas(),
        analyticsAPI.getStrongAreas(),
        analyticsAPI.getScoreTrend(),
        analyticsAPI.getAccuracyVsSpeed(),
        analyticsAPI.getRecommendations(),
        analyticsAPI.getExamTypePerformance(),
        analyticsAPI.getStudySuggestions()
      ]);

      setDashboardStats(stats);
      setPerformanceByTopic(performance);
      setWeakAreas(weak);
      setStrongAreas(strong);
      setScoreTrend(trend);
      setAccuracyVsSpeed(speedAcc);
      setRecommendations(recs);
      setExamTypePerformance(examType);
      setStudySuggestions(study);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading your analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            {error}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Performance Analytics</h1>
          <p className="text-gray-600">Your detailed exam performance breakdown and insights</p>
        </div>

        {/* Dashboard Stats Cards */}
        {dashboardStats && (
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-gray-600 text-sm mb-1">Total Exams</p>
              <p className="text-3xl font-bold text-blue-600">{dashboardStats.total_exams_taken}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-gray-600 text-sm mb-1">Avg Accuracy</p>
              <p className="text-3xl font-bold text-green-600">{dashboardStats.average_accuracy}%</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-gray-600 text-sm mb-1">Avg Speed</p>
              <p className="text-3xl font-bold text-purple-600">{dashboardStats.average_speed}</p>
              <p className="text-xs text-gray-500">q/min</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-gray-600 text-sm mb-1">Best Score</p>
              <p className="text-3xl font-bold text-orange-600">{dashboardStats.best_score}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <p className="text-gray-600 text-sm mb-1">Current Rank</p>
              <p className="text-3xl font-bold text-red-600">#{dashboardStats.current_rank}</p>
            </div>
          </div>
        )}

        {/* Score Trend */}
        {scoreTrend && scoreTrend.trend_data.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Score Trend ({scoreTrend.total_exams} exams)</h2>
              <p className="text-lg">
                <span className="font-semibold">{scoreTrend.trend_direction}</span> • 
                Improvement: <span className={scoreTrend.improvement > 0 ? 'text-green-600' : 'text-red-600'}>
                  {scoreTrend.improvement > 0 ? '+' : ''}{scoreTrend.improvement}
                </span>
              </p>
            </div>
            <PerformanceChart data={scoreTrend.trend_data} type="trend" />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Performance by Topic */}
          {performanceByTopic.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Performance by Topic</h2>
              <PerformanceChart data={performanceByTopic} type="topic" />
            </div>
          )}

          {/* Accuracy vs Speed */}
          {accuracyVsSpeed && accuracyVsSpeed.data.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Accuracy vs Speed</h2>
              <div className="text-sm text-gray-600 mb-4">
                <p>Avg Accuracy: <span className="font-bold text-blue-600">{accuracyVsSpeed.average_accuracy}%</span></p>
                <p>Avg Speed: <span className="font-bold text-blue-600">{accuracyVsSpeed.average_speed} q/min</span></p>
              </div>
              <PerformanceChart data={accuracyVsSpeed.data} type="scatter" />
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Weak Areas */}
          {weakAreas && weakAreas.weak_areas.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-red-800 mb-4">⚠️ Areas to Focus ({weakAreas.weak_areas.length})</h2>
              <div className="space-y-3">
                {weakAreas.weak_areas.map((area) => (
                  <div key={area.topic} className="bg-white p-3 rounded border-l-4 border-red-500">
                    <div className="flex justify-between mb-1">
                      <h4 className="font-semibold text-gray-800">{area.topic}</h4>
                      <span className="text-red-600 font-bold">{area.accuracy}%</span>
                    </div>
                    <p className="text-xs text-gray-600">{area.recommendation}</p>
                    <p className="text-xs mt-1">
                      {area.correct_answers}/{area.total_questions} correct
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Strong Areas */}
          {strongAreas && strongAreas.strong_areas.length > 0 && (
            <div className="bg-green-50 border border-green-200 rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-green-800 mb-4">✅ Strong Topics ({strongAreas.strong_areas.length})</h2>
              <div className="space-y-3">
                {strongAreas.strong_areas.map((area) => (
                  <div key={area.topic} className="bg-white p-3 rounded border-l-4 border-green-500">
                    <div className="flex justify-between mb-1">
                      <h4 className="font-semibold text-gray-800">{area.topic}</h4>
                      <span className="text-green-600 font-bold">{area.accuracy}%</span>
                    </div>
                    <p className="text-xs text-gray-600">Keep it up!</p>
                    <p className="text-xs mt-1">
                      {area.correct_answers}/{area.total_questions} correct
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Exam Type Performance */}
        {examTypePerformance.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Performance by Exam Type</h2>
            <PerformanceChart data={examTypePerformance} type="exam-type" />
          </div>
        )}

        {/* Recommendations */}
        {recommendations && recommendations.recommendations.length > 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-2xl font-bold text-blue-800 mb-4">💡 Recommended Actions</h2>
            <div className="space-y-3">
              {recommendations.recommendations.map((rec, idx) => (
                <div key={idx} className="bg-white p-4 rounded border-l-4 border-blue-500">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-gray-800">{rec.type}</h4>
                    <span className={`text-xs px-2 py-1 rounded font-semibold ${
                      rec.priority === 'High' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                    }`}>
                      {rec.priority}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">{rec.suggestion}</p>
                  <p className="text-xs text-blue-600 font-semibold">✓ {rec.action}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Study Suggestions */}
        {studySuggestions && studySuggestions.study_plan.length > 0 && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold text-purple-800 mb-4">📚 Personalized Study Plan</h2>
            <div className="space-y-4">
              {studySuggestions.study_plan.map((phase) => (
                <div key={phase.phase} className="bg-white p-4 rounded border-l-4 border-purple-500">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-gray-800">Phase {phase.phase}: {phase.name}</h4>
                    <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">{phase.duration}</span>
                  </div>
                  <p className="text-sm text-gray-700 mb-3">{phase.description}</p>
                  <div className="flex flex-wrap gap-2">
                    {phase.topics.map((topic) => (
                      <span key={topic} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {dashboardStats && dashboardStats.total_exams_taken === 0 && (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <p className="text-4xl mb-4">📊</p>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">No Exam Data Yet</h3>
            <p className="text-gray-600 mb-6">Take some exams to see your performance analytics!</p>
            <a
              href="/exams"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
            >
              Browse Exams
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
