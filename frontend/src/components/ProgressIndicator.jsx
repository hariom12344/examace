import React from 'react'

export default function ProgressIndicator({ current, total, label = 'Progress' }) {
  const percentage = (current / total) * 100
  
  const getColor = () => {
    if (percentage < 33) return 'from-red-500 to-red-600'
    if (percentage < 66) return 'from-yellow-500 to-orange-600'
    return 'from-green-500 to-emerald-600'
  }

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-semibold text-gray-700">{label}</span>
        <span className="text-sm font-bold text-gray-600">{current}/{total}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <div
          className={`bg-gradient-to-r ${getColor()} h-full rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <p className="text-xs text-gray-500 mt-1">{percentage.toFixed(0)}% Complete</p>
    </div>
  )
}
