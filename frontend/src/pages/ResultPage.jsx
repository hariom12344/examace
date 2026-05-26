import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import examAPI from '../services/exam';

export default function ResultPage() {
  const { resultId } = useParams();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    loadResult();
  }, [resultId]);

  const loadResult = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await examAPI.getResult(resultId);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load result');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Calculating results...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-md">
          <p className="text-red-600 font-semibold mb-4">{error}</p>
          <button
            onClick={() => navigate('/exams')}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
          >
            Back to Exams
          </button>
        </div>
      </div>
    );
  }

  if (!result) return null;

  // Determine performance level
  const getPerformanceLevel = (accuracy) => {
    if (accuracy >= 80) return { level: 'Excellent', color: 'text-green-600', bg: 'bg-green-100' };
    if (accuracy >= 60) return { level: 'Good', color: 'text-blue-600', bg: 'bg-blue-100' };
    if (accuracy >= 40) return { level: 'Average', color: 'text-yellow-600', bg: 'bg-yellow-100' };
    return { level: 'Poor', color: 'text-red-600', bg: 'bg-red-100' };
  };

  const performance = getPerformanceLevel(result.accuracy);
  const totalQuestions = result.correct_answers + result.wrong_answers + result.unanswered;
  const timeInMinutes = Math.floor(result.time_taken / 60);
  const timeInSeconds = result.time_taken % 60;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="text-7xl mb-4">🎉</div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Test Completed!</h1>
          <p className="text-gray-600 text-lg">Results are ready</p>
        </div>

        {/* Main Score Card */}
        <div className="bg-white rounded-lg shadow-2xl p-8 mb-8">
          {/* Score Circle */}
          <div className="flex justify-center mb-8">
            <div className="relative w-48 h-48">
              {/* Circle Background */}
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke="#e5e7eb"
                  strokeWidth="3"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke="#3b82f6"
                  strokeWidth="3"
                  strokeDasharray={`${(result.accuracy / 100) * 282.7} 282.7`}
                  strokeLinecap="round"
                />
              </svg>

              {/* Center Text */}
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <p className={`text-5xl font-bold ${performance.color}`}>
                  {Math.round(result.accuracy)}%
                </p>
                <p className="text-sm text-gray-600 mt-2">{performance.level}</p>
              </div>
            </div>
          </div>

          {/* Score Details Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg text-center">
              <p className="text-gray-600 text-sm mb-1">Total Score</p>
              <p className="text-3xl font-bold text-blue-600">{Math.round(result.score)}</p>
            </div>
            <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg text-center">
              <p className="text-gray-600 text-sm mb-1">Correct</p>
              <p className="text-3xl font-bold text-green-600">{result.correct_answers}</p>
            </div>
            <div className="bg-gradient-to-br from-red-50 to-red-100 p-4 rounded-lg text-center">
              <p className="text-gray-600 text-sm mb-1">Wrong</p>
              <p className="text-3xl font-bold text-red-600">{result.wrong_answers}</p>
            </div>
            <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-lg text-center">
              <p className="text-gray-600 text-sm mb-1">Unanswered</p>
              <p className="text-3xl font-bold text-gray-600">{result.unanswered}</p>
            </div>
          </div>

          {/* Stats Row */}
          <div className="grid grid-cols-3 gap-4 border-t pt-6">
            <div className="text-center">
              <p className="text-gray-600 text-sm mb-1">Accuracy</p>
              <p className="text-2xl font-bold text-blue-600">{Math.round(result.accuracy)}%</p>
            </div>
            <div className="text-center">
              <p className="text-gray-600 text-sm mb-1">Speed</p>
              <p className="text-2xl font-bold text-purple-600">{Math.round(result.speed)} q/min</p>
            </div>
            <div className="text-center">
              <p className="text-gray-600 text-sm mb-1">Time Taken</p>
              <p className="text-2xl font-bold text-indigo-600">
                {timeInMinutes}:{String(timeInSeconds).padStart(2, '0')}
              </p>
            </div>
          </div>
        </div>

        {/* Performance Analysis */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Question Breakdown */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Question Breakdown</h3>
            
            <div className="space-y-3">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-700">Correct Answers</span>
                  <span className="font-semibold text-green-600">
                    {result.correct_answers}/{totalQuestions}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${(result.correct_answers / totalQuestions) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-700">Wrong Answers</span>
                  <span className="font-semibold text-red-600">
                    {result.wrong_answers}/{totalQuestions}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-red-500 h-2 rounded-full"
                    style={{ width: `${(result.wrong_answers / totalQuestions) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-700">Unanswered</span>
                  <span className="font-semibold text-gray-600">
                    {result.unanswered}/{totalQuestions}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gray-500 h-2 rounded-full"
                    style={{ width: `${(result.unanswered / totalQuestions) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Achievements */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Performance Metrics</h3>
            
            <div className="space-y-4">
              <div className={`${performance.bg} p-4 rounded-lg`}>
                <p className={`${performance.color} font-bold text-lg`}>
                  Performance: {performance.level}
                </p>
              </div>

              {result.rank && (
                <div className="bg-purple-50 p-4 rounded-lg">
                  <p className="text-purple-600 font-bold text-lg">
                    🏆 Rank: #{result.rank}
                  </p>
                </div>
              )}

              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-blue-600 text-sm">📊 Speed: Answers per minute</p>
                <p className="text-blue-600 font-bold text-lg">{Math.round(result.speed)} q/min</p>
              </div>
            </div>
          </div>
        </div>

        {/* Detailed Analysis Button */}
        <div className="mb-8">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            {showDetails ? 'Hide Detailed Analysis' : 'View Detailed Analysis'}
          </button>
        </div>

        {/* Detailed Analysis */}
        {showDetails && result.answers && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Answer Review</h3>
            
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {result.answers.map((answer, index) => (
                <div
                  key={answer.question_id}
                  className={`p-4 rounded-lg border-l-4 ${
                    answer.is_correct
                      ? 'border-green-500 bg-green-50'
                      : 'border-red-500 bg-red-50'
                  }`}
                >
                  <p className="font-semibold text-gray-800 mb-2">
                    Q{index + 1}: {answer.is_correct ? '✅ Correct' : '❌ Incorrect'}
                  </p>
                  <p className="text-sm text-gray-600">
                    Your answer: <span className="font-semibold">{answer.selected_answer || 'Not answered'}</span>
                  </p>
                  <p className="text-sm text-gray-600">
                    Time spent: <span className="font-semibold">{answer.time_spent}s</span>
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={() => navigate('/exams')}
            className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            Back to Exams
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
