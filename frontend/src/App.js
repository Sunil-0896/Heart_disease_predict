import React, { useState } from 'react';
import ImageUploader from './components/ImageUploader';
import ChatWindow from './components/ChatWindow';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [isAnalyzed, setIsAnalyzed] = useState(false);

  const handleAnalysisComplete = (pred, conf) => {
    setPrediction(pred);
    setConfidence(conf);
    setIsAnalyzed(true);
  };

  const handleReset = () => {
    setPrediction(null);
    setConfidence(null);
    setIsAnalyzed(false);
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '40px 20px', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <header style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h2 style={{ color: '#1a1a1a', marginBottom: '8px' }}>AI-Powered Medical Assistant</h2>
        <p style={{ color: '#666', margin: 0 }}>Upload medical imaging scans for automated triage and instant analysis.</p>
      </header>

      {!isAnalyzed ? (
        <ImageUploader onAnalysisComplete={handleAnalysisComplete} />
      ) : (
        <div>
          <div style={{ padding: '20px', backgroundColor: '#fff', borderRadius: '8px', marginBottom: '25px', border: '1px solid #e0e0e0', boxShadow: '0 2px 4px rgba(0,0,0,0.02)' }}>
            <button 
              onClick={handleReset} 
              style={{ float: 'right', cursor: 'pointer', background: 'none', border: '1px solid #ccc', padding: '6px 12px', borderRadius: '4px', fontSize: '13px' }}
            >
              Upload New Image
            </button>
            <h4 style={{ margin: '0 0 12px 0', color: '#333' }}>Inference Pipeline Output</h4>
            <p style={{ margin: '4px 0', color: '#555' }}><strong>Preliminary Indication:</strong> {prediction}</p>
            <p style={{ margin: '4px 0', color: '#555' }}><strong>Statistical Confidence:</strong> {(confidence * 100).toFixed(1)}%</p>
          </div>
          
          <ChatWindow prediction={prediction} confidence={confidence} />
        </div>
      )}
    </div>
  );
}

export default App;