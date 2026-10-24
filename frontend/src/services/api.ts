const API_BASE = '/api/v1';

async function handleResponse<T>(res: Response, defaultMessage: string): Promise<T> {
  if (!res.ok) {
    let errorDetail = '';
    try {
      const errJson = await res.json();
      if (typeof errJson.detail === 'string') {
        errorDetail = errJson.detail;
      } else if (Array.isArray(errJson.detail)) {
        errorDetail = errJson.detail.map((d: any) => `${d.loc?.join('.') || 'campo'}: ${d.msg}`).join(', ');
      } else if (errJson.message) {
        errorDetail = errJson.message;
      }
    } catch {
      // response body was not json or empty
    }
    const finalMsg = errorDetail
      ? `${defaultMessage} (${res.status}): ${errorDetail}`
      : `${defaultMessage} (${res.status} ${res.statusText})`;
    throw new Error(finalMsg);
  }
  return res.json();
}

export interface RepoItem {
  id: string;
  url: string;
  name: string;
  default_branch: string;
  connected_at: string;
  last_run_status?: string;
  last_global_score?: number;
  last_analyzed_at?: string;
}

export interface MetricItem {
  criterio: string;
  valor: number;
  umbral?: number;
  severidad: string;
  detalles?: any;
}

export interface DependencyItem {
  package_name: string;
  ecosystem: string;
  source_file: string;
  current_version: string;
  recommended_version: string;
  status: 'up_to_date' | 'patch_update' | 'minor_update' | 'major_update' | 'incompatible';
  is_compatible: boolean;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  reason: string;
  upgrade_command: string;
}

export interface DependencyAuditResponse {
  repo_id?: string;
  run_id?: string;
  score: number;
  total_dependencies: number;
  up_to_date_count: number;
  outdated_count: number;
  patch_updates_count?: number;
  minor_updates_count?: number;
  major_updates_count?: number;
  incompatible_count: number;
  ecosystems?: string[];
  dependencies: DependencyItem[];
}

export interface FindingItem {
  id: string;
  file_path: string;
  function_name?: string;
  line_number?: number;
  criterio: string;
  veredicto: string;
  explicacion: string;
  rag_source?: string;
  severidad: 'info' | 'warning' | 'high' | 'critical';
  sugerencia?: string;
}

export interface ArchitectureData {
  repo_id: string;
  run_id: string;
  resumen: string;
  ciclos_detectados: string[][];
  has_circular_dependencies: boolean;
  dependencias_nuevas: string[];
  dependencias_rotas: string[];
}

export interface KnowledgeDocument {
  id: string;
  tipo: 'adr' | 'summary' | 'module_doc';
  path: string;
  titulo: string;
  contenido: string;
  created_at: string;
}

export interface CodeCitation {
  file_path: string;
  start_line: number;
  end_line: number;
  label: string;
}

export interface FileTreeNode {
  name: string;
  path: string;
  type: string;
  size?: number;
  language?: string;
  children?: FileTreeNode[];
}

export interface ChatResponse {
  response: string;
  cited_sources?: string[];
  citations?: CodeCitation[];
  timestamp?: string;
}

export interface ChatSessionItem {
  id: string;
  repo_id?: string;
  title: string;
  source: string;
  model: string;
  tier: string;
  messages_count: number;
  created_at: string;
  updated_at: string;
}

export interface ChatSessionDetail {
  id: string;
  repo_id?: string;
  title: string;
  source: string;
  model: string;
  tier: string;
  messages: any[];
  created_at: string;
  updated_at: string;
}

