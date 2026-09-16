import React from 'react';

interface StatusBadgeProps {
  status: string;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const normalized = status.toUpperCase();

  let colorClasses = 'bg-slate-800 text-slate-300 border-slate-700';
  let dotClass = 'bg-slate-400';

  if (normalized === 'HEALTHY' || normalized === 'RESOLVED' || normalized === 'COMPLETED') {
    colorClasses = 'bg-emerald-950/80 text-emerald-400 border-emerald-800/60';
    dotClass = 'bg-emerald-400 animate-pulse';
  } else if (normalized === 'AT_RISK' || normalized === 'WARNING' || normalized === 'MEDIUM' || normalized === 'PENDING') {
    colorClasses = 'bg-amber-950/80 text-amber-400 border-amber-800/60';
    dotClass = 'bg-amber-400 animate-ping';
  } else if (normalized === 'CRITICAL' || normalized === 'URGENT' || normalized === 'HIGH') {
    colorClasses = 'bg-rose-950/80 text-rose-400 border-rose-800/60';
    dotClass = 'bg-rose-500 animate-ping';
  }

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-xs px-2.5 py-1',
    lg: 'text-sm px-3.5 py-1.5 font-medium'
  }[size];

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border ${sizeClasses} ${colorClasses} font-semibold shadow-sm`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dotClass}`} />
      {normalized.replace('_', ' ')}
    </span>
  );
};
