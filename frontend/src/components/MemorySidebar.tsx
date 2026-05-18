import React from 'react';
import { Database, Trash2, Tag, Calendar, HeartPulse } from 'lucide-react';
import { MemoryRecord } from '../types';

interface MemorySidebarProps {
  memories: MemoryRecord[];
  onForget: (id: string) => void;
}

export const MemorySidebar: React.FC<MemorySidebarProps> = ({ memories, onForget }) => {
  return (
    <div className="w-80 h-full flex flex-col bg-mentra-soft/20 border-l border-mentra-soft overflow-hidden">
      <div className="p-4 border-b border-mentra-soft bg-white/50">
        <h2 className="text-lg font-medium text-mentra-text flex items-center gap-2">
          <Database size={20} className="text-mentra-sage" />
          AI Memory Transparency
        </h2>
        <p className="text-xs text-mentra-text/60 mt-1">
          These are the clusters Mentra remembers to personalize your care. You have full control.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {memories.length === 0 ? (
          <div className="text-center py-10 text-mentra-text/40 text-sm italic">
            No memories extracted yet. Ingest sample sessions to see data.
          </div>
        ) : (
          memories.map((memory) => (
            <div 
              key={memory.id} 
              className="bg-white p-4 rounded-xl border border-mentra-soft shadow-sm hover:shadow-md transition-shadow group"
            >
              <div className="flex justify-between items-start mb-2">
                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                  memory.memory_type === 'core_profile' 
                    ? 'bg-blue-50 text-blue-600' 
                    : 'bg-purple-50 text-purple-600'
                }`}>
                  {memory.memory_type.replace('_', ' ')}
                </span>
                <button 
                  onClick={() => onForget(memory.id)}
                  className="p-1.5 text-mentra-text/40 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                  title="Forget this memory"
                >
                  <Trash2 size={14} />
                </button>
              </div>
              
              <h3 className="text-sm font-semibold text-mentra-text mb-1 flex items-center gap-1">
                <Tag size={12} className="text-mentra-sage" />
                {memory.theme}
              </h3>
              
              <p className="text-sm text-mentra-text/80 leading-snug mb-3">
                {memory.summary}
              </p>
              
              <div className="flex items-center gap-3 text-[10px] text-mentra-text/50 border-t border-mentra-soft/50 pt-2">
                <div className="flex items-center gap-1">
                  <HeartPulse size={10} />
                  {memory.emotional_tone}
                </div>
                <div className="flex items-center gap-1">
                  <Calendar size={10} />
                  {new Date(memory.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
