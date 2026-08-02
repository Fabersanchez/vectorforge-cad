import React, { useState } from 'react';
import { History, Search, Trash2, Download, CheckCircle2, FileText } from 'lucide-react';
import { HistoryItem } from '../types/conversion';

interface HistoryTableProps {
  history: HistoryItem[];
  onDownload: (jobId: string) => void;
  onClear: () => void;
}

export const HistoryTable: React.FC<HistoryTableProps> = ({ history, onDownload, onClear }) => {
  const [search, setSearch] = useState('');

  const filteredHistory = history.filter(
    (item) =>
      item.original_name.toLowerCase().includes(search.toLowerCase()) ||
      item.job_id.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="bg-surface/80 border border-surface-border rounded-3xl p-6 backdrop-blur-xl space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-border pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-accent-cyan/20 text-accent-cyan border border-accent-cyan/30">
            <History className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white">Historial de Conversiones</h2>
            <p className="text-xs text-slate-400">Registro persistente de archivos procesados</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Buscar por nombre..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-xl pl-9 pr-4 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-accent-cyan w-48 sm:w-64"
            />
          </div>

          {history.length > 0 && (
            <button
              type="button"
              onClick={onClear}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs transition-all"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Limpiar</span>
            </button>
          )}
        </div>
      </div>

      {filteredHistory.length === 0 ? (
        <div className="text-center py-12 text-slate-500 text-sm">
          No hay registros de conversiones previas.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="py-3 px-4">Archivo PDF</th>
                <th className="py-3 px-4">DXF Generado</th>
                <th className="py-3 px-4">Versión DXF</th>
                <th className="py-3 px-4">Entidades Total</th>
                <th className="py-3 px-4">Fecha</th>
                <th className="py-3 px-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {filteredHistory.map((item) => (
                <tr key={item.job_id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 font-medium text-white flex items-center space-x-2">
                    <FileText className="w-4 h-4 text-accent-cyan" />
                    <span>{item.original_name}</span>
                  </td>
                  <td className="py-3 px-4 font-mono text-slate-400">{item.dxf_name}</td>
                  <td className="py-3 px-4 font-mono text-accent-purple font-semibold">
                    DXF {item.dxf_version}
                  </td>
                  <td className="py-3 px-4 font-mono text-accent-emerald">
                    {item.stats?.optimized_counts?.total ?? '—'}
                  </td>
                  <td className="py-3 px-4 text-slate-400">
                    {new Date(item.created_at).toLocaleString()}
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      type="button"
                      onClick={() => onDownload(item.job_id)}
                      className="p-1.5 rounded-lg bg-accent-cyan/10 hover:bg-accent-cyan/20 text-accent-cyan border border-accent-cyan/30 transition-all"
                      title="Descargar DXF"
                    >
                      <Download className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
