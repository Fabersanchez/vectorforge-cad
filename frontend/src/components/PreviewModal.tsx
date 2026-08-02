import React, { useState } from 'react';
import { X, ZoomIn, ZoomOut, RotateCcw, Layers, FileImage, DraftingCompass } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { PreviewData } from '../types/conversion';

interface PreviewModalProps {
  previewData: PreviewData | null;
  onClose: () => void;
}

export const PreviewModal: React.FC<PreviewModalProps> = ({ previewData, onClose }) => {
  const [zoom, setZoom] = useState(1);

  if (!previewData) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative w-full max-w-6xl h-[85vh] bg-surface border border-surface-border rounded-3xl overflow-hidden flex flex-col shadow-2xl"
        >
          {/* Modal Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-surface-border bg-slate-900/80">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-xl bg-accent-cyan/10 text-accent-cyan border border-accent-cyan/30">
                <Layers className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Vista Previa Comparativa</h3>
                <p className="text-xs text-slate-400 font-mono">{previewData.filename}</p>
              </div>
            </div>

            {/* Controls & Close */}
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-1 bg-slate-800 p-1 rounded-xl border border-slate-700">
                <button
                  type="button"
                  onClick={() => setZoom((z) => Math.max(0.5, z - 0.2))}
                  className="p-1.5 hover:bg-slate-700 rounded-lg text-slate-300 transition-all"
                  title="Alejar"
                >
                  <ZoomOut className="w-4 h-4" />
                </button>
                <span className="text-xs font-mono text-slate-300 px-2">{Math.round(zoom * 100)}%</span>
                <button
                  type="button"
                  onClick={() => setZoom((z) => Math.min(3, z + 0.2))}
                  className="p-1.5 hover:bg-slate-700 rounded-lg text-slate-300 transition-all"
                  title="Acercar"
                >
                  <ZoomIn className="w-4 h-4" />
                </button>
                <button
                  type="button"
                  onClick={() => setZoom(1)}
                  className="p-1.5 hover:bg-slate-700 rounded-lg text-slate-300 transition-all"
                  title="Restablecer"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>

              <button
                type="button"
                onClick={onClose}
                className="p-2 rounded-xl bg-slate-800 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 border border-slate-700 transition-all"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Dual Preview Content */}
          <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4 p-6 overflow-hidden">
            {/* Left: Original PDF Image */}
            <div className="flex flex-col bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden">
              <div className="flex items-center justify-between px-4 py-2 bg-slate-900 border-b border-slate-800">
                <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <FileImage className="w-4 h-4 text-accent-cyan" /> Rendering PDF Original
                </span>
                <span className="text-[10px] text-slate-500 font-mono">Raster Representation</span>
              </div>
              <div className="flex-1 overflow-auto p-4 flex items-center justify-center">
                {previewData.pdf_image ? (
                  <img
                    src={previewData.pdf_image}
                    alt="PDF Original"
                    style={{ transform: `scale(${zoom})`, transformOrigin: 'center center' }}
                    className="max-h-full object-contain transition-transform duration-150"
                  />
                ) : (
                  <div className="text-xs text-slate-500">Cargando PDF...</div>
                )}
              </div>
            </div>

            {/* Right: Vector DXF SVG Render */}
            <div className="flex flex-col bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden">
              <div className="flex items-center justify-between px-4 py-2 bg-slate-900 border-b border-slate-800">
                <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <DraftingCompass className="w-4 h-4 text-accent-purple" /> Geometría DXF Vectorial Extraída
                </span>
                <span className="text-[10px] text-accent-cyan font-mono">Precision CAD Renderer</span>
              </div>
              <div className="flex-1 overflow-auto p-4 flex items-center justify-center">
                {previewData.svg_vector ? (
                  <div
                    style={{ transform: `scale(${zoom})`, transformOrigin: 'center center' }}
                    className="w-full h-full transition-transform duration-150 flex items-center justify-center"
                    dangerouslySetInnerHTML={{ __html: previewData.svg_vector }}
                  />
                ) : (
                  <div className="text-xs text-slate-500">Cargando Geometría Vectorial...</div>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
