import React from 'react';
import { LucideIcon } from 'lucide-react';

interface GaugeCardProps {
  title: string;
  value: number;
  unit: string;
  min: number;
  max: number;
  normalMin: number;
  normalMax: number;
  icon: LucideIcon;
  sensorModel: string;
}

export const GaugeCard: React.FC<GaugeCardProps> = ({
  title,
  value,
  unit,
  min,
  max,
  normalMin,
  normalMax,
  icon: Icon,
  sensorModel
}) => {
  const percentage = Math.min(Math.max(((value - min) / (max - min)) * 100, 0), 100);

  const isNormal = value >= normalMin && value <= normalMax;
  const isHigh = value > normalMax;
  const isLow = value < normalMin;

  let statusColor = 'text-emerald-400 bg-emerald-500';
  let statusText = 'Normal';
  let badgeColor = 'bg-emerald-950/80 text-emerald-400 border-emerald-800/60';

  if (isHigh) {
    statusColor = 'text-rose-400 bg-rose-500';
    statusText = 'Elevated';
    badgeColor = 'bg-rose-950/80 text-rose-400 border-rose-800/60';
  } else if (isLow) {
    statusColor = 'text-amber-400 bg-amber-500';
    statusText = 'Subnormal';
    badgeColor = 'bg-amber-950/80 text-amber-400 border-amber-800/60';
  }

  return (
    <div className="glass-panel rounded-xl p-5 relative overflow-hidden flex flex-col justify-between">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-slate-800/80 border border-slate-700 text-slate-300">
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-slate-200">{title}</h4>
            <span className="text-[10px] text-slate-400 font-mono tracking-tight">{sensorModel}</span>
          </div>
        </div>
        <span className={`text-[11px] font-medium px-2 py-0.5 rounded-full border ${badgeColor}`}>
          {statusText}
        </span>
      </div>

      <div className="my-4">
        <div className="flex items-baseline gap-1.5">
          <span className="text-3xl lg:text-4xl font-extrabold text-slate-100 font-mono tracking-tight">
            {value.toFixed(1)}
          </span>
          <span className="text-sm text-slate-400 font-medium">{unit}</span>
        </div>
        <p className="text-[11px] text-slate-400 mt-1">
          Normal ref: {normalMin} – {normalMax} {unit}
        </p>
      </div>

      <div>
        <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-700/60">
          <div
            className={`h-full rounded-full transition-all duration-700 ease-out ${statusColor.split(' ')[1]}`}
            style={{ width: `${percentage}%` }}
          />
        </div>
        <div className="flex justify-between text-[10px] text-slate-400 font-mono mt-1">
          <span>{min} {unit}</span>
          <span>{max} {unit}</span>
        </div>
      </div>
    </div>
  );
};
