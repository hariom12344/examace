export default function PerformanceChart({ data, type = 'bar' }) {
  if (!data || data.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500">
        No data available
      </div>
    );
  }

  return (
    <div className="w-full h-64">
      {type === 'topic' && (
        <div className="space-y-3">
          {data.map((item) => (
            <div key={item.topic}>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">{item.topic}</span>
                <span className="text-sm font-semibold">{item.accuracy}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all ${
                    item.accuracy >= 75
                      ? 'bg-green-500'
                      : item.accuracy >= 60
                      ? 'bg-yellow-500'
                      : 'bg-red-500'
                  }`}
                  style={{ width: `${item.accuracy}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      )}

      {type === 'trend' && (
        <div className="flex items-end justify-around h-full gap-2">
          {data.map((item, idx) => (
            <div key={idx} className="flex flex-col items-center gap-2">
              <div
                className="bg-blue-500 rounded-t w-8"
                style={{
                  height: `${(item.score / 100) * 200}px`,
                  minHeight: '20px'
                }}
                title={`Score: ${item.score}`}
              ></div>
              <span className="text-xs text-gray-600">{item.date.slice(5)}</span>
            </div>
          ))}
        </div>
      )}

      {type === 'scatter' && (
        <div className="relative w-full h-full border-l border-b border-gray-300 p-4">
          {data.map((item, idx) => (
            <div
              key={idx}
              className="absolute w-3 h-3 bg-blue-500 rounded-full hover:bg-blue-700 cursor-pointer group"
              style={{
                left: `${(item.speed / 2) * 80}%`,
                top: `${100 - item.accuracy}%`,
                transform: 'translate(-50%, -50%)'
              }}
              title={`Accuracy: ${item.accuracy}% | Speed: ${item.speed} q/min | Score: ${item.score}`}
            >
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block bg-gray-800 text-white text-xs p-2 rounded whitespace-nowrap">
                Acc: {item.accuracy}% | Speed: {item.speed} q/min
              </div>
            </div>
          ))}
          
          {/* Axes labels */}
          <div className="absolute bottom-0 left-0 text-xs text-gray-600">0</div>
          <div className="absolute bottom-0 right-0 text-xs text-gray-600">Speed</div>
          <div className="absolute top-0 left-0 text-xs text-gray-600">100</div>
        </div>
      )}

      {type === 'exam-type' && (
        <div className="space-y-4">
          {data.map((item) => (
            <div key={item.exam_type} className="border-l-4 border-blue-500 pl-4 py-2">
              <div className="flex justify-between mb-2">
                <h4 className="font-semibold text-gray-800">{item.exam_type}</h4>
                <span className="text-sm text-gray-600">{item.total_exams} exams</span>
              </div>
              <div className="grid grid-cols-3 gap-2 text-sm">
                <div>
                  <p className="text-gray-600">Avg Score</p>
                  <p className="font-bold text-blue-600">{item.average_score}</p>
                </div>
                <div>
                  <p className="text-gray-600">Best</p>
                  <p className="font-bold text-green-600">{item.best_score}</p>
                </div>
                <div>
                  <p className="text-gray-600">Accuracy</p>
                  <p className="font-bold text-purple-600">{item.average_accuracy}%</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
