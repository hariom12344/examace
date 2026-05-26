export default function QuestionDisplay({
  question,
  selectedAnswer,
  onAnswerSelect,
  onMarkForReview,
  onClearAnswer,
  isMarkedForReview
}) {
  const options = [
    { key: 'A', text: question.option_a },
    { key: 'B', text: question.option_b },
    { key: 'C', text: question.option_c },
    { key: 'D', text: question.option_d }
  ];

  return (
    <div>
      {/* Question Text */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">{question.question_text}</h2>
        
        {/* Topic and Marks */}
        <div className="flex gap-3 text-sm">
          {question.topic && (
            <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
              📚 {question.topic}
            </span>
          )}
          <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full">
            ⭐ {question.marks} marks
          </span>
        </div>
      </div>

      {/* Options */}
      <div className="space-y-3 mb-8">
        {options.map(({ key, text }) => (
          <button
            key={key}
            onClick={() => onAnswerSelect(question.id, key)}
            className={`w-full p-4 text-left border-2 rounded-lg transition-all ${
              selectedAnswer === key
                ? 'border-blue-600 bg-blue-50'
                : 'border-gray-200 bg-white hover:border-blue-300'
            }`}
          >
            <div className="flex items-center gap-4">
              <div
                className={`w-6 h-6 rounded-full border-2 flex items-center justify-center font-semibold ${
                  selectedAnswer === key
                    ? 'border-blue-600 bg-blue-600 text-white'
                    : 'border-gray-300 text-gray-600'
                }`}
              >
                {key}
              </div>
              <span className="text-gray-800">{text}</span>
            </div>
          </button>
        ))}
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3 border-t pt-6">
        <button
          onClick={() => onMarkForReview(question.id)}
          className={`flex-1 px-4 py-2 rounded-lg font-semibold transition-colors ${
            isMarkedForReview
              ? 'bg-yellow-100 text-yellow-700 border border-yellow-300'
              : 'bg-gray-100 text-gray-700 border border-gray-300 hover:bg-gray-200'
          }`}
        >
          {isMarkedForReview ? '⭐ Marked for Review' : '☆ Mark for Review'}
        </button>
        <button
          onClick={() => onClearAnswer(question.id)}
          disabled={selectedAnswer === null}
          className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 border border-gray-300 rounded-lg font-semibold hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Clear Answer
        </button>
      </div>
    </div>
  );
}
