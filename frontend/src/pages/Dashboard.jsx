import { useSelector, useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { logout } from '../store/authSlice'
import { authAPI } from '../services/auth'

export default function Dashboard() {
  const user = useSelector((state) => state.auth.user)
  const dispatch = useDispatch()
  const navigate = useNavigate()

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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">ExamAce</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-700">Welcome, {user?.name}!</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow p-8">
          <h2 className="text-3xl font-bold text-dark mb-4">Dashboard</h2>
          <p className="text-gray-600 mb-8">
            Welcome to ExamAce! You're logged in and ready to start preparing.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              { icon: '📝', title: 'Take Mock Test', desc: 'Syllabus-aligned practice exams', action: () => navigate('/exams?tab=mock') },
              { icon: '📚', title: 'Previous Year Papers', desc: 'Actual competitive exam papers', action: () => navigate('/exams?tab=pyq') },
              { icon: '📊', title: 'Analytics', desc: 'Detailed performance insights', action: () => navigate('/analytics') },
              { icon: '📈', title: 'My Progress', desc: 'Track your preparation stats', action: () => navigate('/analytics') },
              { icon: '⚙️', title: 'Settings', desc: 'Update your profile', action: () => navigate('/settings') },
            ].map((item, idx) => (
              <div
                key={idx}
                onClick={item.action}
                className="border border-gray-200 rounded-lg p-5 hover:shadow-lg transition cursor-pointer hover:bg-gray-50 flex flex-col justify-between"
              >
                <div>
                  <div className="text-4xl mb-3">{item.icon}</div>
                  <h3 className="text-lg font-semibold mb-2">{item.title}</h3>
                  <p className="text-gray-600 text-sm">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 p-6 bg-blue-50 rounded-lg border border-blue-200">
            <h3 className="text-lg font-semibold text-dark mb-2">👋 Getting Started</h3>
            <p className="text-gray-700">
              This is your dashboard! More features are coming soon. Check back for exams, results, and AI-powered learning tools.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
