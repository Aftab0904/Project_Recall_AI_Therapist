import React from 'react';
import { ShieldAlert } from 'lucide-react';

interface SafetyBadgeProps {
  notes?: string;
}

export const SafetyBadge: React.FC<SafetyBadgeProps> = ({ notes }) => {
  if (!notes) return null;

  return (
    <div className="flex items-center gap-2 p-2 mb-4 text-sm bg-orange-50 text-orange-700 border border-orange-200 rounded-lg">
      <ShieldAlert size={16} />
      <span>{notes}</span>
    </div>
  );
};
