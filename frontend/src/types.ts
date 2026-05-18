export type MemoryType = 'core_profile' | 'session_ephemeral' | 'safety_signal';
export type SensitivityLevel = 'low' | 'medium' | 'high' | 'critical';
export type MemoryStatus = 'active' | 'resolved' | 'deleted' | 'archived';

export interface MemoryRecord {
  id: string;
  user_id: string;
  source_session_id?: string;
  memory_type: MemoryType;
  theme: string;
  summary: string;
  emotional_tone: string;
  status: MemoryStatus;
  importance: number;
  sensitivity: SensitivityLevel;
  safe_to_reference: boolean;
  created_at: string;
  last_mentioned_at?: string;
  deleted_at?: string;
}

export interface IngestResponse {
  session_count: number;
  memories_extracted: number;
  summary: string[];
}

export interface OpeningMessageResponse {
  message: string;
  memories_used: string[];
  safety_notes?: string;
}

export interface NotificationTriggerResponse {
  should_send: boolean;
  scenario?: string;
  reason?: string;
  copy?: string;
}
