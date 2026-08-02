import React from 'react';
import { Activity, Clock, ShieldCheck, FileCheck, Layers, Hash } from 'lucide-react';
import { OptimizationStats } from '../types/conversion';

interface StatsCardProps {
  stats: OptimizationStats;
}

export const StatsCard: React.FC<StatsCardProps> = ({ stats }) => {
  const opt = stats.optimized_counts;

  return (
    <div className="bg-surface/80 border border-surface-border rounded-3xl p-6 backdrop-blur-xl space-y-6">
      <div className="flex items-center justify-between border-b border-surface-border pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-accent-emerald/20 text-accent-emerald border border-accent-emerald/30">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white">Métricas y Estadísticas Geométricas</h2>
            <p className="text-xs text-slate-400">Resumen detallado del motor de optimización CAD</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <span className="px-3 py-1 rounded-full bg-accent-emerald/10 border border-accent-emerald/30 text-xs font-semibold text-accent-emerald">
            -{stats.optimization_percentage}% Reducción
          </span>
        </div>
      </div>

      {/* Grid of Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4 text-center">
        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <div className="text-xs text-slate-400">Líneas (LINE)</div>
          <div className="text-lg font-bold text-accent-cyan font-mono mt-1">{opt.lines}</div>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <div className="text-xs text-slate-400">Polígonos (LWPOLY)</div>
          <div className="text-lg font-bold text-accent-purple font-mono mt-1">{opt.polylines}</div>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <div className="text-xs text-slate-400">Arcos (ARC)</div>
          <div className="text-lg font-bold text-accent-pink font-mono mt-1">{opt.arcs}</div>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <div className="text-xs text-slate-400">Círculos (CIRCLE)</div>
          <div className="text-lg font-bold text-accent-emerald font-mono mt-1">{opt.circles}</div>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <div className="text-xs text-slate-400">Textos (TEXT)</div>
          <div className="text-lg font-bold text-amber-400 font-mono mt-1">{opt.texts}</div>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <div className="text-xs text-slate-400">Tiempo Conversión</div>
          <div className="text-lg font-bold text-white font-mono mt-1">{stats.execution_time_seconds}s</div>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <div className="text-xs text-slate-400">Total Entidades</div>
          <div className="text-lg font-bold text-accent-cyan font-mono mt-1">{opt.total}</div>
        </div>
      </div>
    </div>
  );
};
