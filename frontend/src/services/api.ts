import axios from 'axios';
import { ConversionJob, ConversionOptions, HistoryItem, PreviewData } from '../types/conversion';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  uploadFiles: async (files: File[]): Promise<ConversionJob[]> => {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));

    const response = await apiClient.post<ConversionJob[]>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  triggerConvert: async (jobIds: string[], options: ConversionOptions): Promise<void> => {
    await apiClient.post('/convert', {
      job_ids: jobIds,
      options: options,
    });
  },

  getJobStatus: async (jobId: string): Promise<ConversionJob> => {
    const response = await apiClient.get<ConversionJob>(`/status/${jobId}`);
    return response.data;
  },

  getJobPreview: async (jobId: string): Promise<PreviewData> => {
    const response = await apiClient.get<PreviewData>(`/preview/${jobId}`);
    return response.data;
  },

  getDownloadUrl: (jobId: string): string => {
    return `${API_BASE_URL}/download/${jobId}`;
  },

  batchDownload: async (jobIds: string[]): Promise<Blob> => {
    const response = await apiClient.post(
      '/batch-download',
      { job_ids: jobIds },
      {
        responseType: 'blob',
      }
    );
    return response.data;
  },

  getHistory: async (): Promise<HistoryItem[]> => {
    const response = await apiClient.get<HistoryItem[]>('/history');
    return response.data;
  },

  clearHistory: async (): Promise<void> => {
    await apiClient.delete('/history');
  },
};
