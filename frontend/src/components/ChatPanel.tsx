import React, { useState } from 'react';
import { Send, Bot, Sparkles } from 'lucide-react';
import { OpeningMessageResponse } from '../types';
import { SafetyBadge } from './SafetyBadge';

interface ChatPanelProps {
  opener?: OpeningMessageResponse;
  isLoading: boolean;
  onSendMessage: (msg: string) => void;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ opener, isLoading, onSendMessage }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-2xl shadow-sm border border-mentra-soft overflow-hidden">
      <div className="p-4 bg-mentra-soft/30 border-b border-mentra-soft flex items-center justify-between">
        <h2 className="text-lg font-medium text-mentra-text flex items-center gap-2">
          <Bot size={20} className="text-mentra-sage" />
          Mentra Assistant
        </h2>
        {opener?.memories_used && opener.memories_used.length > 0 && (
          <div className="flex items-center gap-1 text-xs text-mentra-sage font-medium bg-mentra-sage/10 px-2 py-1 rounded-full">
            <Sparkles size={12} />
            Context: {opener.memories_used.join(', ')}
          </div>
        )}
      </div>

      <div className="flex-1 p-6 overflow-y-auto space-y-6 bg-mentra-light/50">
        <SafetyBadge notes={opener?.safety_notes} />

        {opener ? (
          <div className="flex gap-3 max-w-[85%] animate-in fade-in slide-in-from-bottom-2 duration-500">
            <div className="w-8 h-8 rounded-full bg-mentra-sage flex items-center justify-center text-white shrink-0">
              <Bot size={18} />
            </div>
            <div className="p-4 bg-white rounded-2xl rounded-tl-none border border-mentra-soft shadow-sm">
              <p className="text-mentra-text leading-relaxed">
                {opener.message}
              </p>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-mentra-text/40 italic">
            Start a new session to begin.
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="p-4 bg-white border-t border-mentra-soft flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 p-3 bg-mentra-light border border-mentra-soft rounded-xl focus:outline-none focus:ring-2 focus:ring-mentra-sage/20 focus:border-mentra-sage transition-all"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="p-3 bg-mentra-sage text-white rounded-xl hover:bg-mentra-sage/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md shadow-mentra-sage/20"
        >
          <Send size={20} />
        </button>
      </form>
    </div>
  );
};
