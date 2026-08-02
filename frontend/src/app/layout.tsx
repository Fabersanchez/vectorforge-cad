import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CADVector Pro — Plataforma de Conversión PDF Vectorial a DXF",
  description: "Plataforma web profesional para convertir archivos PDF vectoriales de AutoCAD, Civil 3D, Revit, SolidWorks e Inventor a formato DXF con alta precisión geométrica.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className="dark">
      <body className="bg-background text-slate-100 antialiased selection:bg-accent-cyan selection:text-black">
        {children}
      </body>
    </html>
  );
}
