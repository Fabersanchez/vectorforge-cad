import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, AlertTriangle, Info, X } from 'lucide-react';

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'info';
  title: string;
  description?: string;
}

interface ToastProps {
  toasts: ToastMessage[];
  onDismiss: (id: string) => void;
}

export function ToastContainer({ toasts, onDismiss }: ToastProps) {
  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col space-y-3 max-w-sm w-full pointer-events-none">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="pointer-events-auto bg-slate-900 border border-slate-700 rounded-2xl p-4 shadow-2xl flex items-start space-x-3 backdrop-blur-xl"
          >
            {toast.type === 'success' && <CheckCircle2 className="w-5 h-5 text-accent-emerald flex-shrink-0 mt-0.5" />}
            {toast.type === 'error' && <AlertTriangle className="w-5 h-5 text-rose-500 flex-shrink-0 mt-0.5" />}
            {toast.type === 'info' && <Info className="w-5 h-5 text-accent-cyan flex-shrink-0 mt-0.5" />}

            <div className="flex-1">
              <h4 className="text-xs font-bold text-white">{toast.title}</h4>
              {toast.description && (
                <p className="text-[11px] text-slate-400 mt-0.5">
                  {typeof toast.description === 'string' ? toast.description : JSON.stringify(toast.description)}
                </p>
              )}
            </div>

            <button
              type="button"
              aria-label="Cerrar notificación"
              onClick={(e: React.MouseEvent<HTMLButtonElement>) => {
                e.stopPropagation();
                onDismiss(toast.id);
              }}
              className="text-slate-500 hover:text-slate-300 p-1"
            >
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
