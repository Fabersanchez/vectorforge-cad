"use client";

import React, { useState, useEffect } from 'react';
import { Header } from '../components/Header';
import { Dropzone } from '../components/Dropzone';
import { ConfigPanel } from '../components/ConfigPanel';
import { FileCard } from '../components/FileCard';
import { PreviewModal } from '../components/PreviewModal';
import { StatsCard } from '../components/StatsCard';
import { HistoryTable } from '../components/HistoryTable';
import { ToastContainer, ToastMessage } from '../components/Toast';
import { ConversionJob, ConversionOptions, HistoryItem, PreviewData } from '../types/conversion';
import { api } from '../services/api';
import { Play, Download, RefreshCw, Sparkles, Layers } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Dashboard() {
  const [jobs, setJobs] = useState<ConversionJob[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [previewData, setPreviewData] = useState<PreviewData | null>(null);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const [isProcessingBatch, setIsProcessingBatch] = useState(false);

  const [options, setOptions] = useState<ConversionOptions>({
    dxf_version: "2018",
    snap_tolerance: 0.0001,
    remove_duplicates: true,
    join_segments: true,
    extract_text: true,
  });

  const addToast = (type: 'success' | 'error' | 'info', title: string, description?: any) => {
    let descString: string | undefined = undefined;
    if (description) {
      if (typeof description === 'string') {
        descString = description;
      } else if (Array.isArray(description)) {
        descString = description.map((d) => (typeof d === 'string' ? d : d?.msg || JSON.stringify(d))).join(', ');
      } else if (typeof description === 'object') {
        descString = description?.msg || JSON.stringify(description);
      } else {
        descString = String(description);
      }
    }

    const id = Math.random().toString(36).substring(7);
    setToasts((prev) => [...prev, { id, type, title, description: descString }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 5000);
  };

  const loadHistory = async () => {
    try {
      const data = await api.getHistory();
      setHistory(data);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleFilesSelected = async (files: File[]) => {
    try {
      const uploadedJobs = await api.uploadFiles(files);
      setJobs((prev) => [...uploadedJobs, ...prev]);
      addToast('info', 'Archivos Subidos', `${files.length} archivo(s) listo(s) para convertir.`);
    } catch (err: any) {
      addToast('error', 'Error de Carga', err?.response?.data?.detail || 'Falló la subida del archivo PDF.');
    }
  };

  const handleConvertAll = async () => {
    const pendingJobIds = jobs.filter((j) => j.status === 'pending' || j.status === 'failed').map((j) => j.job_id);
    if (pendingJobIds.length === 0) return;

    setIsProcessingBatch(true);
    addToast('info', 'Procesando Conversión', `Iniciando conversión DXF para ${pendingJobIds.length} archivo(s)...`);

    try {
      await api.triggerConvert(pendingJobIds, options);

      // Poll status for all jobs
      const interval = setInterval(async () => {
        let allFinished = true;
        const updatedJobs = await Promise.all(
          jobs.map(async (j) => {
            if (pendingJobIds.includes(j.job_id)) {
              try {
                const status = await api.getJobStatus(j.job_id);
                if (status.status === 'processing' || status.status === 'pending') {
                  allFinished = false;
                }
                return status;
              } catch {
                return j;
              }
            }
            return j;
          })
        );

        setJobs(updatedJobs);

        if (allFinished) {
          clearInterval(interval);
          setIsProcessingBatch(false);
          loadHistory();
          addToast('success', 'Conversión Finalizada', 'Todos los archivos DXF se han generado exitosamente.');
        }
      }, 1500);
    } catch (err: any) {
      setIsProcessingBatch(false);
      addToast('error', 'Error de Conversión', err?.response?.data?.detail || 'Error al procesar archivos.');
    }
  };

  const handleDownload = (jobId: string) => {
    const url = api.getDownloadUrl(jobId);
    window.open(url, '_blank');
  };

  const handleBatchDownloadZip = async () => {
    const completedIds = jobs.filter((j) => j.status === 'completed').map((j) => j.job_id);
    if (completedIds.length === 0) return;

    try {
      const blob = await api.batchDownload(completedIds);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `lote_dxf_${Date.now()}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      addToast('success', 'Descarga ZIP Iniciada', 'Archivo comprimido con todos los DXF generado.');
    } catch (err) {
      addToast('error', 'Error de Descarga', 'No se pudo generar el archivo ZIP del lote.');
    }
  };

  const handlePreview = async (jobId: string) => {
    try {
      const data = await api.getJobPreview(jobId);
      setPreviewData(data);
    } catch (err) {
      addToast('error', 'Vista Previa No Disponible', 'No se pudo renderizar la geometría del archivo.');
    }
  };

  const handleClearHistory = async () => {
    try {
      await api.clearHistory();
      setHistory([]);
      addToast('info', 'Historial Limpiado', 'Se ha eliminado el registro de conversiones.');
    } catch (err) {
      addToast('error', 'Error', 'No se pudo limpiar el historial.');
    }
  };

  const completedStats = jobs.find((j) => j.status === 'completed')?.stats;

  return (
    <div className="min-h-screen bg-background text-slate-100 flex flex-col">
      <Header />

      {/* Main Content Workspace */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
        {/* Hero Banner */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-surface via-slate-900 to-surface border border-surface-border p-8 md:p-10 shadow-2xl">
          <div className="absolute -top-24 -right-24 w-96 h-96 bg-accent-cyan/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-accent-purple/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10 max-w-3xl space-y-4">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-accent-cyan/10 border border-accent-cyan/30 text-xs font-semibold text-accent-cyan">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Motor de Precisión CAD Vectorial</span>
            </div>
            <h1 className="text-3xl md:text-5xl font-black text-white tracking-tight leading-tight">
              Conversión de PDF Vectorial a <span className="bg-clip-text text-transparent bg-gradient-to-r from-accent-cyan via-accent-purple to-accent-pink">DXF Editable</span>
            </h1>
            <p className="text-slate-400 text-sm md:text-base leading-relaxed">
              Conserve el 100% de sus líneas, polígonos, arcos, círculos y textos exportados desde AutoCAD, Civil 3D, Revit, SolidWorks e Inventor sin pérdida de geometría.
            </p>
          </div>
        </div>

        {/* Dropzone Upload Section */}
        <section className="space-y-4">
          <Dropzone onFilesSelected={handleFilesSelected} disabled={isProcessingBatch} />
        </section>

        {/* Configuration Settings */}
        <section>
          <ConfigPanel options={options} onChange={setOptions} />
        </section>

        {/* File Cards & Action Controls */}
        {jobs.length > 0 && (
          <section className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-surface/60 border border-surface-border p-4 rounded-2xl">
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-xl bg-accent-cyan/20 text-accent-cyan">
                  <Layers className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-white">Cola de Conversión ({jobs.length})</h2>
                  <p className="text-xs text-slate-400">Administre y ejecute la conversión de sus archivos</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                {jobs.some((j) => j.status === 'completed') && (
                  <button
                    onClick={handleBatchDownloadZip}
                    className="flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white border border-slate-700 transition-all"
                  >
                    <Download className="w-4 h-4 text-accent-cyan" />
                    <span>Descargar ZIP de Lote</span>
                  </button>
                )}

                <button
                  onClick={handleConvertAll}
                  disabled={isProcessingBatch || !jobs.some((j) => j.status === 'pending' || j.status === 'failed')}
                  className="flex items-center space-x-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-accent-cyan to-accent-purple hover:from-cyan-400 hover:to-purple-500 text-xs font-bold text-black shadow-glow-cyan transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isProcessingBatch ? (
                    <RefreshCw className="w-4 h-4 animate-spin text-black" />
                  ) : (
                    <Play className="w-4 h-4 text-black fill-black" />
                  )}
                  <span>{isProcessingBatch ? 'Convertiendo...' : 'Convertir Todos a DXF'}</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {jobs.map((job) => (
                <FileCard
                  key={job.job_id}
                  job={job}
                  onPreview={handlePreview}
                  onDownload={handleDownload}
                />
              ))}
            </div>
          </section>
        )}

        {/* Geometry & Optimization Statistics */}
        {completedStats && (
          <section>
            <StatsCard stats={completedStats} />
          </section>
        )}

        {/* History Log */}
        <section>
          <HistoryTable history={history} onDownload={handleDownload} onClear={handleClearHistory} />
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-surface-border py-8 text-center text-xs text-slate-500">
        <p>© 2026 CADVector Pro Engine — Plataforma Institucional de Conversión Vectorial. Todos los derechos reservados.</p>
      </footer>

      {/* Preview Modal */}
      <PreviewModal previewData={previewData} onClose={() => setPreviewData(null)} />

      {/* Notifications */}
      <ToastContainer toasts={toasts} onDismiss={(id) => setToasts((prev) => prev.filter((t) => t.id !== id))} />
    </div>
  );
}
