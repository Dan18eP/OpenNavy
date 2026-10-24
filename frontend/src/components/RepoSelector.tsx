import React, { useState } from 'react';
import { GitBranch, Play, Search, FolderGit2, RefreshCw, Trash2, AlertTriangle, X } from 'lucide-react';
import { RepoItem } from '../services/api';

interface RepoSelectorProps {
  repos: RepoItem[];
  selectedRepoId: string | null;
  onSelectRepo: (repoId: string) => void;
  onTriggerAnalysis: (repoUrl: string, branch: string) => void;
  onDeleteRepo?: (repoId: string) => Promise<void>;
  isAnalyzing: boolean;
}

export const RepoSelector: React.FC<RepoSelectorProps> = ({
  repos,
  selectedRepoId,
  onSelectRepo,
  onTriggerAnalysis,
  onDeleteRepo,
  isAnalyzing,
}) => {
  const [repoType, setRepoType] = useState<'remote' | 'local'>('remote');
  const [url, setUrl] = useState('');
  const [branch, setBranch] = useState('main');
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const selectedRepo = repos.find((r) => r.id === selectedRepoId);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;
    onTriggerAnalysis(url.trim(), branch.trim() || 'main');
  };

  const handleConfirmDelete = async () => {
    if (!selectedRepoId || !onDeleteRepo) return;
    setIsDeleting(true);
    try {
      await onDeleteRepo(selectedRepoId);
      setIsDeleteModalOpen(false);
    } catch (err) {
      console.error('Error al eliminar repositorio', err);
      alert('Error al eliminar el repositorio.');
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <>
      <div className="border border-border-subtle bg-surface/90 p-5 space-y-4">
        {/* Header & Quick Select */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-border-subtle">
          <div>
            <h2 className="font-sans text-base font-bold tracking-tight text-text flex items-center gap-2">
              <FolderGit2 className="size-4 text-brand" />
              Repositorio de Código
            </h2>
            <p className="font-mono text-xs text-text-muted mt-0.5">
              Audita un repositorio remoto en Git o una carpeta local en tu equipo
            </p>
          </div>

          {repos.length > 0 && (
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs text-text-muted">Repo:</span>
              <select
                value={selectedRepoId || ''}
                onChange={(e) => onSelectRepo(e.target.value)}
                className="border border-border-subtle bg-bg-deep text-text font-mono text-xs px-3 py-1.5 focus:border-brand focus:outline-none"
              >
                {repos.map((r) => (
                  <option key={r.id} value={r.id} className="bg-surface text-text">
                    {r.name} ({r.last_global_score !== null && r.last_global_score !== undefined ? `${r.last_global_score}/100` : 'Sin score'})
                  </option>
                ))}
              </select>

              {onDeleteRepo && selectedRepo && (
                <button
                  type="button"
                  onClick={() => setIsDeleteModalOpen(true)}
                  title={`Eliminar repositorio ${selectedRepo.name}`}
                  className="border border-red-300 bg-red-50 hover:bg-red-100 text-red-700 font-mono text-xs px-3 py-1.5 flex items-center gap-1.5 transition-colors cursor-pointer"
                >
                  <Trash2 className="size-3.5" />
                  <span>Eliminar</span>
                </button>
              )}
            </div>
          )}
        </div>

        {/* Selector de Tipo de Repositorio: Remoto vs Local */}
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs text-text-muted">Origen:</span>
            <div className="inline-flex border border-border-subtle bg-bg-deep p-0.5">
              <button
                type="button"
                onClick={() => {
                  setRepoType('remote');
                  setUrl('');
                }}
                className={`font-mono text-xs px-3 py-1.5 transition-colors cursor-pointer ${
                  repoType === 'remote'
                    ? 'bg-[#003893] text-white font-bold'
                    : 'text-text-muted hover:text-text'
                }`}
              >
                Repositorio Remoto (Git)
              </button>
              <button
                type="button"
                onClick={() => {
                  setRepoType('local');
                  setUrl('.');
                }}
                className={`font-mono text-xs px-3 py-1.5 transition-colors cursor-pointer ${
                  repoType === 'local'
                    ? 'bg-[#003893] text-white font-bold'
                    : 'text-text-muted hover:text-text'
                }`}
              >
                Carpeta Local (Ruta)
              </button>
            </div>
          </div>

          {repoType === 'local' && (
            <button
              type="button"
              onClick={() => {
                setUrl('.');
                setBranch('develop');
              }}
              className="text-[11px] font-mono text-[#003893] hover:underline px-2 py-1 border border-[#003893]/30 bg-[#003893]/5 transition-colors cursor-pointer font-medium"
            >
              Usar Proyecto OpenNavy Local (.)
            </button>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2">
          <div className="relative flex-1">
            <Search className="size-4 text-text-muted absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              placeholder={
                repoType === 'remote'
                  ? 'https://github.com/usuario/nombre-del-repositorio'
                  : '/home/usuario/proyectos/mi-aplicacion'
              }
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full bg-bg-deep border border-border-subtle pl-9 pr-3 py-2 text-xs font-mono text-text placeholder:text-text-muted focus:border-brand focus:outline-none transition-colors"
            />
          </div>

          {repoType === 'remote' && (
            <div className="relative w-full sm:w-32">
              <GitBranch className="size-4 text-text-muted absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
              <input
                type="text"
                placeholder="main"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                className="w-full bg-bg-deep border border-border-subtle pl-9 pr-3 py-2 text-xs font-mono text-text placeholder:text-text-muted focus:border-brand focus:outline-none transition-colors"
              />
            </div>
          )}

          <button
            type="submit"
            disabled={isAnalyzing || !url.trim()}
            className="px-5 py-2 bg-[#003893] hover:bg-[#002d75] text-white font-mono font-bold text-xs flex items-center justify-center gap-2 transition-colors disabled:opacity-40 cursor-pointer"
          >
            {isAnalyzing ? (
              <>
                <RefreshCw className="size-3.5 animate-spin" />
                <span>Analizando...</span>
              </>
            ) : (
              <>
                <Play className="size-3.5 fill-current" />
                <span>{repoType === 'remote' ? 'Clonar y Evaluar' : 'Analizar Ruta Local'}</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Confirmation Modal for Repo Deletion */}
      {isDeleteModalOpen && selectedRepo && (
        <div
          className="fixed inset-0 bg-black/70 backdrop-blur-sm z-[1000] flex items-center justify-center p-4"
          onClick={() => !isDeleting && setIsDeleteModalOpen(false)}
        >
          <div
            className="w-full max-w-md border border-red-300 bg-surface p-6 space-y-4 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 border border-red-200 bg-red-50 text-red-600">
                  <AlertTriangle className="size-5 text-red-600" />
                </div>
                <div>
                  <h3 className="font-sans font-bold text-base text-text">
                    ¿Eliminar repositorio?
                  </h3>
                  <p className="font-mono text-xs text-red-600">
                    Esta acción es irreversible
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => !isDeleting && setIsDeleteModalOpen(false)}
                className="text-text-muted hover:text-text p-1 transition-colors"
              >
                <X className="size-4" />
              </button>
            </div>

            <p className="font-sans text-xs text-text-secondary leading-relaxed">
              Estás a punto de eliminar el repositorio <strong className="text-text font-mono">{selectedRepo.name}</strong>.
              Se borrarán permanentemente sus análisis históricos, métricas de calidad, hallazgos, diagramas de arquitectura y documentación ADR.
            </p>

            <div className="flex justify-end gap-2 pt-2 border-t border-border-subtle">
              <button
                type="button"
                onClick={() => setIsDeleteModalOpen(false)}
                disabled={isDeleting}
                className="font-mono text-xs px-4 py-2 border border-border-subtle bg-surface-2 text-text-secondary hover:text-text transition-colors"
              >
                Cancelar
              </button>
              <button
                type="button"
                onClick={handleConfirmDelete}
                disabled={isDeleting}
                className="font-mono font-bold text-xs px-4 py-2 border border-rose-500 bg-rose-600 hover:bg-rose-700 text-white flex items-center gap-2 transition-colors disabled:opacity-50"
              >
                {isDeleting ? (
                  <>
                    <RefreshCw className="size-3.5 animate-spin" />
                    Eliminando...
                  </>
                ) : (
                  <>
                    <Trash2 className="size-3.5" />
                    Confirmar Eliminación
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
