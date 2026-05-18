import React from 'react';
import { Bell, Info, X } from 'lucide-react';
import { NotificationTriggerResponse } from '../types';

interface NotificationPreviewProps {
  notification: NotificationTriggerResponse | null;
  onClose: () => void;
}

export const NotificationPreview: React.FC<NotificationPreviewProps> = ({ notification, onClose }) => {
  if (!notification) return null;

  return (
    <div className="fixed bottom-6 left-6 right-6 md:left-auto md:right-6 md:w-96 animate-in slide-in-from-right-10 duration-500 z-50">
      <div className="bg-white rounded-2xl shadow-2xl border border-mentra-soft overflow-hidden">
        <div className="p-4 bg-orange-50 border-b border-orange-100 flex items-center justify-between">
          <div className="flex items-center gap-2 text-orange-700 font-semibold">
            <Bell size={18} />
            <span>Smart Re-engagement</span>
          </div>
          <button onClick={onClose} className="text-orange-400 hover:text-orange-600">
            <X size={18} />
          </button>
        </div>

        <div className="p-6">
          {notification.should_send ? (
            <div className="space-y-4">
              <div className="p-3 bg-mentra-light rounded-xl border border-mentra-soft italic text-mentra-text/80 text-sm">
                "{notification.copy}"
              </div>
              <div className="flex gap-2 items-start text-xs text-mentra-text/60 bg-gray-50 p-3 rounded-lg">
                <Info size={14} className="shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold text-mentra-text/80">Trigger Rationale:</p>
                  <p>{notification.reason}</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-4">
              <p className="text-mentra-text/60 text-sm">No notification triggered.</p>
              <p className="text-xs text-mentra-text/40 mt-1">Reason: {notification.reason}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
