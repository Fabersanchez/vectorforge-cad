export type DXFVersion = "R12" | "R14" | "2000" | "2004" | "2007" | "2010" | "2013" | "2018";

export interface ConversionOptions {
  dxf_version: DXFVersion;
  snap_tolerance: float;
  remove_duplicates: boolean;
  join_segments: boolean;
  extract_text: boolean;
}

export type float = number;

export interface EntityCounts {
  lines: number;
  polylines: number;
  arcs: number;
  circles: number;
  ellipses: number;
  splines: number;
  texts: number;
  total: number;
}

export interface OptimizationStats {
  original_counts: EntityCounts;
  optimized_counts: EntityCounts;
  optimization_percentage: number;
  execution_time_seconds: number;
  original_file_size_bytes: number;
  output_file_size_bytes: number;
}

export interface ConversionJob {
  job_id: string;
  filename: string;
  file?: File;
  status: "pending" | "processing" | "completed" | "failed";
  progress: number;
  dxf_download_url?: string;
  stats?: OptimizationStats;
  error?: string;
  created_at: string;
}

export interface HistoryItem {
  job_id: string;
  original_name: string;
  dxf_name: string;
  status: string;
  dxf_version: string;
  stats?: OptimizationStats;
  created_at: string;
}

export interface PreviewData {
  job_id: string;
  filename: string;
  pdf_image: string;
  svg_vector: string;
}
