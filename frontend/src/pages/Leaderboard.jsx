import { useState, useEffect } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filter, setFilter] = useState('global')
  const navigate = useNavigate()

  useEffect(() => {
    fetchLeaderboard()
  }, [filter])

  const fetchLeaderboard = async () => {
    try {
      setLoading(true)
      const endpoint = filter === 'global' 
        ? 'http://localhost:8000/api/leaderboard/global'
        : `http://localhost:8000/api/leaderboard/trending?days=7`
      
      const response = await axios.get(endpoint)
      setLeaderboard(response.data.leaderboard || [])
      setError(null)
    } catch (err) {
      setError('Failed to load leaderboard')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading leaderboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="bg-red-500/20 border border-red-500/30 p-8 rounded-lg text-red-300 max-w-md">
          <p className="font-semibold mb-4">{error}</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="w-full px-4 py-2 bg-red-500/30 hover:bg-red-500/40 rounded-lg transition"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🏆 Leaderboard</h1>
          <p className="text-white/70">See how you rank among ExamAce users</p>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-4 mb-8">
          {[
            { label: 'Global Rankings', value: 'global' },
            { label: 'Trending This Week', value: 'trending' }
          ].map((tab) => (
            <button
              key={tab.value}
              onClick={() => setFilter(tab.value)}
              className={`px-6 py-2 rounded-lg font-semibold transition ${
                filter === tab.value
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                  : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Leaderboard Table */}
        <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-white/5 border-b border-white/10">
                  <th className="px-6 py-4 text-left text-white font-semibold">Rank</th>
                  <th className="px-6 py-4 text-left text-white font-semibold">Name</th>
                  <th className="px-6 py-4 text-center text-white font-semibold">Exams</th>
                  <th className="px-6 py-4 text-center text-white font-semibold">Accuracy</th>
                  <th className="px-6 py-4 text-center text-white font-semibold">Avg Score</th>
                  <th className="px-6 py-4 text-center text-white font-semibold">Speed</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.length > 0 ? (
                  leaderboard.map((entry, idx) => (
                    <tr
                      key={entry.user_id}
                      className={`border-b border-white/5 transition hover:bg-white/5 ${
                        idx === 0 ? 'bg-yellow-500/10' : idx === 1 ? 'bg-gray-400/10' : idx === 2 ? 'bg-orange-400/10' : ''
                      }`}
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          {idx === 0 && <span className="text-2xl">🥇</span>}
                          {idx === 1 && <span className="text-2xl">🥈</span>}
                          {idx === 2 && <span className="text-2xl">🥉</span>}
                          <span className="text-white font-bold text-lg">#{entry.rank}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-white font-medium">{entry.name}</div>
                      </td>
                      <td className="px-6 py-4 text-center text-white/80">{entry.exams_completed}</td>
                      <td className="px-6 py-4 text-center">
                        <span className="bg-blue-500/30 text-blue-300 px-3 py-1 rounded-full text-sm font-semibold">
                          {entry.avg_accuracy}%
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center text-white/80">{entry.avg_score}</td>
                      <td className="px-6 py-4 text-center text-white/80">{entry.avg_speed.toFixed(2)}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="px-6 py-12 text-center text-white/50">
                      No data available yet
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}
