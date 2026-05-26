import { useState, useEffect } from 'react';

export default function Timer({ duration, onTimeUp, timeUp }) {
  const [timeRemaining, setTimeRemaining] = useState(duration * 60); // convert to seconds
  const [isWarning, setIsWarning] = useState(false);

  useEffect(() => {
    if (timeUp) return;

    const timer = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          onTimeUp();
          return 0;
        }
        
        // Show warning when 5 minutes remaining
        if (prev <= 300 && !isWarning) {
          setIsWarning(true);
        }
        
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeUp, onTimeUp, isWarning]);

  const minutes = Math.floor(timeRemaining / 60);
  const seconds = timeRemaining % 60;

  const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  let bgColor = 'bg-green-600';
  let textColor = 'text-white';
  
  if (isWarning) {
    bgColor = 'bg-red-600';
  }

  return (
    <div className={`${bgColor} ${textColor} px-6 py-2 rounded-lg font-mono text-xl font-bold flex items-center gap-2`}>
      <span>⏱️</span>
      <span>{formattedTime}</span>
    </div>
  );
}
