import React from 'react';

const InputForm = ({ text, onTextChange, onSubmit, loading, disabled }) => (
    <form onSubmit={onSubmit} className="space-y-4 mb-8">
        <textarea
            value={text}
            onChange={onTextChange}
            placeholder="Paste a full news article or headline here (e.g., 'UN climate agreement approved...') for best results."
            className="w-full p-5 border-2 border-gray-300 rounded-xl resize-none h-48 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all duration-300 shadow-sm hover:shadow-md"
            rows="6"
            disabled={loading}
        />
        <button
            type="submit"
            disabled={disabled}
            className="w-full bg-primary text-white py-4 px-6 rounded-xl font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
        >
            {loading ? '🔍 Analyzing...' : '🚀 Detect Fake News'}
        </button>
    </form>
);

export default InputForm;