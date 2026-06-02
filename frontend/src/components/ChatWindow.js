import React, { useState, useRef, useEffect } from 'react';

function ChatWindow({ prediction, confidence }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: `Hello, I have synthesized the image metrics indicating '${prediction}'. How can I help clarify these findings for you?` }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatBottomRef = useRef(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userText = input;
    setInput('');
    
    const updatedHistory = [...messages, { role: 'user', content: userText }];
    setMessages(updatedHistory);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: userText,
          prediction_context: prediction,
          confidence_context: confidence,
          chat_history: updatedHistory.slice(1, -1) 
        }),
      });

      if (!response.ok) throw new Error("Faulty state matching response stream.");

      const data = await response.json();
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'assistant', content: "Communication failure. Backend text engine is unavailable." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: '8px', padding: '20px', backgroundColor: '#fff', boxShadow: '0 2px 4px rgba(0,0,0,0.02)' }}>
      <div style={{ height: '350px', overflowY: 'auto', marginBottom: '20px', paddingRight: '5px' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: '16px', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
            <div style={{ fontSize: '12px', color: '#888', marginBottom: '4px' }}>
              {msg.role === 'user' ? 'Patient' : 'Clinical AI Assistant'}
            </div>
            <span style={{ 
              display: 'inline-block', 
              padding: '10px 16px', 
              borderRadius: '8px', 
              backgroundColor: msg.role === 'user' ? '#e3f2fd' : '#f5f5f5',
              color: '#333',
              maxWidth: '80%',
              textAlign: 'left',
              fontSize: '14px',
              lineHeight: '1.5'
            }}>
              {msg.content}
            </span>
          </div>
        ))}
        {loading && <p style={{ color: '#999', fontSize: '13px' }}>Assistant is processing clinical query...</p>}
        <div ref={chatBottomRef} />
      </div>

      <form onSubmit={handleSendMessage} style={{ display: 'flex', gap: '10px' }}>
        <input 
          type="text" 
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about precautions, terminology, or general details..."
          style={{ flexGrow: 1, padding: '12px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '14px' }}
          disabled={loading}
        />
        <button 
          type="submit" 
          disabled={loading || !input.trim()} 
          style={{ 
            padding: '0 24px', 
            borderRadius: '4px', 
            border: 'none', 
            backgroundColor: '#2e7d32', 
            color: '#fff', 
            fontWeight: '500', 
            cursor: 'pointer' 
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatWindow;