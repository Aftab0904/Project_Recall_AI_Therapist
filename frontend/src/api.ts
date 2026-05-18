import { 
  MemoryRecord, IngestResponse, OpeningMessageResponse, 
  NotificationTriggerResponse 
} from './types';

const API_BASE = '/api';

export const api = {
  health: () => fetch(`${API_BASE}/health`).then(res => res.json()),
  
  ingest: (): Promise<IngestResponse> => 
    fetch(`${API_BASE}/ingest`, { method: 'POST' }).then(res => res.json()),
  
  startSession: (userId: string, currentMessage?: string): Promise<OpeningMessageResponse> =>
    fetch(`${API_BASE}/session/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, current_message: currentMessage })
    }).then(res => res.json()),
  
  getMemories: (userId: string): Promise<MemoryRecord[]> =>
    fetch(`${API_BASE}/memories/${userId}`).then(res => res.json()),
  
  deleteMemory: (memoryId: string): Promise<any> =>
    fetch(`${API_BASE}/memories/${memoryId}`, { method: 'DELETE' }).then(res => res.json()),
  
  excludeMemory: (userId: string, memoryId?: string, contentToExclude?: string): Promise<any> =>
    fetch(`${API_BASE}/memories/exclude`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        user_id: userId, 
        memory_id: memoryId, 
        content_to_exclude: contentToExclude 
      })
    }).then(res => res.json()),
  
  triggerNotification: (userId: string): Promise<NotificationTriggerResponse> =>
    fetch(`${API_BASE}/notifications/trigger`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId })
    }).then(res => res.json()),
  
  resetDemo: (): Promise<any> =>
    fetch(`${API_BASE}/demo/reset`, { method: 'POST' }).then(res => res.json()),
};
