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
    return (
        <div className={`p-6 rounded-xl border-l-4 ${bg} ${textColor} fade-in shadow-md border`}>
            <div className="flex items-center mb-3">
                <span className="text-3xl mr-3">{emoji}</span>
                <h2 className="text-2xl font-bold">{result.prediction}</h2>
            </div>
            <p className="text-xl mb-3 font-semibold">
                Confidence: <span className="text-2xl">{result.confidence}%</span>
            </p>
            <p className="text-sm italic opacity-90 mb-2">{result.explanation}</p>
            <p className="text-xs text-gray-500">Algorithm Used: <strong>{result.algorithm || 'N/A'}</strong></p>
        </div>
    );
};

export default ResultDisplay;