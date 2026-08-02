import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileCheck2, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

interface DropzoneProps {
  onFilesSelected: (files: File[]) => void;
  disabled?: boolean;
}

export const Dropzone: React.FC<DropzoneProps> = ({ onFilesSelected, disabled = false }) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const pdfFiles = acceptedFiles.filter(
        (f) => f.name.toLowerCase().endsWith('.pdf')
      );
      if (pdfFiles.length > 0) {
        onFilesSelected(pdfFiles);
      }
    },
    [onFilesSelected]
  );

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: true,
    disabled,
  });

  return (
    <motion.div
      whileHover={{ scale: disabled ? 1 : 1.005 }}
      whileTap={{ scale: disabled ? 1 : 0.995 }}
      className="w-full"
    >
      <div
        {...getRootProps()}
        className={`relative cursor-pointer overflow-hidden rounded-3xl p-10 text-center transition-all duration-300 border-2 border-dashed ${
          isDragActive
            ? 'border-accent-cyan bg-accent-cyan/10 shadow-glow-cyan'
            : isDragReject
            ? 'border-rose-500 bg-rose-500/10'
            : 'border-slate-700 hover:border-slate-500 bg-surface/60 hover:bg-surface/80'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} />

        {/* Backdrop Glow */}
        <div className="absolute -inset-1 bg-gradient-to-r from-accent-cyan/10 via-accent-purple/10 to-accent-pink/10 opacity-30 blur-2xl pointer-events-none" />

        <div className="relative z-10 flex flex-col items-center justify-center space-y-4">
          <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-700/60 shadow-xl">
            {isDragActive ? (
              <FileCheck2 className="w-10 h-10 text-accent-cyan animate-bounce" />
            ) : isDragReject ? (
              <AlertCircle className="w-10 h-10 text-rose-500" />
            ) : (
              <UploadCloud className="w-10 h-10 text-slate-300" />
            )}
          </div>

          <div>
            <p className="text-lg font-semibold text-white">
              {isDragActive
                ? 'Suelte los archivos PDF vectoriales aquí...'
                : 'Arrastre y suelte sus PDFs de AutoCAD / Civil 3D aquí'}
            </p>
            <p className="mt-1 text-sm text-slate-400">
              o <span className="text-accent-cyan underline font-medium">examine sus archivos</span> (soporta conversión individual y por lotes)
            </p>
          </div>

          <div className="flex items-center space-x-3 text-xs text-slate-400 bg-slate-900/80 px-4 py-2 rounded-full border border-slate-800">
            <span>Solo PDF Vectorial (AutoCAD, Civil 3D, Revit, SolidWorks)</span>
            <span>•</span>
            <span>Hasta 100 MB</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
