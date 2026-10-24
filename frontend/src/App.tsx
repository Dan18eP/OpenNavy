import React, { useState, useEffect } from 'react'
import {
  api,
  RepoItem,
  MetricItem,
  FindingItem,
  ArchitectureData,
  KnowledgeDocument,
  DependencyAuditResponse,
} from './services/api'
import { PraxiaHeader, TabType } from './components/PraxiaHeader'
import { OmarchyHomePage } from './components/OmarchyHomePage'
import { ThemePicker } from './components/ThemePicker'
import { RepoSelector } from './components/RepoSelector'
import { AnalysisProgress } from './components/AnalysisProgress'
import { UnifiedAuditView } from './components/UnifiedAuditView'
import { UnifiedWorkspaceView } from './components/UnifiedWorkspaceView'
import { KnowledgeDocsView } from './components/KnowledgeDocsView'
import { DependenciesModal } from './components/DependenciesModal'
import { X } from 'lucide-react'

export const App: React.FC = () => {
  const [systemStatus, setSystemStatus] = useState<string>('connecting')
  const [repos, setRepos] = useState<RepoItem[]>([])
  const [selectedRepoId, setSelectedRepoId] = useState<string | null>(null)

  // Repo state
  const [metrics, setMetrics] = useState<MetricItem[]>([])
  const [globalScore, setGlobalScore] = useState<number | null>(null)
  const [lastAnalyzedAt, setLastAnalyzedAt] = useState<string | undefined>(undefined)
  const [findings, setFindings] = useState<FindingItem[]>([])
  const [architecture, setArchitecture] = useState<ArchitectureData | null>(null)
  const [knowledgeDocs, setKnowledgeDocs] = useState<KnowledgeDocument[]>([])

  // Pipeline & Modal states
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false)
  const [currentProgressEvent, setCurrentProgressEvent] = useState<any>(null)
  const [isDownloadingPdf, setIsDownloadingPdf] = useState<boolean>(false)
  const [isAuditModalOpen, setIsAuditModalOpen] = useState<boolean>(false)

  // Dependencies modal state
  const [isDependenciesModalOpen, setIsDependenciesModalOpen] = useState<boolean>(false)
  const [dependenciesData, setDependenciesData] = useState<DependencyAuditResponse | null>(null)
  const [isLoadingDependencies, setIsLoadingDependencies] = useState<boolean>(false)

  // Active tab (Omarchy Navigation)
  const [activeTab, setActiveTab] = useState<TabType>('overview')

  // 1. Cargar Estado Inicial del Backend
  useEffect(() => {
    loadHealthAndRepos()
  }, [])

  const loadHealthAndRepos = async () => {
    try {
      const health = await api.getHealth()
      setSystemStatus(health.status || 'healthy')

      const repoList = await api.getRepos()
      setRepos(repoList)

      if (repoList.length > 0 && !selectedRepoId) {
        const preferred = repoList.find((r) => r.name.toLowerCase().includes('opennavy')) || repoList[0]
        setSelectedRepoId(preferred.id)
      }
    } catch (e: any) {
      console.error('Error loading initial data', e)
      setSystemStatus('error')
    }
  }

  // 2. Cargar Datos del Repositorio Seleccionado
  useEffect(() => {
    if (selectedRepoId) {
      loadRepoData(selectedRepoId)
    }
  }, [selectedRepoId])

  const loadRepoData = async (repoId: string) => {
    try {
      const [metricsRes, findingsRes, archRes, knowledgeRes] = await Promise.allSettled([
        api.getLatestMetrics(repoId),
        api.getFindings(repoId),
        api.getArchitecture(repoId),
        api.getKnowledge(repoId),
      ])

      if (metricsRes.status === 'fulfilled') {
        setGlobalScore(metricsRes.value.global_score ?? null)
        setLastAnalyzedAt(metricsRes.value.analyzed_at)
        setMetrics(metricsRes.value.metrics || [])
      } else {
        setGlobalScore(null)
        setLastAnalyzedAt(undefined)
        setMetrics([])
      }

      if (findingsRes.status === 'fulfilled') {
        setFindings(findingsRes.value.findings || [])
      } else {
        setFindings([])
      }

      if (archRes.status === 'fulfilled') {
        setArchitecture(archRes.value)
      } else {
        setArchitecture(null)
      }

      if (knowledgeRes.status === 'fulfilled') {
        setKnowledgeDocs(knowledgeRes.value.documents || [])
      } else {
        setKnowledgeDocs([])
      }
    } catch (e: any) {
      console.error('Error loading repo data', e)
    }
  }

  // 3. Disparar Análisis con Streaming SSE
  const handleTriggerAnalysis = async (repoUrl: string, branch: string) => {
    setIsAnalyzing(true)
    setCurrentProgressEvent({
      step: 'cloning',
      progress: 10,
      message: 'Iniciando pipeline de análisis...',
    })

    try {
      const job = await api.triggerAnalysis(repoUrl, branch)
      setSelectedRepoId(job.repo_id)

      api.connectProgressStream(
        job.job_id,
        (eventData) => {
          setCurrentProgressEvent(eventData)

          if (eventData.step === 'completed') {
            setIsAnalyzing(false)
            loadHealthAndRepos()
            loadRepoData(job.repo_id)
          } else if (eventData.step === 'failed') {
            setIsAnalyzing(false)
            setCurrentProgressEvent({
              step: 'failed',
              progress: 100,
              message: eventData.message || eventData.error || 'El análisis falló en el backend.',
            })
          }
        },
        (err) => {
          console.error('SSE Error', err)
          setIsAnalyzing(false)
          setCurrentProgressEvent({
            step: 'failed',
            progress: 100,
            message: `Error en streaming SSE: ${err?.message || 'Conexión interrumpida con el backend.'}`,
          })
        },
      )
    } catch (e: any) {
      console.error('Error triggering analysis', e)
      setIsAnalyzing(false)
      setCurrentProgressEvent({
        step: 'failed',
        progress: 100,
        message: `Error al iniciar el análisis: ${e.message || 'Verifica que el backend esté activo.'}`,
      })
    }
  }

  // 4. Descargar Informe PDF
  const handleDownloadPdf = async () => {
    if (!selectedRepoId) return
    const selectedRepo = repos.find((r) => r.id === selectedRepoId)
    const repoName = selectedRepo?.name || 'auditoria'
    setIsDownloadingPdf(true)
    try {
      await api.downloadPdfReport(selectedRepoId, repoName)
    } catch (err) {
      console.error('Error al descargar PDF', err)
      alert('Error al generar el informe PDF.')
    } finally {
      setIsDownloadingPdf(false)
    }
  }

  // 5. Abrir Modal de Auditoría de Dependencias
  const handleOpenDependenciesModal = async () => {
    if (!selectedRepoId) return
    setIsDependenciesModalOpen(true)
    setIsLoadingDependencies(true)
    try {
      const res = await api.getDependencies(selectedRepoId)
      setDependenciesData(res)
    } catch (e) {
      console.error('Error loading dependencies', e)
    } finally {
      setIsLoadingDependencies(false)
    }
  }

  // 6. Eliminar Repositorio
  const handleDeleteRepo = async (repoId: string) => {
    try {
      await api.deleteRepo(repoId)
      const updatedRepos = await api.getRepos()
      setRepos(updatedRepos)

      if (selectedRepoId === repoId) {
        if (updatedRepos.length > 0) {
          setSelectedRepoId(updatedRepos[0].id)
        } else {
          setSelectedRepoId(null)
          setGlobalScore(null)
          setLastAnalyzedAt(undefined)
          setMetrics([])
          setFindings([])
          setArchitecture(null)
          setKnowledgeDocs([])
        }
      }
    } catch (e) {
      console.error('Error al eliminar repositorio', e)
      throw e
    }
  }

  const isOverview = activeTab === 'overview'

  return (
    <div className="h-[100dvh] max-h-[100dvh] w-screen max-w-full overflow-hidden flex flex-col bg-bg text-text select-none">
      {/* Omarchy Theme Picker Modal */}
      <ThemePicker />

      {/* Backend Connection Error Banner */}
      {systemStatus === 'error' && (
        <div className="bg-[#E73427] text-white px-4 py-2 font-mono text-xs flex items-center justify-between z-[200] flex-shrink-0">
          <div className="flex items-center gap-2">
            <span className="font-bold uppercase tracking-wide">Error de Conexión:</span>
            <span>No se pudo conectar con el servidor backend de OpenNavy en http://localhost:8000. Verifica que FastAPI esté en ejecución.</span>
          </div>
          <button
            onClick={loadHealthAndRepos}
            className="px-2.5 py-0.5 bg-white text-[#E73427] font-bold text-[11px] hover:bg-slate-100 transition-colors"
          >
            Reconectar
          </button>
        </div>
      )}

      {/* Omarchy Style Header */}
      <PraxiaHeader
        activeTab={activeTab}
        onSelectTab={(tab) => setActiveTab(tab)}
        totalRepos={repos.length}
        findingsCount={findings.length}
        knowledgeDocsCount={knowledgeDocs.length}
        repos={repos}
        selectedRepoId={selectedRepoId}
        onSelectRepo={(id) => setSelectedRepoId(id)}
        onStartAudit={() => setIsAuditModalOpen(true)}
      />

      {/* Main Content Area */}
      {isOverview ? (
        <main className="flex-1 w-full h-[calc(100dvh-56px)] max-h-[calc(100dvh-56px)] overflow-hidden relative">
          <OmarchyHomePage
            onStartAudit={() => setIsAuditModalOpen(true)}
            onNavigate={(tab) => setActiveTab(tab as TabType)}
            onOpenDependencies={handleOpenDependenciesModal}
            findingsCount={findings.length}
            score={globalScore}
            lastAnalyzed={lastAnalyzedAt}
          />
        </main>
      ) : (
        <main className="flex-1 w-full h-[calc(100dvh-56px)] max-h-[calc(100dvh-56px)] overflow-hidden relative">
          {/* Tab 2: Unified Audit (Hallazgos, SOLID & Arquitectura) */}
          {(activeTab === 'audit' || activeTab === 'findings' || activeTab === 'architecture') && (
            <UnifiedAuditView
              findings={findings}
              architecture={architecture}
              globalScore={globalScore}
              onDownloadPdf={handleDownloadPdf}
              isDownloadingPdf={isDownloadingPdf}
              onOpenDependencies={handleOpenDependenciesModal}
            />
          )}

          {/* Tab 3: Unified Workspace (File Tree + Syntax Viewer + RAG Copilot) */}
          {(activeTab === 'workspace' || activeTab === 'explorer' || activeTab === 'chat') && (
            <UnifiedWorkspaceView
              repoId={selectedRepoId}
              repoName={repos.find((r) => r.id === selectedRepoId)?.name || 'repository'}
            />
          )}

          {/* Tab 4: Unified Documentation Hub (ADRs Vivos & AI Assessment) */}
          {(activeTab === 'docs' || activeTab === 'knowledge' || activeTab === 'assessment') && (
            <KnowledgeDocsView documents={knowledgeDocs} />
          )}
        </main>
      )}

      {/* Audit Pipeline Trigger Modal / Overlay */}
      {(isAuditModalOpen || isAnalyzing || currentProgressEvent) && (
        <div className="fixed inset-0 z-[200] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-2xl bg-surface border border-border-strong ring-elevation p-6 relative flex flex-col gap-4">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <h3 className="font-mono text-base font-semibold text-text">
                Pipeline de Auditoría AST & Análisis Estático
              </h3>
              {!isAnalyzing && (
                <button
                  onClick={() => {
                    setIsAuditModalOpen(false)
                    setCurrentProgressEvent(null)
                  }}
                  className="text-text-muted hover:text-text p-1"
                >
                  <X className="size-5" />
                </button>
              )}
            </div>

            <RepoSelector
              repos={repos}
              selectedRepoId={selectedRepoId}
              onSelectRepo={(id) => setSelectedRepoId(id)}
              onTriggerAnalysis={handleTriggerAnalysis}
              onDeleteRepo={handleDeleteRepo}
              isAnalyzing={isAnalyzing}
            />

            {currentProgressEvent && (
              <AnalysisProgress currentEvent={currentProgressEvent} />
            )}
          </div>
        </div>
      )}

      {/* Dependencies Audit Modal */}
      <DependenciesModal
        isOpen={isDependenciesModalOpen}
        onClose={() => setIsDependenciesModalOpen(false)}
        data={dependenciesData}
        isLoading={isLoadingDependencies}
      />
    </div>
  )
}
