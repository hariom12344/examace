import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import examAPI from '../services/exam';

export default function ExamList() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  
  // Set tab based on URL query param (defaults to 'mock')
  const currentTab = searchParams.get('tab') === 'pyq' ? 'pyq' : 'mock';

  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    exam_type: '',
    difficulty: ''
  });

  useEffect(() => {
    loadExams();
  }, [filters, currentTab]);

  const loadExams = async () => {
    try {
      setLoading(true);
      setError(null);
      const isPyq = currentTab === 'pyq';
      const data = await examAPI.getExams(
        filters.exam_type || null,
        filters.difficulty || null,
        isPyq
      );
      setExams(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load exams');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleStartExam = (examId) => {
    navigate(`/exam/${examId}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            {currentTab === 'pyq' ? 'Previous Year Papers' : 'Practice Mock Exams'}
          </h1>
          <p className="text-gray-600">
            {currentTab === 'pyq' 
              ? 'Attempt official previous year question papers from competitive exams' 
              : 'Choose a syllabus-aligned mock test to prepare for your exam'}
          </p>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-200 mb-8 gap-6 text-lg font-medium">
          <button
            onClick={() => setSearchParams({ tab: 'mock' })}
            className={`pb-4 border-b-2 px-2 transition-all duration-200 ${
              currentTab === 'mock'
                ? 'border-blue-600 text-blue-600 font-bold scale-105'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            🎯 Mock Tests
          </button>
          <button
            onClick={() => setSearchParams({ tab: 'pyq' })}
            className={`pb-4 border-b-2 px-2 transition-all duration-200 ${
              currentTab === 'pyq'
                ? 'border-blue-600 text-blue-600 font-bold scale-105'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📚 Previous Year Papers (PYQs)
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Exam Type
              </label>
              <select
                name="exam_type"
                value={filters.exam_type}
                onChange={handleFilterChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Types</option>
                <option value="Bank">Bank (IBPS/SBI)</option>
                <option value="SSC">SSC (CGL)</option>
                <option value="Railway">Railway (RRB)</option>
                <option value="CAT">CAT (Quant)</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Difficulty Level
              </label>
              <select
                name="difficulty"
                value={filters.difficulty}
                onChange={handleFilterChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Levels</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
            <p className="mt-4 text-gray-600">Loading exams...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            {error}
          </div>
        )}

        {/* Exams Grid */}
        {!loading && !error && exams.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {exams.map((exam) => (
              <div
                key={exam.id}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden"
              >
                {/* Card Header */}
                <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-4 text-white">
                  <h3 className="text-lg font-bold mb-1">{exam.title}</h3>
                  <div className="flex items-center justify-between text-sm">
                    <span className="bg-white bg-opacity-20 px-2 py-1 rounded">
                      {exam.exam_type}
                    </span>
                    <span className="bg-white bg-opacity-20 px-2 py-1 rounded">
                      {exam.difficulty}
                    </span>
                  </div>
                </div>

                {/* Card Body */}
                <div className="p-4">
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {exam.description || 'No description available'}
                  </p>

                  {/* Exam Details */}
                  <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
                    <div className="bg-blue-50 p-2 rounded">
                      <p className="text-gray-600">Duration</p>
                      <p className="font-semibold text-gray-800">{exam.duration} min</p>
                    </div>
                    <div className="bg-green-50 p-2 rounded">
                      <p className="text-gray-600">Marks</p>
                      <p className="font-semibold text-gray-800">{exam.total_marks}</p>
                    </div>
                    <div className="bg-purple-50 p-2 rounded">
                      <p className="text-gray-600">Sections</p>
                      <p className="font-semibold text-gray-800">{exam.sections}</p>
                    </div>
                    <div className="bg-orange-50 p-2 rounded">
                      <p className="text-gray-600">Questions</p>
                      <p className="font-semibold text-gray-800">TBD</p>
                    </div>
                  </div>

                  {/* Start Button */}
                  <button
                    onClick={() => handleStartExam(exam.id)}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                  >
                    Start Exam →
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && exams.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📚</div>
            <p className="text-gray-600 text-lg mb-4">No exams available with the selected filters</p>
            <button
              onClick={() => setFilters({ exam_type: '', difficulty: '' })}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
            >
              Clear Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
