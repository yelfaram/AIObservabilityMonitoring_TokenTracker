import React, { useState, useRef, useEffect } from 'react';
import './ChatWindow.css';

const ChatWindow = ({ setMetadata }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatRef = useRef();

  const scrollToBottom = () => {
    chatRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
  if (!input.trim()) return;

  const userMsg = { role: 'user', content: input };
  const newMessages = [...messages, userMsg];
  setMessages(newMessages);
  setInput('');

  try {
    const res = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: input })
    });

    const data = await res.json();

    // 👇 Add the bot response to the chat window
    const botMsg = { role: 'bot', content: data.response };
    setMessages(prev => [...prev, botMsg]);

    // 👇 Update observability metadata
    setBotResponse(data.response);
    setMetadata(data.meta);

  } catch (err) {
    console.error('Error fetching response:', err);
  }
};


  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <div className="chat-page">
      <div className="chat-window-container small center">
        <div className="chat-window-header">Chat Window</div>

        <div className="chat-history-box">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-message ${msg.role === 'bot' ? 'bot' : 'user'}`}
            >
              <span className="label">{msg.role === 'user' ? 'You' : 'Bot'}:</span> {msg.content}
            </div>
          ))}
          <div ref={chatRef} />
        </div>

        <div className="chat-input-bar">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask something..."
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
