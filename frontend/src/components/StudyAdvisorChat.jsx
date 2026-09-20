import React, { useState, useRef, useEffect } from 'react';
import { X, Send, Bot, Sparkles, Loader2, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { API_BASE } from '../config';
import ReactMarkdown from 'react-markdown';

export default function StudyAdvisorChat({ isOpen, onClose, initialContext }) {
  const { currentUser, token } = useAuth();
  
  // Use initialContext as the first user message if provided
  const [messages, setMessages] = useState([
    { role: 'agent', content: 'Hello! I am your AI Study Advisor. How can I help you prepare for your exam today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (initialContext && isOpen && messages.length === 1) {
      handleSend(initialContext);
    }
  }, [initialContext, isOpen]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (messageText = input) => {
    if (!messageText.trim() || loading) return;
    const userMessage = messageText.trim();
    if (messageText === input) setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    if (!currentUser) {
      setMessages(prev => [...prev, { role: 'agent', content: 'Please log in to chat with the AI Study Advisor.' }]);
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/agent/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { Authorization: `Bearer ${token}` })
        },
        body: JSON.stringify({
          message: userMessage,
          user_id: currentUser.id,
          exam_id: 1 // hardcoded to GATE CS for hackathon
        })
      });
      
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'agent', content: data.response || "No response generated." }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'agent', content: 'Sorry, I encountered an error connecting to the server.' }]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-[#0f1219] border border-white/10 rounded-2xl w-full max-w-2xl h-[80vh] flex flex-col shadow-2xl shadow-indigo-500/10 overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-gradient-to-r from-indigo-500/10 to-purple-500/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center">
              <Bot size={20} className="text-indigo-400" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                AI Study Advisor
                <Sparkles size={14} className="text-amber-400" />
              </h3>
              <p className="text-[10px] text-slate-400">Powered by Google Antigravity SDK</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-white/5 rounded-lg text-slate-400 transition-colors">
            <X size={20} />
          </button>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-black/20">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex gap-3 max-w-[85%] ${m.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.role === 'user' ? 'bg-indigo-500/20' : 'bg-purple-500/20'}`}>
                  {m.role === 'user' ? <User size={16} className="text-indigo-400" /> : <Bot size={16} className="text-purple-400" />}
                </div>
                <div className={`p-4 rounded-2xl text-sm ${m.role === 'user' ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-white/5 text-slate-200 rounded-tl-none border border-white/5'}`}>
                  {m.role === 'agent' ? (
                    <div className="prose prose-invert prose-sm max-w-none">
                      <ReactMarkdown>{m.content}</ReactMarkdown>
                    </div>
                  ) : (
                    m.content
                  )}
                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="flex gap-3 max-w-[85%]">
                <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center shrink-0">
                  <Bot size={16} className="text-purple-400" />
                </div>
                <div className="bg-white/5 border border-white/5 p-4 rounded-2xl rounded-tl-none flex items-center gap-3">
                  <Loader2 size={16} className="text-indigo-400 animate-spin" />
                  <span className="text-xs text-slate-400">Thinking and querying tools...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-white/5 bg-black/40">
          <div className="flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl p-1 pl-4 focus-within:border-indigo-500/50 transition-colors">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Ask for a study plan or topic stats..."
              className="flex-1 bg-transparent border-none text-sm text-white focus:outline-none focus:ring-0 placeholder:text-slate-500 py-3"
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white p-3 rounded-lg transition-colors"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
