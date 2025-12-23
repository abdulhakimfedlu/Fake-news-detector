import React from 'react';

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  const getEmojiAndColor = (pred) => {
    switch (pred) {
      case 'Fake': return { emoji: '🚨', bg: 'bg-red-50 border-red-400 text-red-700' };
      case 'Real': return { emoji: '✅', bg: 'bg-green-50 border-green-400 text-green-700' };
      case 'Uncertain': return { emoji: '❓', bg: 'bg-yellow-50 border-yellow-400 text-yellow-700' };
      case 'Error': return { emoji: '⚠️', bg: 'bg-red-50 border-red-400 text-red-700' };
      default: return { emoji: '⚠️', bg: 'bg-gray-50 border-gray-400 text-gray-700' };
    }
  };

  const { emoji, bg, textColor } = getEmojiAndColor(result.prediction);
  const comp = result.comparison || {};
  const dt = comp.decision_tree || { prediction: 'N/A', confidence: 0 };
  const rf = comp.random_forest || { prediction: 'N/A', confidence: 0 };

  return (
    <div className={`p-6 rounded-xl border-l-4 ${bg} ${textColor} fade-in shadow-md border mb-4`}>
      <div className="flex items-center mb-3">
        <span className="text-3xl mr-3">{emoji}</span>
        <h2 className="text-2xl font-bold">{result.prediction}</h2>
      </div>
      <p className="text-xl mb-3 font-semibold">
        Confidence: <span className="text-2xl">{result.confidence}%</span>
      </p>
      <p className="text-sm italic opacity-90 mb-4">{result.explanation}</p>
      <p className="text-xs text-gray-500 mb-4">Best Algorithm: <strong>{result.best_algorithm || 'N/A'}</strong></p>
      
      {/* Comparison Table */}
      <div className="bg-white rounded-lg shadow-inner p-4">
        <h3 className="text-sm font-medium mb-2 text-gray-700">Live Comparison:</h3>
        <table className="w-full text-xs text-left">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-2 py-1 rounded-tl">Algorithm</th>
              <th className="px-2 py-1">Prediction</th>
              <th className="px-2 py-1 rounded-tr">Confidence</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-t">
              <td className="px-2 py-1 font-medium">Decision Tree</td>
              <td className="px-2 py-1">{dt.prediction}</td>
              <td className="px-2 py-1">{dt.confidence}%</td>
            </tr>
            <tr className="bg-blue-50 border-t">
              <td className="px-2 py-1 font-medium">Random Forest (Best)</td>
              <td className="px-2 py-1">{rf.prediction}</td>
              <td className="px-2 py-1 font-bold">{rf.confidence}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultDisplay;