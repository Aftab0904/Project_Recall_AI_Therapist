import React from 'react';
import { Play, RotateCcw, Database, Bell, PlusCircle } from 'lucide-react';

interface SimulationBarProps {
  onIngest: () => void;
  onStartSession: () => void;
  onTriggerNotification: () => void;
  onReset: () => void;
  isLoading: boolean;
}

export const SimulationBar: React.FC<SimulationBarProps> = ({ 
  onIngest, onStartSession, onTriggerNotification, onReset, isLoading 
}) => {
  return (
    <div className="flex gap-4 p-4 bg-mentra-soft/30 border-b border-mentra-soft overflow-x-auto no-scrollbar">
      <button
        onClick={onIngest}
        disabled={isLoading}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-mentra-soft rounded-lg text-sm font-medium text-mentra-text hover:bg-mentra-sage/10 transition-colors shrink-0 disabled:opacity-50"
      >
        <Database size={16} className="text-mentra-sage" />
        Ingest Samples
      </button>

      <button
        onClick={onStartSession}
        disabled={isLoading}
        className="flex items-center gap-2 px-4 py-2 bg-mentra-sage text-white rounded-lg text-sm font-medium hover:bg-mentra-sage/90 transition-colors shadow-sm shadow-mentra-sage/20 shrink-0 disabled:opacity-50"
      >
        <PlusCircle size={16} />
        New Session
      </button>

      <button
        onClick={onTriggerNotification}
        disabled={isLoading}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-mentra-soft rounded-lg text-sm font-medium text-mentra-text hover:bg-mentra-rose transition-colors shrink-0 disabled:opacity-50"
      >
        <Bell size={16} className="text-orange-400" />
        Trigger Notification
      </button>

      <div className="flex-1" />

      <button
        onClick={onReset}
        disabled={isLoading}
        className="flex items-center gap-2 px-4 py-2 text-red-500 hover:bg-red-50 rounded-lg text-sm font-medium transition-colors shrink-0 disabled:opacity-50"
      >
        <RotateCcw size={16} />
        Reset Demo
      </button>
    </div>
  );
};
