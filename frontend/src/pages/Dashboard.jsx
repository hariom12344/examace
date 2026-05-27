import { useSelector, useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { logout } from '../store/authSlice'
import { authAPI } from '../services/auth'

export default function Dashboard() {
  const user = useSelector((state) => state.auth.user)
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const [stats, setStats] = useState({ examsCompleted: 0, accuracy: 0, rank: 0 })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate loading stats - replace with API call
    setTimeout(() => {
      setStats({
        examsCompleted: 3,
        accuracy: 74.5,
        rank: 128
      })
      setIsLoading(false)
    }, 800)
  }, [])

  const handleLogout = async () => {
    try {
      await authAPI.logout()
      dispatch(logout())
      navigate('/login')
    } catch (error) {
      console.error('Logout error:', error)
      dispatch(logout())
      navigate('/login')
    }
  }

  const dashboardCards = [
    { icon: '📝', title: 'Take Mock Test', desc: 'Syllabus-aligned practice exams', action: () => navigate('/exams?tab=mock'), color: 'from-blue-500 to-blue-600' },
    { icon: '📚', title: 'Previous Year Papers', desc: 'Actual competitive exam papers', action: () => navigate('/exams?tab=pyq'), color: 'from-purple-500 to-purple-600' },
    { icon: '📊', title: 'Analytics', desc: 'Detailed performance insights', action: () => navigate('/analytics'), color: 'from-green-500 to-green-600' },
    { icon: '📈', title: 'My Progress', desc: 'Track your preparation stats', action: () => navigate('/analytics'), color: 'from-orange-500 to-orange-600' },
    { icon: '⚙️', title: 'Settings', desc: 'Update your profile', action: () => navigate('/settings'), color: 'from-gray-500 to-gray-600' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">ExamAce</h1>
          <div className="flex items-center gap-4">
            <span className="text-white/80 font-medium">Welcome, {user?.name}! 👋</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-500/20 text-red-300 rounded-lg hover:bg-red-500/30 transition duration-300 border border-red-500/30"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header Section */}
        <div className="mb-12 animate-fade-in">
          <h2 className="text-4xl font-bold text-white mb-4">Welcome Back! 🚀</h2>
          <p className="text-white/70 text-lg">Continue your journey towards success with ExamAce</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[
            { label: 'Exams Completed', value: isLoading ? '...' : stats.examsCompleted, icon: '✓', color: 'from-green-500 to-emerald-600' },
            { label: 'Avg Accuracy', value: isLoading ? '...' : `${stats.accuracy}%`, icon: '🎯', color: 'from-blue-500 to-cyan-600' },
            { label: 'Current Rank', value: isLoading ? '...' : `#${stats.rank}`, icon: '🏆', color: 'from-yellow-500 to-orange-600' }
          ].map((stat, idx) => (
            <div
              key={idx}
              className={`bg-gradient-to-br ${stat.color} p-8 rounded-xl text-white shadow-lg hover:shadow-2xl transform hover:scale-105 transition duration-300 animate-slide-up`}
              style={{ animationDelay: `${idx * 100}ms` }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white/80 text-sm font-medium mb-2">{stat.label}</p>
                  <p className="text-3xl font-bold">{stat.value}</p>
                </div>
                <span className="text-5xl opacity-30">{stat.icon}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Action Cards */}
        <div className="mb-8">
          <h3 className="text-2xl font-bold text-white mb-6">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {dashboardCards.map((item, idx) => (
              <div
                key={idx}
                onClick={item.action}
                className={`bg-gradient-to-br ${item.color} rounded-xl p-6 text-white cursor-pointer shadow-lg hover:shadow-2xl transform hover:scale-105 transition duration-300 animate-slide-up`}
                style={{ animationDelay: `${idx * 50}ms` }}
              >
                <div className="text-5xl mb-4">{item.icon}</div>
                <h3 className="text-lg font-bold mb-2">{item.title}</h3>
                <p className="text-sm text-white/80">{item.desc}</p>
                <div className="mt-4 pt-4 border-t border-white/20 flex items-center text-sm font-medium">
                  Get Started →
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Info Section */}
        <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 backdrop-blur-md border border-white/10 p-8 rounded-xl text-white">
          <h3 className="text-xl font-bold mb-3">💡 Pro Tips for Better Preparation</h3>
          <ul className="space-y-2 text-white/80">
            <li>✓ Take mock tests regularly to assess your progress</li>
            <li>✓ Review previous year papers to understand exam patterns</li>
            <li>✓ Analyze your performance metrics for targeted improvement</li>
            <li>✓ Practice time management with our timed exams</li>
          </ul>
        </div>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.6s ease-out;
        }
        .animate-slide-up {
          animation: slide-up 0.5s ease-out forwards;
          opacity: 0;
        }
      `}</style>
    </div>
  )
}
