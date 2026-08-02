import React from 'react';
import { FileText, Download, Eye, CheckCircle2, AlertTriangle, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { ConversionJob } from '../types/conversion';

interface FileCardProps {
  job: ConversionJob;
  onPreview: (jobId: string) => void;
  onDownload: (jobId: string) => void;
}

export const FileCard: React.FC<FileCardProps> = ({ job, onPreview, onDownload }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-surface/90 border border-surface-border rounded-2xl p-5 backdrop-blur-md flex flex-col justify-between space-y-4 hover:border-slate-600 transition-all duration-200"
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3.5">
          <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-accent-cyan">
            <FileText className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white line-clamp-1 max-w-[220px]" title={job.filename}>
              {job.filename}
            </h3>
            <div className="flex items-center space-x-2 mt-1">
              <span className="text-xs text-slate-400 font-mono">
                ID: {job.job_id}
              </span>
              <span className="text-slate-600">•</span>
              <span className="text-xs text-slate-400">
                {new Date(job.created_at).toLocaleTimeString()}
              </span>
            </div>
          </div>
        </div>

        {/* Status Badge */}
        <div>
          {job.status === 'completed' && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-accent-emerald/10 border border-accent-emerald/30 text-xs font-semibold text-accent-emerald">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Completado
            </span>
          )}
          {job.status === 'processing' && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-accent-cyan/10 border border-accent-cyan/30 text-xs font-semibold text-accent-cyan animate-pulse">
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              Procesando ({job.progress}%)
            </span>
          )}
          {job.status === 'pending' && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-300">
              Pendiente
            </span>
          )}
          {job.status === 'failed' && (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-xs font-semibold text-rose-400">
              <AlertTriangle className="w-3.5 h-3.5" />
              Error
            </span>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      {job.status === 'processing' && (
        <div className="w-full bg-slate-900 h-2 rounded-full overflow-hidden border border-slate-800">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${job.progress}%` }}
            className="bg-gradient-to-r from-accent-cyan to-accent-purple h-full rounded-full"
          />
        </div>
      )}

      {/* Optimization summary if completed */}
      {job.status === 'completed' && job.stats && (
        <div className="bg-slate-900/80 rounded-xl p-3 border border-slate-800 text-xs grid grid-cols-3 gap-2 text-center">
          <div>
            <div className="text-slate-400">Líneas / Polígonos</div>
            <div className="font-semibold text-white font-mono mt-0.5">
              {job.stats.optimized_counts.lines + job.stats.optimized_counts.polylines}
            </div>
          </div>
          <div>
            <div className="text-slate-400">Optimización</div>
            <div className="font-semibold text-accent-emerald font-mono mt-0.5">
              -{job.stats.optimization_percentage}%
            </div>
          </div>
          <div>
            <div className="text-slate-400">Tiempo</div>
            <div className="font-semibold text-accent-cyan font-mono mt-0.5">
              {job.stats.execution_time_seconds}s
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center justify-end space-x-3 pt-2">
        <button
          type="button"
          onClick={() => onPreview(job.job_id)}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 transition-all"
        >
          <Eye className="w-3.5 h-3.5 text-accent-cyan" />
          <span>Vista Previa</span>
        </button>

        {job.status === 'completed' && (
          <button
            type="button"
            onClick={() => onDownload(job.job_id)}
            className="flex items-center space-x-1.5 px-4 py-1.5 rounded-xl bg-gradient-to-r from-accent-cyan/20 to-accent-purple/20 hover:from-accent-cyan/30 hover:to-accent-purple/30 border border-accent-cyan/40 text-xs font-semibold text-white shadow-glow-cyan transition-all"
          >
            <Download className="w-3.5 h-3.5 text-accent-cyan" />
            <span>Descargar DXF</span>
          </button>
        )}
      </div>
    </motion.div>
  );
};
