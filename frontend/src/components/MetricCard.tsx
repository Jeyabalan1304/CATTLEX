import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: {
    value: string;
    positive: boolean;
  };
  color?: 'brand' | 'amber' | 'rose' | 'blue' | 'purple';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  color = 'brand'
}) => {
  const colorMap = {
    brand: 'text-emerald-400 bg-emerald-950/40 border-emerald-800/40',
    amber: 'text-amber-400 bg-amber-950/40 border-amber-800/40',
    rose: 'text-rose-400 bg-rose-950/40 border-rose-800/40',
    blue: 'text-sky-400 bg-sky-950/40 border-sky-800/40',
    purple: 'text-purple-400 bg-purple-950/40 border-purple-800/40'
  }[color];

  return (
    <div className="glass-panel rounded-xl p-5 hover:border-slate-700 transition-all duration-300 relative overflow-hidden group">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs uppercase tracking-wider font-semibold text-slate-400">{title}</p>
          <p className="text-2xl lg:text-3xl font-bold mt-1.5 text-slate-100 font-sans tracking-tight">{value}</p>
          {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-lg border ${colorMap} group-hover:scale-110 transition-transform duration-300`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      {trend && (
        <div className="mt-3 flex items-center gap-1 text-xs">
          <span className={trend.positive ? 'text-emerald-400' : 'text-rose-400 font-medium'}>
            {trend.value}
          </span>
          <span className="text-slate-500">vs historical baseline</span>
        </div>
      )}
    </div>
  );
};
