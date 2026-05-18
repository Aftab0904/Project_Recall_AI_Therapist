import { useState, useEffect } from 'react';
import { ChatPanel } from './components/ChatPanel';
import { MemorySidebar } from './components/MemorySidebar';
import { SimulationBar } from './components/SimulationBar';
import { NotificationPreview } from './components/NotificationPreview';
import { api } from './api';
import { MemoryRecord, OpeningMessageResponse, NotificationTriggerResponse } from './types';
import { Heart } from 'lucide-react';

const USER_ID = 'demo_user';

function App() {
  const [memories, setMemories] = useState<MemoryRecord[]>([]);
  const [opener, setOpener] = useState<OpeningMessageResponse | undefined>();
  const [notification, setNotification] = useState<NotificationTriggerResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchMemories = async () => {
    try {
      const data = await api.getMemories(USER_ID);
      setMemories(data);
    } catch (err) {
      console.error('Failed to fetch memories', err);
    }
  };

  useEffect(() => {
    fetchMemories();
  }, []);

  const handleIngest = async () => {
    setIsLoading(true);
    try {
      await api.ingest();
      await fetchMemories();
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartSession = async (message?: string) => {
    setIsLoading(true);
    try {
      const data = await api.startSession(USER_ID, message);
      setOpener(data);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTriggerNotification = async () => {
    setIsLoading(true);
    try {
      const data = await api.triggerNotification(USER_ID);
      setNotification(data);
    } finally {
      setIsLoading(false);
    }
  };

  const handleForget = async (id: string) => {
    try {
      await api.deleteMemory(id);
      await fetchMemories();
    } catch (err) {
      console.error('Failed to delete memory', err);
    }
  };

  const handleReset = async () => {
    if (confirm('Are you sure you want to reset all demo data?')) {
      setIsLoading(true);
      try {
        await api.resetDemo();
        setMemories([]);
        setOpener(undefined);
        setNotification(null);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-mentra-light overflow-hidden">
      {/* Header */}
      <header className="px-6 py-4 bg-white border-b border-mentra-soft flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-mentra-sage rounded-xl flex items-center justify-center text-white shadow-md shadow-mentra-sage/20">
            <Heart size={24} fill="currentColor" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-mentra-text tracking-tight">Mentra</h1>
            <p className="text-[10px] text-mentra-sage font-bold uppercase tracking-widest">Recall System</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4 text-sm text-mentra-text/60">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-green-400"></span>
            System Online
          </span>
        </div>
      </header>

      {/* Simulation Controls */}
      <SimulationBar 
        onIngest={handleIngest}
        onStartSession={() => handleStartSession()}
        onTriggerNotification={handleTriggerNotification}
        onReset={handleReset}
        isLoading={isLoading}
      />

      {/* Main Content */}
      <main className="flex-1 flex overflow-hidden">
        <div className="flex-1 p-6 flex flex-col min-w-0">
          <ChatPanel 
            opener={opener} 
            isLoading={isLoading}
            onSendMessage={(msg) => handleStartSession(msg)}
          />
        </div>
        
        <MemorySidebar 
          memories={memories} 
          onForget={handleForget} 
        />
      </main>

      <NotificationPreview 
        notification={notification} 
        onClose={() => setNotification(null)} 
      />

      {isLoading && (
        <div className="fixed inset-0 bg-white/20 backdrop-blur-[1px] flex items-center justify-center z-50">
          <div className="flex flex-col items-center gap-3">
            <div className="w-10 h-10 border-4 border-mentra-sage/20 border-t-mentra-sage rounded-full animate-spin"></div>
            <p className="text-sm font-medium text-mentra-sage animate-pulse">Processing Context...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
