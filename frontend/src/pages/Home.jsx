import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-primary">ExamAce</h1>
            <div className="flex gap-4">
              <button
                onClick={() => navigate('/login')}
                className="px-6 py-2 text-primary border border-primary rounded-lg hover:bg-blue-50 transition"
              >
                Login
              </button>
              <button
                onClick={() => navigate('/signup')}
                className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-blue-700 transition"
              >
                Sign Up
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h2 className="text-4xl md:text-6xl font-bold text-dark mb-6">
          Master Competitive Exams with <span className="text-primary">AI</span>
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          ExamAce provides adaptive testing, AI performance analysis, and personalized learning for IBPS, SBI, SSC, and more.
        </p>
        <button
          onClick={() => navigate('/signup')}
          className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          Start Free Trial
        </button>
      </section>

      {/* Features Section */}
      <section className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h3 className="text-3xl font-bold text-center mb-12">Key Features</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { icon: '🎯', title: 'Adaptive Testing', desc: 'Difficulty adjusts based on your performance' },
              { icon: '📊', title: 'AI Analytics', desc: 'Get detailed performance insights & weak areas' },
              { icon: '💬', title: 'AI Doubt Solver', desc: 'Instant solutions with step-by-step explanations' },
              { icon: '🏆', title: 'Leaderboards', desc: 'Compete with peers and track rankings' },
              { icon: '⚡', title: 'Real-time Timer', desc: 'Authentic exam experience with full-screen mode' },
              { icon: '🎓', title: 'Expert Curriculum', desc: 'Questions from previous year papers' },
            ].map((feature, idx) => (
              <div key={idx} className="p-6 border border-gray-200 rounded-lg hover:shadow-lg transition">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h4 className="text-xl font-semibold mb-2">{feature.title}</h4>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-primary text-white py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">50,000+</div>
              <p>Questions</p>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">100K+</div>
              <p>Active Users</p>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">2M+</div>
              <p>Tests Attempted</p>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">8</div>
              <p>Exams Covered</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-white py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h3 className="text-3xl font-bold mb-6">Ready to Excel?</h3>
          <p className="text-lg text-gray-600 mb-8">
            Join thousands of successful candidates preparing for competitive exams.
          </p>
          <button
            onClick={() => navigate('/signup')}
            className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Get Started Now
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark text-white py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-400">
          <p>&copy; 2024 ExamAce. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
