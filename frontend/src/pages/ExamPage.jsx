import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import examAPI from '../services/exam';
import Timer from '../components/Timer';
import QuestionDisplay from '../components/QuestionDisplay';

export default function ExamPage() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const user = useSelector(state => state.auth.user);

  const [exam, setExam] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [timeUp, setTimeUp] = useState(false);
  const [examStartTime, setExamStartTime] = useState(null);
  const [currentSection, setCurrentSection] = useState(null);

  // Exam states
  const [reviewed, setReviewed] = useState({});
  const [markedForReview, setMarkedForReview] = useState({});

  useEffect(() => {
    loadExam();
  }, [examId]);

  const loadExam = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const examData = await examAPI.getExam(examId);
      setExam(examData);

      const questionsData = await examAPI.getExamQuestions(examId);
      setQuestions(questionsData);

      // Initialize exam
      setExamStartTime(new Date());
      setCurrentSection(questionsData[0]?.section || 'General');
      
      // Initialize answers object
      const initialAnswers = {};
      questionsData.forEach(q => {
        initialAnswers[q.id] = null;
      });
      setAnswers(initialAnswers);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load exam');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
    // Auto-mark as reviewed when answered
    if (markedForReview[questionId]) {
      setMarkedForReview(prev => ({
        ...prev,
        [questionId]: false
      }));
    }
  };

  const handleMarkForReview = (questionId) => {
    setMarkedForReview(prev => ({
      ...prev,
      [questionId]: !prev[questionId]
    }));
  };

  const handleClearAnswer = (questionId) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: null
    }));
  };

  const handleTimeUp = () => {
    setTimeUp(true);
    // Auto-submit
    setTimeout(() => {
      handleSubmitExam();
    }, 2000);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setCurrentSection(questions[currentQuestionIndex + 1]?.section || 'General');
    }
  };

  const handlePrevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
      setCurrentSection(questions[currentQuestionIndex - 1]?.section || 'General');
    }
  };

  const handleGoToQuestion = (index) => {
    setCurrentQuestionIndex(index);
    setCurrentSection(questions[index]?.section || 'General');
  };

  const handleSubmitExam = async () => {
    try {
      const timeTaken = Math.round((new Date() - examStartTime) / 1000); // in seconds

      // Convert answers to submission format
      const submissionAnswers = questions.map(q => ({
        question_id: q.id,
        selected_answer: answers[q.id],
        time_spent: Math.round(timeTaken / questions.length) // Simple time distribution
      }));

      const result = await examAPI.submitTest(examId, submissionAnswers, timeTaken);
      
      // Navigate to result page
      navigate(`/result/${result.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit exam');
    }
  };

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading exam...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-100">
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

  if (!exam || questions.length === 0) {
    return null;
  }

  const currentQuestion = questions[currentQuestionIndex];
  const answeredCount = Object.values(answers).filter(a => a !== null).length;
  const reviewedCount = Object.values(reviewed).filter(r => r === true).length;
  const markedCount = Object.values(markedForReview).filter(m => m === true).length;
  const notVisitedCount = questions.length - answeredCount - reviewedCount - markedCount;

  return (
    <div className="h-screen bg-gray-100 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">{exam.title}</h1>
            <p className="text-blue-100 text-sm">Section: {currentSection}</p>
          </div>
          <div className="flex gap-4">
            <Timer
              duration={exam.duration}
              onTimeUp={handleTimeUp}
              timeUp={timeUp}
            />
            <button
              onClick={() => setShowModal(true)}
              className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-semibold"
            >
              Submit Exam
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden max-w-7xl mx-auto w-full">
        {/* Left Panel - Question Display */}
        <div className="flex-1 p-6 overflow-y-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="mb-6">
              <p className="text-gray-600 text-sm">
                Question {currentQuestionIndex + 1} of {questions.length}
              </p>
              <div className="mt-2 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{
                    width: `${((currentQuestionIndex + 1) / questions.length) * 100}%`
                  }}
                ></div>
              </div>
            </div>

            <QuestionDisplay
              question={currentQuestion}
              selectedAnswer={answers[currentQuestion.id]}
              onAnswerSelect={handleAnswerSelect}
              onMarkForReview={handleMarkForReview}
              onClearAnswer={handleClearAnswer}
              isMarkedForReview={markedForReview[currentQuestion.id] || false}
            />

            {/* Navigation Buttons */}
            <div className="flex gap-4 mt-8">
              <button
                onClick={handlePrevQuestion}
                disabled={currentQuestionIndex === 0}
                className="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-400"
              >
                ← Previous
              </button>
              <button
                onClick={handleNextQuestion}
                disabled={currentQuestionIndex === questions.length - 1}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700"
              >
                Next →
              </button>
            </div>
          </div>
        </div>

        {/* Right Panel - Questions Panel */}
        <div className="w-64 bg-white shadow-lg p-4 overflow-y-auto border-l border-gray-200">
          <h3 className="font-bold text-gray-800 mb-4">Questions Navigator</h3>

          {/* Stats */}
          <div className="grid grid-cols-2 gap-2 mb-4 text-xs">
            <div className="bg-green-50 p-2 rounded">
              <p className="text-gray-600">Answered</p>
              <p className="font-bold text-green-600">{answeredCount}</p>
            </div>
            <div className="bg-yellow-50 p-2 rounded">
              <p className="text-gray-600">Marked</p>
              <p className="font-bold text-yellow-600">{markedCount}</p>
            </div>
          </div>

          {/* Question Grid */}
          <div className="grid grid-cols-4 gap-2">
            {questions.map((q, index) => {
              let bgColor = 'bg-gray-200'; // Not visited
              if (answers[q.id] !== null) bgColor = 'bg-green-500'; // Answered
              if (markedForReview[q.id]) bgColor = 'bg-yellow-500'; // Marked for review
              
              return (
                <button
                  key={q.id}
                  onClick={() => handleGoToQuestion(index)}
                  className={`${bgColor} text-xs font-semibold w-8 h-8 rounded flex items-center justify-center ${
                    currentQuestionIndex === index ? 'ring-2 ring-offset-2 ring-blue-600' : ''
                  } hover:opacity-80 transition-opacity`}
                >
                  {index + 1}
                </button>
              );
            })}
          </div>

          {/* Legend */}
          <div className="mt-6 text-xs border-t pt-4">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-4 h-4 bg-green-500 rounded"></div>
              <span className="text-gray-600">Answered</span>
            </div>
            <div className="flex items-center gap-2 mb-2">
              <div className="w-4 h-4 bg-yellow-500 rounded"></div>
              <span className="text-gray-600">Marked for Review</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-gray-200 rounded"></div>
              <span className="text-gray-600">Not Visited</span>
            </div>
          </div>
        </div>
      </div>

      {/* Submit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md shadow-xl">
            <h2 className="text-2xl font-bold mb-4">Submit Exam?</h2>
            <div className="bg-gray-50 p-4 rounded mb-6 text-sm">
              <p className="mb-2"><strong>Answered:</strong> {answeredCount} questions</p>
              <p className="mb-2"><strong>Not Answered:</strong> {questions.length - answeredCount} questions</p>
              <p className="text-red-600"><strong>This action cannot be undone!</strong></p>
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => setShowModal(false)}
                className="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
              >
                Continue Exam
              </button>
              <button
                onClick={handleSubmitExam}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Time Up Alert */}
      {timeUp && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md shadow-xl animate-pulse">
            <h2 className="text-2xl font-bold text-red-600 mb-4">⏰ Time's Up!</h2>
            <p className="text-gray-600 mb-6">Your exam has been submitted automatically.</p>
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          </div>
        </div>
      )}
    </div>
  );
}
