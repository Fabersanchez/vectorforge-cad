import React from 'react';
import { Layers, Activity, FileCode2, Terminal } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-surface-border bg-background/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand Logo & Name */}
        <div className="flex items-center space-x-4">
          <div className="relative p-3 rounded-2xl bg-gradient-to-br from-accent-cyan/20 to-accent-purple/20 border border-accent-cyan/30 shadow-glow-cyan">
            <Layers className="w-7 h-7 text-accent-cyan" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400">
                CADVector Pro
              </h1>
              <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-accent-cyan/10 text-accent-cyan border border-accent-cyan/30">
                v1.0 Enterprise
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono">
              Plataforma de Conversión PDF Vectorial → DXF
            </p>
          </div>
        </div>

        {/* Right System Indicators */}
        <div className="flex items-center space-x-6">
          <div className="hidden sm:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-surface border border-surface-border text-xs text-slate-300">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-emerald opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-emerald"></span>
            </span>
            <span className="font-mono">Engine PyMuPDF + ezdxf</span>
          </div>

          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-surface hover:bg-slate-800 border border-surface-border text-sm text-slate-300 hover:text-white transition-all duration-200"
          >
            <Terminal className="w-4 h-4 text-accent-purple" />
            <span>API Docs</span>
          </a>
        </div>
      </div>
    </header>
  );
};
