import React, { useState } from 'react';
import Header from './components/Header';
import InputForm from './components/InputForm';
import ResultDisplay from './components/ResultDisplay';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      if (!response.ok) throw new Error(`API Error: ${response.status}`);
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        prediction: 'Error',
        confidence: 0,
        explanation: 'Check backend server or try again!',
        algorithm: 'N/A'
      });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <Header />
        <InputForm
          text={text}
          onTextChange={(e) => setText(e.target.value)}
          onSubmit={handleSubmit}
          loading={loading}
          disabled={loading || !text.trim()}
        />
        <ResultDisplay result={result} />
      </div>
    </div>
  );
}

export default App;