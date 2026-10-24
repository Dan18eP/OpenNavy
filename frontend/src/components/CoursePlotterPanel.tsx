import React, { useState, useRef } from 'react';
import {
  Compass,
  Navigation,
  MapPin,
  AlertTriangle,
  FileCode,
  Image as ImageIcon,
  UploadCloud,
  Trash2,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  Sparkles,
  ShieldAlert,
  ListChecks,
  GitPullRequest,
  Loader2,
  ExternalLink,
  RotateCcw
} from 'lucide-react';
import { api, CoursePlotResult, WaypointItem } from '../services/api';
import { AiMessageRenderer } from './AiMessageRenderer';

interface CoursePlotterPanelProps {
  repoId: string | null;
  repoName: string;
  onSelectWaypoint: (file: string, lines?: [number, number]) => void;
}

export const CoursePlotterPanel: React.FC<CoursePlotterPanelProps> = ({
  repoId,
  repoName,
  onSelectWaypoint,
}) => {
  const [mission, setMission] = useState<string>('');
  const [issueUrl, setIssueUrl] = useState<string>('');
  const [officerName, setOfficerName] = useState<string>('Brandon Carranza');
  const [imageBase64, setImageBase64] = useState<string | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isPlotting, setIsPlotting] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Result state
  const [result, setResult] = useState<CoursePlotResult | null>(null);
  const [isThoughtExpanded, setIsThoughtExpanded] = useState<boolean>(true);
  const [isPrExpanded, setIsPrExpanded] = useState<boolean>(false);
  const [copiedPr, setCopiedPr] = useState<boolean>(false);
  const [activeWaypointIndex, setActiveWaypointIndex] = useState<number | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = (file: File) => {
    if (!file.type.startsWith('image/')) {
      setErrorMsg('El archivo debe ser una imagen (PNG, JPG, WebP).');
      return;
    }
    setErrorMsg(null);
    const reader = new FileReader();
    reader.onload = (e) => {
      const dataUrl = e.target?.result as string;
      setImagePreview(dataUrl);
      // Extraer Base64 puro para enviar al endpoint
      const base64Data = dataUrl.includes(',') ? dataUrl.split(',')[1] : dataUrl;
      setImageBase64(base64Data);
    };
    reader.readAsDataURL(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageUpload(e.dataTransfer.files[0]);
    }
  };

  const handleRemoveImage = () => {
    setImageBase64(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handlePlotCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!repoId) {
      setErrorMsg('Selecciona un repositorio antes de trazar rumbo.');
      return;
    }

    const promptText = [
      issueUrl.trim() ? `Issue URL: ${issueUrl.trim()}` : '',
      mission.trim(),
    ].filter(Boolean).join('\n\n');

    if (!promptText && !imageBase64) {
      setErrorMsg('Ingresa una descripción del issue o adjunta una captura de error.');
      return;
    }

    setIsPlotting(true);
    setErrorMsg(null);

    try {
      const res = await api.plotCourse({
        repo_id: repoId,
        mission: promptText || 'Análisis de captura visual de error.',
        image_base64: imageBase64 || undefined,
        officer_name: officerName || 'Brandon Carranza',
      });
      setResult(res);
      setIsThoughtExpanded(true);
    } catch (err: any) {
      console.error('Error trazando rumbo:', err);
      setErrorMsg(err.message || 'Error al conectar con el Almirante Gemma 4.');
    } finally {
      setIsPlotting(false);
    }
  };

  const handleCopyPrTemplate = async () => {
    if (!result?.pr_template) return;
    try {
      await navigator.clipboard.writeText(result.pr_template);
      setCopiedPr(true);
      setTimeout(() => setCopiedPr(false), 2000);
    } catch (e) {
      console.error('Error al copiar al portapapeles', e);
    }
  };

  const handleWaypointClick = (wp: WaypointItem, index: number) => {
    setActiveWaypointIndex(index);
    const start = Array.isArray(wp.lines) && wp.lines.length > 0 ? wp.lines[0] : 1;
    const end = Array.isArray(wp.lines) && wp.lines.length > 1 ? wp.lines[1] : start;
    onSelectWaypoint(wp.file, [start, end]);
  };

  const handleResetCourse = () => {
    setResult(null);
    setMission('');
    setIssueUrl('');
    handleRemoveImage();
    setActiveWaypointIndex(null);
  };

  return (
    <div className="w-full h-full flex flex-col min-h-0 bg-surface/30 select-text">
      {/* Header */}
      <div className="p-3.5 border-b border-border-subtle bg-surface/80 flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-2">
          <Compass className="size-4 text-brand animate-pulse" />
          <h2 className="font-sans text-sm font-bold text-text">El Trazador de Rumbo (Course Plotter)</h2>
        </div>
        <div className="flex items-center gap-1.5 font-mono text-[10px] px-2 py-0.5 border border-[#003893]/30 bg-[#003893]/10 text-[#003893] font-semibold">
          <Sparkles className="size-3" />
          <span>Gemma 4 Multimodal</span>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto scroll-accent p-4 space-y-4">
        {errorMsg && (
          <div className="p-3 border border-red-200 bg-red-50 text-red-700 text-xs flex items-center gap-2 font-mono">
            <AlertTriangle className="size-4 flex-shrink-0 text-red-600" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Course Form View (when no result yet or plotting) */}
        {!result ? (
          <form onSubmit={handlePlotCourse} className="space-y-4">
            <div className="space-y-1.5">
              <label className="block font-mono text-[11px] text-text-muted">
                Oficial al Mando:
              </label>
              <input
                type="text"
                value={officerName}
                onChange={(e) => setOfficerName(e.target.value)}
                placeholder="Nombre del oficial"
                className="w-full px-3 py-1.5 border border-border-subtle bg-surface text-text font-mono text-xs focus:border-brand focus:outline-none"
              />
            </div>

            <div className="space-y-1.5">
              <label className="block font-mono text-[11px] text-text-muted">
                Enlace de Issue / Requerimiento (Opcional):
              </label>
              <input
                type="url"
                value={issueUrl}
                onChange={(e) => setIssueUrl(e.target.value)}
                placeholder="https://github.com/org/repo/issues/42"
                className="w-full px-3 py-1.5 border border-border-subtle bg-surface text-text font-mono text-xs focus:border-brand focus:outline-none"
              />
            </div>

            <div className="space-y-1.5">
              <label className="block font-mono text-[11px] text-text-muted">
                Misión o Descripción del Error:
              </label>
              <textarea
                value={mission}
                onChange={(e) => setMission(e.target.value)}
                placeholder="Describe el bug, bounty o funcionalidad. Ej: Al expirar el token JWT no se renueva la sesión y el socket lanza desconexión no controlada."
                rows={4}
                className="w-full px-3 py-2 border border-border-subtle bg-surface text-text font-sans text-xs focus:border-brand focus:outline-none resize-none"
              />
            </div>

            {/* Multimodal Drag & Drop Area */}
            <div className="space-y-1.5">
              <label className="block font-mono text-[11px] text-text-muted">
                Artefacto Visual (Captura de pantalla de bug o excepción de terminal):
              </label>

              {!imagePreview ? (
                <div
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className="border border-dashed border-border-strong hover:border-brand/70 bg-surface/50 p-4 flex flex-col items-center justify-center gap-2 cursor-pointer transition-colors text-center"
                >
                  <UploadCloud className="size-6 text-brand/80" />
                  <div className="font-mono text-xs text-text">
                    Arrastra una imagen o haz clic para subir
                  </div>
                  <div className="font-mono text-[10px] text-text-muted">
                    Soporta capturas de UI bugs, diagramas o stack traces (Gemma 4 Visión)
                  </div>
                </div>
              ) : (
                <div className="relative border border-brand/40 bg-surface p-2 flex items-center justify-between">
                  <div className="flex items-center gap-2.5 overflow-hidden">
                    <img
                      src={imagePreview}
                      alt="Captura adjunta"
                      className="size-12 object-cover border border-border-subtle flex-shrink-0"
                    />
                    <div className="overflow-hidden">
                      <div className="font-mono text-xs text-text truncate">Captura adjunta</div>
                      <div className="font-mono text-[10px] text-brand">Lista para inferencia multimodal</div>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={handleRemoveImage}
                    className="p-1 text-text-muted hover:text-red-400 transition-colors"
                    title="Eliminar imagen"
                  >
                    <Trash2 className="size-4" />
                  </button>
                </div>
              )}

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={(e) => e.target.files?.[0] && handleImageUpload(e.target.files[0])}
                className="hidden"
              />
            </div>

            <button
              type="submit"
              disabled={isPlotting || !repoId}
              className="w-full py-2.5 px-4 bg-[#003893] text-white font-mono font-semibold text-xs flex items-center justify-center gap-2 hover:bg-[#002d75] transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer shadow-sm"
            >
              {isPlotting ? (
                <>
                  <Loader2 className="size-4 animate-spin" />
                  <span>El Almirante Gemma 4 está trazando rumbo...</span>
                </>
              ) : (
                <>
                  <Navigation className="size-4" />
                  <span>Trazar Rumbo con Google Gemma 4</span>
                </>
              )}
            </button>
          </form>
        ) : (
          /* Results View */
          <div className="space-y-4">
            {/* Mission Header */}
            <div className="p-3 border border-border-subtle bg-surface flex items-start justify-between gap-3 shadow-xs">
              <div>
                <div className="font-mono text-[10px] text-text-muted">Plan de Vuelo Náutico:</div>
                <div className="font-sans text-xs font-semibold text-text mt-0.5 line-clamp-2">
                  {result.mission}
                </div>
              </div>
              <button
                type="button"
                onClick={handleResetCourse}
                className="inline-flex items-center gap-1 font-mono text-[10px] px-2.5 py-1 border border-border-subtle bg-surface-2 hover:bg-surface text-text hover:text-[#003893] transition-colors flex-shrink-0 cursor-pointer"
                title="Trazar otro rumbo"
              >
                <RotateCcw className="size-3 text-[#003893]" />
                <span>Nuevo Rumbo</span>
              </button>
            </div>

            {/* Gemma 4 Thought Process Accordion */}
            {result.thought_process && (
              <div className="border border-[#003893]/30 bg-surface overflow-hidden shadow-xs">
                <button
                  type="button"
                  onClick={() => setIsThoughtExpanded(!isThoughtExpanded)}
                  className="w-full p-2.5 bg-[#003893]/10 border-b border-[#003893]/20 flex items-center justify-between text-left text-xs font-mono text-[#003893] font-semibold cursor-pointer"
                >
                  <div className="flex items-center gap-2">
                    <Sparkles className="size-3.5 text-[#003893]" />
                    <span>Flujo de Razonamiento del Almirante (&lt;|think|&gt;)</span>
                  </div>
                  {isThoughtExpanded ? (
                    <ChevronUp className="size-3.5" />
                  ) : (
                    <ChevronDown className="size-3.5" />
                  )}
                </button>
                {isThoughtExpanded && (
                  <div className="p-3.5 text-xs font-mono leading-relaxed text-text bg-surface/90 border-t border-border-subtle max-h-56 overflow-y-auto scroll-accent">
                    <AiMessageRenderer
                      content={result.thought_process}
                      onOpenFile={(file, range) => onSelectWaypoint(file, range)}
                    />
                  </div>
                )}
              </div>
            )}

            {/* Waypoints List */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <MapPin className="size-4 text-[#003893]" />
                  <h3 className="font-sans text-xs font-bold text-text uppercase tracking-wider">
                    Waypoints (Coordenadas Exactas)
                  </h3>
                </div>
                <span className="font-mono text-[10px] px-2 py-0.5 border border-[#003893]/30 bg-[#003893]/10 text-[#003893] font-bold">
                  {result.waypoints.length} puntos
                </span>
              </div>

              <div className="space-y-2">
                {result.waypoints.map((wp, idx) => {
                  const startLine = Array.isArray(wp.lines) && wp.lines.length > 0 ? wp.lines[0] : 1;
                  const endLine = Array.isArray(wp.lines) && wp.lines.length > 1 ? wp.lines[1] : startLine;
                  const isSelected = activeWaypointIndex === idx;

                  return (
                    <div
                      key={idx}
                      onClick={() => handleWaypointClick(wp, idx)}
                      className={`p-2.5 border cursor-pointer transition-all ${
                        isSelected
                          ? 'border-[#003893] bg-[#003893]/10 shadow-sm'
                          : 'border-border-subtle bg-surface hover:border-[#003893]/50 hover:bg-surface-2'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-1.5 font-mono text-xs font-semibold text-text truncate">
                          <FileCode className="size-3.5 text-[#003893] flex-shrink-0" />
                          <span className="truncate">{wp.file}</span>
                        </div>
                        <span className="font-mono text-[10px] px-1.5 py-0.5 border border-[#003893]/30 bg-surface-2 text-[#003893] font-bold flex-shrink-0">
                          L{startLine}-{endLine}
                        </span>
                      </div>
                      <div className="mt-1 text-[11px] text-text-muted leading-relaxed">
                        {wp.reason}
                      </div>
                      <div className="mt-2 flex items-center justify-end font-mono text-[10px] text-[#003893] gap-1 font-semibold">
                        <span>Ver en AST split-view</span>
                        <ExternalLink className="size-3" />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Reef Warnings (Tarjan SCC Cyclic Alerts) */}
            {result.reef_warnings && result.reef_warnings.length > 0 && (
              <div className="p-3 border border-amber-300 bg-amber-50 space-y-2">
                <div className="flex items-center gap-2 text-amber-800 font-sans text-xs font-bold uppercase tracking-wider">
                  <ShieldAlert className="size-4 text-amber-600 animate-pulse flex-shrink-0" />
                  <span>Arrecifes Topológicos (Acoplamiento Crítico)</span>
                </div>
                <div className="space-y-1 font-mono text-[11px] text-amber-900 leading-relaxed">
                  {result.reef_warnings.map((warn, wIdx) => (
                    <div key={wIdx} className="flex items-start gap-1.5">
                      <span className="text-amber-600 font-bold">•</span>
                      <span>{warn}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Action Steps */}
            {result.action_steps && result.action_steps.length > 0 && (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <ListChecks className="size-4 text-[#003893]" />
                  <h3 className="font-sans text-xs font-bold text-text uppercase tracking-wider">
                    Plan de Implementación Paso a Paso
                  </h3>
                </div>
                <div className="space-y-1.5">
                  {result.action_steps.map((step, sIdx) => (
                    <div
                      key={sIdx}
                      className="p-2 border border-border-subtle bg-surface text-xs font-mono flex items-start gap-2"
                    >
                      <span className="px-1.5 py-0.5 border border-[#003893]/30 bg-[#003893]/10 text-[#003893] font-bold text-[10px] flex-shrink-0">
                        {sIdx + 1}
                      </span>
                      <span className="text-text leading-relaxed">{step}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Pull Request & Commit Draft Template */}
            {result.pr_template && (
              <div className="border border-border-subtle bg-surface overflow-hidden shadow-xs">
                <div className="p-2.5 bg-surface-2 border-b border-border-subtle flex items-center justify-between">
                  <button
                    type="button"
                    onClick={() => setIsPrExpanded(!isPrExpanded)}
                    className="flex items-center gap-2 text-xs font-mono font-semibold text-text cursor-pointer"
                  >
                    <GitPullRequest className="size-3.5 text-[#003893]" />
                    <span>Borrador de Pull Request (Conventional Commit)</span>
                    {isPrExpanded ? <ChevronUp className="size-3" /> : <ChevronDown className="size-3" />}
                  </button>

                  <button
                    type="button"
                    onClick={handleCopyPrTemplate}
                    className="inline-flex items-center gap-1 font-mono text-[10px] px-2.5 py-1 border border-[#003893]/30 bg-[#003893]/10 text-[#003893] hover:bg-[#003893] hover:text-white transition-colors cursor-pointer font-semibold"
                  >
                    {copiedPr ? (
                      <>
                        <Check className="size-3 text-emerald-600" />
                        <span className="text-emerald-700">Copiado</span>
                      </>
                    ) : (
                      <>
                        <Copy className="size-3 text-[#003893]" />
                        <span>Copiar PR</span>
                      </>
                    )}
                  </button>
                </div>

                {isPrExpanded && (
                  <div className="p-3 bg-surface-2 text-[11px] font-mono leading-relaxed whitespace-pre-wrap text-text max-h-48 overflow-y-auto scroll-accent border-t border-border-subtle">
                    {result.pr_template}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
