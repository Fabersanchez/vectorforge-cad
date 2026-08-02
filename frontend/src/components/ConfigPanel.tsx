import React from 'react';
import { Settings2, Zap, Layers, FileText, Magnet } from 'lucide-react';
import { ConversionOptions, DXFVersion } from '../types/conversion';

interface ConfigPanelProps {
  options: ConversionOptions;
  onChange: (options: ConversionOptions) => void;
}

const DXF_VERSIONS: { value: DXFVersion; label: string; year: string }[] = [
  { value: "R12", label: "AutoCAD R12 / LT2", year: "1992" },
  { value: "R14", label: "AutoCAD R14", year: "1997" },
  { value: "2000", label: "AutoCAD 2000 / 2000i", year: "1999" },
  { value: "2004", label: "AutoCAD 2004", year: "2003" },
  { value: "2007", label: "AutoCAD 2007", year: "2006" },
  { value: "2010", label: "AutoCAD 2010", year: "2009" },
  { value: "2013", label: "AutoCAD 2013", year: "2012" },
  { value: "2018", label: "AutoCAD 2018 / 2024+", year: "2017" },
];

export const ConfigPanel: React.FC<ConfigPanelProps> = ({ options, onChange }) => {
  return (
    <div className="bg-surface/80 border border-surface-border rounded-3xl p-6 backdrop-blur-xl space-y-6">
      <div className="flex items-center justify-between border-b border-surface-border pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-xl bg-accent-purple/20 text-accent-purple border border-accent-purple/30">
            <Settings2 className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white">Parámetros de Conversión DXF</h2>
            <p className="text-xs text-slate-400">Configure la versión de salida y opciones de optimización</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* DXF Version Selector */}
        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Versión del Formato DXF
          </label>
          <select
            value={options.dxf_version}
            onChange={(e) => onChange({ ...options, dxf_version: e.target.value as DXFVersion })}
            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-accent-cyan transition-all"
          >
            {DXF_VERSIONS.map((v) => (
              <option key={v.value} value={v.value}>
                DXF {v.value} — {v.label} ({v.year})
              </option>
            ))}
          </select>
        </div>

        {/* Snap Tolerance */}
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <Magnet className="w-3.5 h-3.5 text-accent-cyan" /> Tolerancia de Ajuste de Vértices (mm)
            </label>
            <span className="text-xs font-mono text-accent-cyan">{options.snap_tolerance} mm</span>
          </div>
          <input
            type="range"
            min="0.00001"
            max="0.01"
            step="0.00005"
            value={options.snap_tolerance}
            onChange={(e) => onChange({ ...options, snap_tolerance: parseFloat(e.target.value) })}
            className="w-full accent-accent-cyan bg-slate-800 rounded-lg cursor-pointer"
          />
        </div>
      </div>

      {/* Toggles */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
        {/* Remove Duplicates */}
        <div
          onClick={() => onChange({ ...options, remove_duplicates: !options.remove_duplicates })}
          className={`cursor-pointer p-4 rounded-2xl border transition-all flex items-start space-x-3 ${
            options.remove_duplicates
              ? 'bg-accent-cyan/10 border-accent-cyan/50 text-white'
              : 'bg-slate-900/60 border-slate-800 text-slate-400'
          }`}
        >
          <Zap className={`w-5 h-5 mt-0.5 ${options.remove_duplicates ? 'text-accent-cyan' : 'text-slate-500'}`} />
          <div>
            <div className="text-xs font-semibold">Eliminar Duplicados</div>
            <div className="text-[11px] text-slate-400 mt-0.5">Depura líneas e hilos solapados</div>
          </div>
        </div>

        {/* Join Segments */}
        <div
          onClick={() => onChange({ ...options, join_segments: !options.join_segments })}
          className={`cursor-pointer p-4 rounded-2xl border transition-all flex items-start space-x-3 ${
            options.join_segments
              ? 'bg-accent-purple/10 border-accent-purple/50 text-white'
              : 'bg-slate-900/60 border-slate-800 text-slate-400'
          }`}
        >
          <Layers className={`w-5 h-5 mt-0.5 ${options.join_segments ? 'text-accent-purple' : 'text-slate-500'}`} />
          <div>
            <div className="text-xs font-semibold">Unir Polígonos</div>
            <div className="text-[11px] text-slate-400 mt-0.5">Crea entidades LWPOLYLINE</div>
          </div>
        </div>

        {/* Extract Text */}
        <div
          onClick={() => onChange({ ...options, extract_text: !options.extract_text })}
          className={`cursor-pointer p-4 rounded-2xl border transition-all flex items-start space-x-3 ${
            options.extract_text
              ? 'bg-accent-emerald/10 border-accent-emerald/50 text-white'
              : 'bg-slate-900/60 border-slate-800 text-slate-400'
          }`}
        >
          <FileText className={`w-5 h-5 mt-0.5 ${options.extract_text ? 'text-accent-emerald' : 'text-slate-500'}`} />
          <div>
            <div className="text-xs font-semibold">Extraer Textos</div>
            <div className="text-[11px] text-slate-400 mt-0.5">Conserva TEXT y MTEXT</div>
          </div>
        </div>
      </div>
    </div>
  );
};
