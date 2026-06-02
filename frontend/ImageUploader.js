import React, { useState } from 'react';

function ImageUploader({ onAnalysisComplete }) {
  const [file, setFile] = useState(null);
  const [scanType, setScanType] = useState('xray'); // Default to X-Ray
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select an image asset before processing.");
      return;
    }

    setLoading(true);
    setError(null);

    // Attach BOTH the image and the selected scan type
    const formData = new FormData();
    formData.append('file', file);
    formData.append('scan_type', scanType); 

    try {
      const response = await fetch('http://localhost:8000/api/v1/analyze', {
        method: 'POST',
        body: formData, // the browser automatically sets the correct multipart headers
      });

      if (!response.ok) throw new Error(`Inference returned code: ${response.status}`);

      const data = await response.json();
      onAnalysisComplete(data.prediction, data.confidence);
    } catch (err) {
      setError(err.message || "Network exception encountered.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: '2px dashed #ccc', padding: '50px 20px', borderRadius: '8px', textAlign: 'center', backgroundColor: '#fff' }}>
      <form onSubmit={handleUpload} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
        
        {/* New Dropdown for Scan Type */}
        <div>
          <label style={{ marginRight: '10px', fontWeight: '500' }}>Image Modality:</label>
          <select 
            value={scanType} 
            onChange={(e) => setScanType(e.target.value)}
            style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            disabled={loading}
          >
            <option value="xray">Chest X-Ray</option>
            <option value="ecg">ECG Image</option>
          </select>
        </div>

        <input 
          type="file" 
          accept="image/jpeg, image/png, image/jpg" 
          onChange={handleFileChange} 
          style={{ fontSize: '14px' }}
        />
        
        {error && <p style={{ color: '#d32f2f', fontSize: '14px', margin: '0' }}>{error}</p>}
        
        <button 
          type="submit" 
          disabled={loading || !file}
          style={{ 
            padding: '12px 24px', 
            fontSize: '14px', 
            fontWeight: '500',
            cursor: loading ? 'not-allowed' : 'pointer',
            backgroundColor: loading ? '#eaeaea' : '#1976d2',
            color: loading ? '#888' : '#fff',
            border: 'none',
            borderRadius: '4px'
          }}
        >
          {loading ? "Running Neural Inference..." : "Submit Scan for Analysis"}
        </button>
      </form>
    </div>
  );
}

export default ImageUploader;