export const api = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<any>(res, 'Error al consultar estado del sistema');
  },

  async getRepos(): Promise<RepoItem[]> {
    const res = await fetch(`${API_BASE}/repos/`);
    return handleResponse<RepoItem[]>(res, 'Error al obtener repositorios');
  },

  async getRepo(repoId: string): Promise<RepoItem> {
    const res = await fetch(`${API_BASE}/repos/${repoId}`);
    return handleResponse<RepoItem>(res, 'Error al obtener repositorio');
  },

  async deleteRepo(repoId: string): Promise<{ success: boolean; message: string; repo_id: string }> {
    const res = await fetch(`${API_BASE}/repos/${repoId}`, {
      method: 'DELETE',
    });
    return handleResponse<{ success: boolean; message: string; repo_id: string }>(res, 'Error al eliminar el repositorio');
  },

  async triggerAnalysis(repoUrl: string, branch: string = 'main') {
    const res = await fetch(`${API_BASE}/repos/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ repo_url: repoUrl, branch }),
    });
    return handleResponse<any>(res, 'Error al iniciar análisis de repositorio');
  },

  async getLatestMetrics(repoId: string) {
    const res = await fetch(`${API_BASE}/repos/${repoId}/metrics`);
    return handleResponse<any>(res, 'Error al obtener métricas');
  },

  async getMetricsHistory(repoId: string) {
    const res = await fetch(`${API_BASE}/repos/${repoId}/metrics/history`);
    return handleResponse<any>(res, 'Error al obtener historial de métricas');
  },

  async getFindings(repoId: string, severity?: string, criterio?: string): Promise<{ total_findings: number; findings: FindingItem[] }> {
    const params = new URLSearchParams();
    if (severity) params.append('severity', severity);
    if (criterio) params.append('criterio', criterio);
    
    const res = await fetch(`${API_BASE}/repos/${repoId}/findings?${params.toString()}`);
    return handleResponse<{ total_findings: number; findings: FindingItem[] }>(res, 'Error al obtener hallazgos');
  },

  async getComplexity(repoId: string) {
    const res = await fetch(`${API_BASE}/repos/${repoId}/complexity`);
    return handleResponse<any>(res, 'Error al obtener mapa de complejidad');
  },

  async getArchitecture(repoId: string): Promise<ArchitectureData> {
    const res = await fetch(`${API_BASE}/repos/${repoId}/architecture`);
    return handleResponse<ArchitectureData>(res, 'Error al obtener arquitectura de dependencias');
  },

  async getDependencies(repoId: string): Promise<DependencyAuditResponse> {
    const res = await fetch(`${API_BASE}/repos/${repoId}/dependencies`);
    return handleResponse<DependencyAuditResponse>(res, 'Error al obtener dependencias');
  },

  async getKnowledge(repoId: string): Promise<{ total_documents: number; documents: KnowledgeDocument[] }> {
    const res = await fetch(`${API_BASE}/repos/${repoId}/knowledge`);
    return handleResponse<{ total_documents: number; documents: KnowledgeDocument[] }>(res, 'Error al obtener documentación');
  },

  async sendChatMessage(repoId: string, message: string): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE}/repos/${repoId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    return handleResponse<ChatResponse>(res, 'Error en chat RAG');
  },

  async downloadPdfReport(repoId: string, repoName: string = 'repository') {
    const res = await fetch(`${API_BASE}/repos/${repoId}/report/pdf`);
    if (!res.ok) {
      let errorDetail = '';
      try {
        const errJson = await res.json();
        errorDetail = errJson.detail || errJson.message || '';
      } catch {
        // ignore
      }
      throw new Error(`Error al generar el informe PDF (${res.status}): ${errorDetail || res.statusText}`);
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `OpenNavy_Report_${repoName}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  // ── Módulo Sesión 01: AI Opportunity Assessment ─────────────────────
  async evaluateAssessment(data: any) {
    const res = await fetch(`${API_BASE}/assessment/evaluate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return handleResponse<any>(res, 'Error al evaluar el assessment');
  },

  async uploadAssessmentExcel(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/assessment/upload`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<any>(res, 'Error al procesar el archivo Excel del assessment');
  },

  async getAssessmentHistory() {
    const res = await fetch(`${API_BASE}/assessment/list`);
    return handleResponse<any>(res, 'Error al listar assessments');
  },

  // ── Módulo DeepCode Explorer (DeepWiki Split-Pane) ──────────────────
  async getRepoTree(repoId: string) {
    const res = await fetch(`${API_BASE}/repos/${repoId}/tree`);
    return handleResponse<FileTreeNode[]>(res, 'Error al obtener el árbol del repositorio');
  },

  async getRepoFile(repoId: string, path: string) {
    const res = await fetch(`${API_BASE}/repos/${repoId}/file?path=${encodeURIComponent(path)}`);
    return handleResponse<{ file_path: string; language: string; total_lines: number; content: string }>(
      res,
      `Error al leer archivo '${path}'`
    );
  },

  async sendDeepQuery(repoId: string, message: string, activeFile?: string) {
    const res = await fetch(`${API_BASE}/repos/${repoId}/deep-query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, active_file: activeFile }),
    });
    return handleResponse<any>(res, 'Error en consulta DeepCode con Gemma 4');
  },

  // ── Módulo Sesiones de Conversación (/resume) ──────────────────
  async getSessions(repoId?: string, source?: string): Promise<ChatSessionItem[]> {
    const params = new URLSearchParams();
    if (repoId) params.append('repo_id', repoId);
    if (source) params.append('source', source);
    const url = `${API_BASE}/sessions/?${params.toString()}`;
    const res = await fetch(url);
    return handleResponse<ChatSessionItem[]>(res, 'Error al listar sesiones de conversación');
  },

  async getSession(sessionId: string): Promise<ChatSessionDetail> {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}`);
    return handleResponse<ChatSessionDetail>(res, 'Error al obtener la sesión de conversación');
  },

  async saveSession(payload: {
    repo_id?: string;
    title: string;
    source?: string;
    model?: string;
    tier?: string;
    messages: any[];
  }): Promise<ChatSessionDetail> {
    const res = await fetch(`${API_BASE}/sessions/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse<ChatSessionDetail>(res, 'Error al guardar la sesión de conversación');
  },

  async updateSession(
    sessionId: string,
    payload: {
      title?: string;
      source?: string;
      model?: string;
      tier?: string;
      messages: any[];
    }
  ): Promise<ChatSessionDetail> {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse<ChatSessionDetail>(res, 'Error al actualizar la sesión de conversación');
  },

  async deleteSession(sessionId: string): Promise<{ success: boolean; message: string }> {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}`, {
      method: 'DELETE',
    });
    return handleResponse<{ success: boolean; message: string }>(res, 'Error al eliminar la sesión de conversación');
  },

  // OpenNavy: Course Plotter & Fleet Sonar
  async plotCourse(payload: {
    repo_id: string;
    mission: string;
    image_base64?: string;
    officer_name?: string;
  }): Promise<{
    mission: string;
    thought_process: string;
    waypoints: Array<{ file: string; lines: [number, number]; reason: string }>;
    reef_warnings: string[];
    action_steps: string[];
    pr_template: string;
  }> {
    const res = await fetch(`${API_BASE}/course/plot`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse<any>(res, 'Error al trazar rumbo con el Almirante Gemma 4');
  },

  async getLatestBlueprint(): Promise<{ latest_blueprint: any | null }> {
    const res = await fetch(`${API_BASE}/sonar/blueprints/latest`);
    return handleResponse<{ latest_blueprint: any | null }>(res, 'Error al consultar el último blueprint del Sonar');
  },

  async getSharedBlueprints(): Promise<{ count: number; blueprints: any[] }> {
    const res = await fetch(`${API_BASE}/sonar/blueprints`);
    return handleResponse<{ count: number; blueprints: any[] }>(res, 'Error al consultar historial de blueprints');
  },

  async getFleetStatus(): Promise<{ active_officers: number; officers: string[] }> {
    const res = await fetch(`${API_BASE}/sonar/status`);
    return handleResponse<{ active_officers: number; officers: string[] }>(res, 'Error al consultar estado del Sonar de Flota');
  },

  connectProgressStream(
    jobId: string,
    onEvent: (eventData: any) => void,
    onError?: (err: any) => void
  ) {
    const eventSource = new EventSource(`${API_BASE}/repos/analyze/${jobId}/stream`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onEvent(data);
        if (data.step === 'completed' || data.step === 'failed') {
          eventSource.close();
        }
      } catch (err) {
        console.error('Error parsing SSE event', err);
      }
    };

    eventSource.onerror = (err) => {
      if (onError) onError(err);
      eventSource.close();
    };

    return eventSource;
  },
};

