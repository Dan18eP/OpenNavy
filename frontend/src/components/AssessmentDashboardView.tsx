import React, { useState, useEffect } from 'react';
import { 
  FileSpreadsheet, 
  Upload, 
  Cpu, 
  FileCheck,
  ShieldAlert,
  Compass
} from 'lucide-react';
import { api } from '../services/api';

export const AssessmentDashboardView: React.FC = () => {
  const [assessmentData, setAssessmentData] = useState<any>({
    proyecto: 'Asistente de Triage Inteligente',
    equipo: 'Tripulación de Ingeniería OpenNavy',
    problema: 'Los tickets y revisiones de código se procesan manualmente generando retrasos.',
    situacion: 'Proceso manual no estandarizado con ~15 minutos por revisión.',
    resultado: 'Clasificar y emitir veredicto de arquitectura y calidad automáticamente.',
    dimension: 'Tiempo',
    metrica: 'Tiempo por auditoría y % de detección de antipatrones',
    meta: 'Reducir de 15 a 3 minutos con 95% de precisión',
    cap_reglas: 'Sí',
    cap_prediccion: 'Sí',
    cap_comprension: 'Sí',
    cap_generacion: 'Sí',
    cap_consulta: 'Sí',
    cap_accion: 'No',
    cap_autonomia: 'No',
    suficiencia: 'No',
    solucion_simple: 'Reglas fijas por palabra clave (no interpretan semántica ni contexto)',
    info_necesaria: 'Repositorios Git, base de conocimiento RAG y rúbricas de estándares',
    info_existe: 'Sí',
    info_accesible: 'Sí',
    info_confiable: 'Sí',
    info_sensible: 'Sí',
    autonomia_nivel: 'Recomienda',
    riesgo_desc: 'Calificar erróneamente un antipatrón o filtrar un secreto a la API',
    riesgo_nivel: 'Medio',
    hipotesis: 'Este problema requiere comprensión y generación para interpretar código y sugerir refactors donde las reglas estáticas no bastan.'
  });

  const [verdict, setVerdict] = useState<any>(null);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);

  useEffect(() => {
    runEvaluation(assessmentData);
  }, []);

  const runEvaluation = async (data: any) => {
    try {
      const res = await api.evaluateAssessment(data);
      setVerdict(res);
    } catch (e) {
      console.error(e);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploadMessage('Procesando archivo Excel...');
    try {
      const res = await api.uploadAssessmentExcel(file);
      setVerdict(res);
      if (res.raw_data) {
        setAssessmentData(res.raw_data);
      }
      setUploadMessage(`[OK] Archivo «${file.name}» cargado y evaluado con éxito.`);
    } catch (err: any) {
      setUploadMessage(`[FALLO] Error: ${err.message || 'No se pudo leer el archivo Excel'}`);
    }
  };

  const capList = [
    { key: 'cap_reglas', label: 'Reglas', desc: 'Decisiones determinísticas conocidas', isAi: false },
    { key: 'cap_prediccion', label: 'Predicción', desc: 'Clasificar, estimar o detectar patrones', isAi: true },
    { key: 'cap_comprension', label: 'Comprensión', desc: 'Interpretar información no estructurada', isAi: true },
    { key: 'cap_generacion', label: 'Generación', desc: 'Producir respuestas o contenido nuevo', isAi: true },
    { key: 'cap_consulta', label: 'Consulta', desc: 'Consultar fuentes y sistemas externos', isAi: false },
    { key: 'cap_accion', label: 'Acción', desc: 'Ejecutar modificaciones sobre otros sistemas', isAi: false },
    { key: 'cap_autonomia', label: 'Autonomía', desc: 'Coordinar pasos hacia un objetivo abierto', isAi: false },
  ];

  const getVerdictStyle = (key: string) => {
    switch (key) {
      case 'op':
        return {
          border: 'border-emerald-500/40',
          bg: 'bg-emerald-50/70',
          badgeBg: 'bg-emerald-100 text-emerald-800 border-emerald-400 font-bold',
          dot: 'bg-emerald-600',
        };
      case 'auto':
        return {
          border: 'border-amber-500/40',
          bg: 'bg-amber-50/70',
          badgeBg: 'bg-amber-100 text-amber-800 border-amber-400 font-bold',
          dot: 'bg-amber-600',
        };
      default:
        return {
          border: 'border-[#003893]/40',
          bg: 'bg-surface',
          badgeBg: 'bg-[#003893]/10 text-[#003893] border-[#003893]/40 font-bold',
          dot: 'bg-[#003893]',
        };
    }
  };

  const vStyle = getVerdictStyle(verdict?.key || 'val');

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header Banner */}
      <div className="p-6 border border-border-subtle bg-surface/90 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-[#003893] mb-1">
            <Compass className="w-4 h-4 text-[#003893]" /> Sesión 01 · Secure AI Engineering Series
          </div>
          <h2 className="text-xl font-bold font-sans tracking-tight text-text">
            AI Opportunity Assessment
          </h2>
          <p className="text-xs font-mono text-text-muted mt-1 max-w-2xl">
            Evalúa estructuradamente por capacidades si una necesidad de software justifica un modelo de IA o si basta una automatización convencional por reglas.
          </p>
        </div>

        {/* Upload Excel Button */}
        <div>
          <label className="flex items-center gap-2 px-4 py-2 border border-[#003893] bg-[#003893] hover:bg-[#002d75] text-white font-mono text-xs cursor-pointer transition-colors shadow-sm">
            <Upload className="w-4 h-4" />
            <span>Cargar Levantamiento (.xlsx)</span>
            <input type="file" accept=".xlsx,.xlsm" className="hidden" onChange={handleFileUpload} />
          </label>
        </div>
      </div>

      {uploadMessage && (
        <div className="p-3 px-4 text-xs font-mono border border-border-subtle bg-surface-2 text-text flex items-center gap-2">
          <FileSpreadsheet className="w-4 h-4 text-brand" />
          {uploadMessage}
        </div>
      )}

      {/* Grid: Veredicto Principal y Matriz de Capacidades */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Columna Izquierda: Veredicto y Racional (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          {/* Tarjeta de Veredicto */}
          <div className={`p-6 border ${vStyle.border} ${vStyle.bg} relative overflow-hidden space-y-4`}>
            <div className="flex justify-between items-start gap-3">
              <span className={`inline-flex items-center gap-2 px-3 py-1 text-xs font-mono font-semibold border ${vStyle.badgeBg}`}>
                <span className={`w-2 h-2 rounded-full ${vStyle.dot} animate-pulse`} />
                {verdict?.title || 'EVALUANDO...'}
              </span>
              <Cpu className="w-5 h-5 text-text-muted" />
            </div>

            <h3 className="text-lg font-bold text-text font-sans tracking-tight">
              {assessmentData.proyecto || 'Proyecto'}
            </h3>
            <p className="text-xs font-sans text-text-secondary leading-relaxed">
              {verdict?.lead}
            </p>
            {verdict?.detail && (
              <p className="text-xs font-mono text-text-muted border-t border-border-subtle pt-3">
                {verdict.detail}
              </p>
            )}

            {/* Razonamiento del algoritmo */}
            <div className="pt-3 border-t border-border-subtle">
              <h4 className="text-xs font-mono uppercase tracking-wider text-text-muted mb-2">
                Cómo se llegó a esta conclusión:
              </h4>
              <div className="space-y-2">
                {verdict?.why?.map((w: string, i: number) => (
                  <div key={i} className="flex items-start gap-2 text-xs text-text-secondary font-sans">
                    <span className="w-4 h-4 border border-border-subtle bg-surface-2 flex items-center justify-center text-[10px] text-text font-mono flex-shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Autonomía y Riesgos */}
          <div className="p-6 border border-border-subtle bg-surface/90 space-y-4">
            <h4 className="text-xs font-mono uppercase tracking-widest text-[#003893] flex items-center gap-2 font-bold">
              <ShieldAlert className="w-4 h-4" /> Nivel de Autonomía y Exposición
            </h4>
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 border border-border-subtle bg-bg-deep/80">
                <span className="text-[10px] text-text-muted block font-mono">Autonomía</span>
                <span className="text-sm font-bold text-text font-mono">{assessmentData.autonomia_nivel || 'Recomienda'}</span>
              </div>
              <div className="p-3 border border-border-subtle bg-bg-deep/80">
                <span className="text-[10px] text-text-muted block font-mono">Riesgo Inicial</span>
                <span className="text-sm font-bold text-amber-700 font-mono">{assessmentData.riesgo_nivel || 'Medio'}</span>
              </div>
            </div>
            <p className="text-xs font-sans text-text leading-relaxed">
              {assessmentData.riesgo_desc || 'No se registraron riesgos adicionales.'}
            </p>
          </div>
        </div>

        {/* Columna Derecha: Matriz de 7 Capacidades y Datos (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          <div className="p-6 border border-border-subtle bg-surface/90 space-y-4">
            <div className="flex justify-between items-center pb-3 border-b border-border-subtle">
              <h4 className="text-xs font-mono uppercase tracking-widest text-[#003893] flex items-center gap-2 font-bold">
                <FileCheck className="w-4 h-4" /> Perfil de las 7 Capacidades
              </h4>
              <span className="text-xs text-text-muted font-mono">Sesión 01 · Paso 2</span>
            </div>

            <div className="space-y-2">
              {capList.map((cap) => {
                const val = assessmentData[cap.key] || 'Por validar';
                const isSi = val === 'Sí';
                const isNo = val === 'No';
                return (
                  <div key={cap.key} className="p-3 px-4 border border-border-subtle bg-surface-2/40 flex items-center justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono font-bold text-text">{cap.label}</span>
                        {cap.isAi && (
                          <span className="text-[10px] px-1.5 py-0.5 border border-brand/40 bg-brand-soft text-brand font-mono">
                            Inteligencia
                          </span>
                        )}
                      </div>
                      <span className="text-xs font-sans text-text-muted">{cap.desc}</span>
                    </div>

                    <div className="flex items-center gap-1 font-mono text-xs">
                      <button
                        type="button"
                        onClick={() => {
                          const updated = { ...assessmentData, [cap.key]: 'Sí' };
                          setAssessmentData(updated);
                          runEvaluation(updated);
                        }}
                        className={`px-2.5 py-0.5 border transition-colors cursor-pointer ${
                          isSi
                            ? 'bg-emerald-100 border-emerald-500 text-emerald-800 font-bold'
                            : 'bg-transparent border-border-subtle text-text-muted hover:text-text'
                        }`}
                      >
                        Sí
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          const updated = { ...assessmentData, [cap.key]: 'No' };
                          setAssessmentData(updated);
                          runEvaluation(updated);
                        }}
                        className={`px-2.5 py-0.5 border transition-colors cursor-pointer ${
                          isNo
                            ? 'bg-red-100 border-red-500 text-red-800 font-bold'
                            : 'bg-transparent border-border-subtle text-text-muted hover:text-text'
                        }`}
                      >
                        No
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          const updated = { ...assessmentData, [cap.key]: 'Por validar' };
                          setAssessmentData(updated);
                          runEvaluation(updated);
                        }}
                        className={`px-2.5 py-0.5 border transition-colors cursor-pointer ${
                          !isSi && !isNo
                            ? 'bg-amber-100 border-amber-500 text-amber-800 font-bold'
                            : 'bg-transparent border-border-subtle text-text-muted hover:text-text'
                        }`}
                      >
                        ?
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Suficiencia de Solución Simple */}
            <div className="p-4 border border-border-subtle bg-bg-deep/80 mt-4 space-y-1">
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs font-mono font-bold text-text">¿Una solución más simple es suficiente?</span>
                <span className="text-xs font-mono font-bold text-brand">{assessmentData.suficiencia || 'No'}</span>
              </div>
              <p className="text-xs font-sans text-text-muted">
                Solución simple considerada: {assessmentData.solucion_simple || '—'}
              </p>
            </div>
          </div>

          {/* Información y Datos Requeridos */}
          <div className="p-6 border border-border-subtle bg-surface/90 space-y-3">
            <h4 className="text-xs font-mono uppercase tracking-widest text-brand">
              Paso 4 · Información Necesaria
            </h4>
            <p className="text-xs font-sans text-text-secondary">{assessmentData.info_necesaria}</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pt-2">
              {[
                { label: 'Existe', val: assessmentData.info_existe },
                { label: 'Accesible', val: assessmentData.info_accesible },
                { label: 'Confiable', val: assessmentData.info_confiable },
                { label: 'Sensible', val: assessmentData.info_sensible },
              ].map((p, idx) => (
                <div key={idx} className="p-2.5 border border-border-subtle bg-bg-deep/80 text-center">
                  <span className="text-[10px] text-text-muted block font-mono">{p.label}</span>
                  <span
                    className={`text-xs font-mono font-bold ${
                      p.val === 'Sí' ? 'text-emerald-400' : p.val === 'No' ? 'text-rose-400' : 'text-amber-400'
                    }`}
                  >
                    {p.val || 'Por validar'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
