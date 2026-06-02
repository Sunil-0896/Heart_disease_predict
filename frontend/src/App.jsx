import React, { useState } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [diagnosis, setDiagnosis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // FIX: Clean up the old blob URL from memory before creating a new one
      if (preview) URL.revokeObjectURL(preview); 
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setDiagnosis(data);
      setMessages([
        {
          sender: "system",
          text: `Analysis Complete. Result: ${data.prediction} (${(data.confidence * 100).toFixed(1)}% confidence). You can now ask questions regarding this finding.`,
        },
      ]);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || !diagnosis) return;

    const userMsg = { sender: "user", text: inputMessage };
    
    // Create the updated message array immediately so we can send it to the backend
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInputMessage("");

    // FIX: Filter out system messages and send the full history as JSON
    const chatHistory = updatedMessages.filter(msg => msg.sender !== "system");

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Switch to JSON
        },
        body: JSON.stringify({
          history: chatHistory,
          diagnosis: diagnosis.prediction,
          confidence: diagnosis.confidence,
        }),
      });
      
      const data = await response.json();
      setMessages((prev) => [...prev, { sender: "bot", text: data.reply }]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px", fontFamily: "sans-serif" }}>
      <h2>AI Medical Dashboard & Chatbot</h2>
      
      <div style={{ border: "1px solid #ccc", padding: "20px", borderRadius: "8px", marginBottom: "20px" }}>
        <h3>1. Image Analysis</h3>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        {preview && (
          <div style={{ marginTop: "15px" }}>
            <img src={preview} alt="Preview" style={{ maxWidth: "100%", maxHeight: "200px", borderRadius: "4px" }} />
          </div>
        )}
        <button 
          onClick={handleUpload} 
          disabled={!file || loading} 
          style={{ marginTop: "15px", display: "block", padding: "10px 15px", cursor: "pointer" }}
        >
          {loading ? "Analyzing..." : "Run Diagnostic Pipeline"}
        </button>
      </div>

      {diagnosis && (
        <div style={{ border: "1px solid #ccc", padding: "20px", borderRadius: "8px" }}>
          <h3>2. Interactive Clinical Chat</h3>
          <div style={{ height: "300px", overflowY: "scroll", border: "1px solid #eee", padding: "10px", marginBottom: "15px", borderRadius: "4px" }}>
            {messages.map((msg, idx) => (
              <div key={idx} style={{ marginBottom: "10px", textAlign: msg.sender === "user" ? "right" : "left" }}>
                <span style={{ display: "inline-block", padding: "8px 12px", borderRadius: "4px", backgroundColor: msg.sender === "user" ? "#e1f5fe" : msg.sender === "system" ? "#fff3e0" : "#f5f5f5" }}>
                  {msg.text}
                </span>
              </div>
            ))}
          </div>
          <form onSubmit={handleSendMessage} style={{ display: "flex", gap: "10px" }}>
            <input 
              type="text" 
              value={inputMessage} 
              onChange={(e) => setInputMessage(e.target.value)} 
              placeholder="Ask about your metrics, precautions, or next steps..." 
              style={{ flexGrow: 1, padding: "10px" }}
            />
            <button type="submit" style={{ padding: "10px 20px", cursor: "pointer" }}>Send</button>
          </form>
        </div>
      )}
    </div>
  );
}