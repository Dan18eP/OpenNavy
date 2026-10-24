import React, { useState, useEffect, useRef } from 'react';
import { 
  FileCode, 
  Folder, 
  FolderOpen,
  Send, 
  Sparkles, 
  Bot, 
  User, 
  Copy, 
  Check, 
  Code2, 
  Loader2, 
  ChevronRight, 
  ChevronDown,
  Search,
  SidebarClose,
  SidebarOpen,
  Terminal,
  HelpCircle,
  FolderTree,
  Cpu,
  ShieldAlert,
  AlertTriangle,
  GitFork,
  BookOpen,
  Layers,
  History,
  RotateCcw,
  Radio,
  Compass,
  X
} from 'lucide-react';
import { api, CodeCitation, ChatSessionItem } from '../services/api';
import { useFleetSonar } from '../hooks/useFleetSonar';
import { FleetSonarRadar } from './FleetSonarRadar';
import { CoursePlotterPanel } from './CoursePlotterPanel';
import { cn } from '../lib/utils';

interface FileTreeNode {
  name: string;
  path: string;
  type: string;
  size?: number;
  language?: string;
  children?: FileTreeNode[];
}

interface UnifiedWorkspaceViewProps {
  repoId: string | null;
  repoName: string;
}

interface WorkspaceMessage {
  role: 'user' | 'assistant';
  content: string;
  citations?: CodeCitation[];
  timestamp: Date;
}

export const UnifiedWorkspaceView: React.FC<UnifiedWorkspaceViewProps> = ({
  repoId,
  repoName,
}) => {
  // Tree & Code State
  const [tree, setTree] = useState<FileTreeNode[]>([]);
  const [activeFile, setActiveFile] = useState<string>('');
  const [fileContent, setFileContent] = useState<string>('');
  const [fileLanguage, setFileLanguage] = useState<string>('plaintext');
  const [highlightRange, setHighlightRange] = useState<[number, number] | null>(null);
  const [isLoadingFile, setIsLoadingFile] = useState<boolean>(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const [isLoadingTree, setIsLoadingTree] = useState<boolean>(false);
  const [treeError, setTreeError] = useState<string | null>(null);
  const [isFileTreeOpen, setIsFileTreeOpen] = useState<boolean>(true);
  const [treeSearch, setTreeSearch] = useState<string>('');
  const [expandedFolders, setExpandedFolders] = useState<Record<string, boolean>>({});

  // Left Panel Navigation: Course Plotter vs Nautical Copilot
  const [activeLeftPanel, setActiveLeftPanel] = useState<'plotter' | 'chat'>('plotter');

  // Chat State
  const [messages, setMessages] = useState<WorkspaceMessage[]>([
    {
      role: 'assistant',
      content: `Hola. Soy el Copilot de arquitectura naval de **OpenNavy**. Puedo ayudarte a explorar este repositorio (${repoName || 'repositorio'}), auditar dependencias con Tarjan SCC y navegar waypoints calculados por Google Gemma 4.\n\nPuedes usar el **Trazador de Rumbo** para ingresar issues o capturas de bugs y saltar a los waypoints en el visor split-view, o activar el radar de **Fleet Sonar** para monitorear colisiones en la red LAN.`,
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isQuerying, setIsQuerying] = useState<boolean>(false);
  const [copiedCode, setCopiedCode] = useState<boolean>(false);
  const [slashSuggestions, setSlashSuggestions] = useState<boolean>(false);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [isSessionsModalOpen, setIsSessionsModalOpen] = useState<boolean>(false);
  const [savedSessions, setSavedSessions] = useState<ChatSessionItem[]>([]);
  const [isLoadingSessions, setIsLoadingSessions] = useState<boolean>(false);

  // Fleet Sonar Real-time Telemetry & Radar (US-08 & US-09 - Dylan Gamero)
  const {
    connected: sonarConnected,
    officerName,
    crew,
    activeCollisions,
    latestBlueprint,
    navigate,
    dismissCollision,
  } = useFleetSonar();
  const [isSonarOpen, setIsSonarOpen] = useState<boolean>(false);

  const codeContainerRef = useRef<HTMLDivElement>(null);
  const chatMessagesEndRef = useRef<HTMLDivElement>(null);

  const slashCommandsList = [
    { cmd: '/help', label: 'Catálogo de Comandos', desc: 'Guía de todos los atajos y herramientas interactivas' },
    { cmd: '/tree', label: 'Árbol Jerárquico', desc: 'Explora y filtra la estructura de directorios y módulos' },
    { cmd: '/models', label: 'Modelos Locales', desc: 'Inspecciona modelos descargados en Ollama local y su tier' },
    { cmd: '/cycles', label: 'Ciclos de Dependencias', desc: 'Audita dependencias circulares con Algoritmo de Tarjan' },
    { cmd: '/solid', label: 'Principios SOLID', desc: 'Diagnóstico de responsabilidades y acoplamiento' },
    { cmd: '/secrets', label: 'Escaneo de Secretos', desc: 'Detecta credenciales expuestas con SecretMasker' },
    { cmd: '/sessions', label: 'Historial de Sesiones', desc: 'Explora y reanuda conversaciones pasadas' },
    { cmd: '/resume', label: 'Reanudar Sesión', desc: 'Vuelve al contexto y mensajes de una sesión anterior' },
  ];

  const quickQuestions = [
    '/help',
    '/tree',
    '/models',
    '¿Cuáles son las violaciones SOLID detectadas?',
    '¿Cómo puedo solucionar las dependencias circulares?',
  ];

  useEffect(() => {
    if (repoId) {
      loadTree();
    }
  }, [repoId]);

  useEffect(() => {
    chatMessagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadTree = async () => {
    if (!repoId) return;
    setIsLoadingTree(true);
    setTreeError(null);
    try {
      const data = await api.getRepoTree(repoId);
      setTree(data);
      if (Array.isArray(data)) {
        const initialExpanded: Record<string, boolean> = {};
        data.forEach((node) => {
          if (node.type === 'directory') {
            initialExpanded[node.path] = true;
          }
        });
        setExpandedFolders(initialExpanded);
        findAndOpenFile(data);
      }
    } catch (e: any) {
      console.error('Error cargando estructura del repositorio', e);
      setTreeError(e.message || 'Error al obtener estructura de directorios del backend.');
      setTree([]);
    } finally {
      setIsLoadingTree(false);
    }
  };

  const findAndOpenFile = (nodes: FileTreeNode[]) => {
    for (const node of nodes) {
      if (node.type === 'file') {
        openFile(node.path);
        return;
      }
      if (node.children && node.children.length > 0) {
        findAndOpenFile(node.children);
        return;
      }
    }
  };

  const openFile = async (path: string, range?: [number, number]) => {
    if (!repoId) return;
    setActiveFile(path);
    setHighlightRange(range || null);
    setIsLoadingFile(true);
    setFileError(null);

    // Notificar posición al radar de colisión de Fleet Sonar (US-08)
    navigate(path);

    try {
      const res = await api.getRepoFile(repoId, path);
      setFileContent(res.content);
      setFileLanguage(res.language || 'plaintext');

      if (range) {
        setTimeout(() => {
          scrollToLine(range[0]);
        }, 150);
      }
    } catch (e: any) {
      console.error('Error al abrir archivo', e);
      setFileError(e.message || `No se pudo leer el archivo '${path}' desde el backend.`);
      setFileContent('');
    } finally {
      setIsLoadingFile(false);
    }
  };

  const scrollToLine = (lineNum: number) => {
    const el = document.getElementById(`workspace-line-${lineNum}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  const toggleFolder = (path: string) => {
    setExpandedFolders((prev) => ({ ...prev, [path]: !prev[path] }));
  };

  const handleSendMessage = async (customPrompt?: string) => {
    const promptToSend = (customPrompt || inputMessage).trim();
    if (!promptToSend || !repoId || isQuerying) return;

    const userMsg: WorkspaceMessage = {
      role: 'user',
      content: promptToSend,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!customPrompt) setInputMessage('');
    setSlashSuggestions(false);

    // ── Interceptor de Comandos Slash en Frontend ──
    const cmdLower = promptToSend.toLowerCase();

    if (cmdLower === '/help' || cmdLower === 'help' || cmdLower === '/ayuda') {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `### Catálogo de Comandos Interactivos (OpenNavy UI)
Selecciona o escribe cualquiera de los siguientes comandos:

- **/tree** — Abre y resalta el árbol de navegación de archivos del repositorio.
- **/models** — Consulta el estado del servicio local de Ollama y los modelos instalados.
- **/cycles** — Evalúa el grafo de dependencias y detecta ciclos con Tarjan SCC.
- **/solid** — Diagnóstico de principios de diseño y acoplamiento estructural.
- **/secrets** — Escaneo de seguridad contra fuga de secretos y credenciales.
- **/clear** — Limpia el historial de conversación actual.`,
          timestamp: new Date(),
        },
      ]);
      return;
    }

    if (cmdLower === '/tree' || cmdLower === 'tree' || cmdLower === '/arbol') {
      setIsFileTreeOpen(true);
      const totalFiles = tree.reduce((acc, n) => acc + (n.type === 'file' ? 1 : (n.children?.length || 0)), 0);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Se ha desplegado el **Árbol Jerárquico del Repositorio** en el panel derecho. Se detectaron **${totalFiles} archivos/módulos** analizables. Puedes filtrar archivos en el buscador superior del explorador o hacer clic en cualquier archivo para inspeccionar su sintaxis.`,
          timestamp: new Date(),
        },
      ]);
      return;
    }

    if (cmdLower === '/clear') {
      setMessages([
        {
          role: 'assistant',
          content: 'Historial del Copilot reiniciado. ¿En qué módulo o principio deseas profundizar ahora?',
          timestamp: new Date(),
        },
      ]);
      return;
    }

    if (cmdLower === '/models' || cmdLower === 'models' || cmdLower === '/modelos') {
      setIsQuerying(true);
      try {
        const health = await api.getHealth();
        const installed = health.installed_models || [];
        const active = health.active_model || 'qwen2.5-coder:1.5b';
        const tier = health.local_tier || 'light';

        const modelsList = installed.length > 0
          ? installed.map((m: any) => `- **${m.name}** (${m.size_mb} MB) ${m.is_active ? '— **[ACTIVO]**' : '— Disponible'}`).join('\n')
          : '- Sin modelos adicionales reportados en Ollama local.';

        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `### Modelos de Inferencia Local en Ollama
- **Modelo Activo:** \`${active}\` (Tier: **${tier.toUpperCase()}**)
- **Inferencia:** 100% On-Premise (Soberana, CPU/GPU local)

**Inventario Local Detectado:**
${modelsList}

*Tip:* Para alternar entre modelos, usa gemma4:e4b (máxima calidad) o gemma4:e2b (ultrarrápido).`,
            timestamp: new Date(),
          },
        ]);
      } catch (err: any) {
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `No se pudo consultar el servicio local de Ollama: ${err.message || 'Servidor no disponible'}`,
            timestamp: new Date(),
          },
        ]);
      } finally {
        setIsQuerying(false);
      }
      return;
    }

    if (cmdLower === '/cycles' || cmdLower === 'cycles' || cmdLower === '/ciclos') {
      setIsQuerying(true);
      try {
        const arch = await api.getArchitecture(repoId);
        const cycles = arch.ciclos_detectados || [];
        const hasCycles = arch.has_circular_dependencies;

        const cycleReport = hasCycles && cycles.length > 0
          ? `**Alerta de Acoplamiento:** Se detectaron **${cycles.length} ciclos cerrados**:\n\n` +
            cycles.map((c: string[], idx: number) => `${idx + 1}. \`${c.join(' → ')}\``).join('\n') +
            `\n\n*Recomendación:* Aplica el Principio de Inversión de Dependencias (DIP) y desacopla los módulos compartidos.`
          : `**Grafo Saludable:** No se detectaron ciclos de importación cerrados (Tarjan SCC: 0 ciclos). Cumple con el Principio de Dependencias Acíclicas (ADP).`;

        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `### Diagnóstico de Dependencias Circulares (Tarjan SCC)\n${cycleReport}`,
            timestamp: new Date(),
          },
        ]);
      } catch (err: any) {
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `Error al evaluar arquitectura de dependencias: ${err.message}`,
            timestamp: new Date(),
          },
        ]);
      } finally {
        setIsQuerying(false);
      }
      return;
    }

    if (cmdLower === '/solid' || cmdLower === 'solid') {
      setIsQuerying(true);
      try {
        const findingsData = await api.getFindings(repoId);
        const solidFindings = (findingsData.findings || []).filter(
          (f) => f.criterio.toLowerCase().includes('solid') || f.criterio.toLowerCase().includes('clean')
        );

        const summary = solidFindings.length > 0
          ? `Se registraron **${solidFindings.length} violaciones de Principios SOLID**:\n\n` +
            solidFindings.slice(0, 5).map((f) => `- **[${f.severidad.toUpperCase()}]** \`[${f.file_path}:${f.line_number || 1}]\` — ${f.explicacion}`).join('\n')
          : `No se registraron violaciones críticas de principios SOLID en el último escaneo completado.`;

        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `### Diagnóstico de Principios SOLID & Modularidad\n${summary}`,
            timestamp: new Date(),
          },
        ]);
      } catch (err: any) {
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `Error al obtener hallazgos SOLID: ${err.message}`,
            timestamp: new Date(),
          },
        ]);
      } finally {
        setIsQuerying(false);
      }
      return;
    }

    if (cmdLower === '/secrets' || cmdLower === 'secrets' || cmdLower === '/secretos') {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `### Auditoría de Seguridad & Fuga de Secretos (OWASP LLM02)
- **SecretMasker:** Activo en pipeline de ingesta, evaluación y chat RAG.
- **Protección:** Se enmascaran automáticamente claves AWS (\`AKIA...\`), OpenAI (\`sk-...\`), GitHub Tokens (\`ghp_...\`), JWT Tokens y contraseñas hardcodeadas antes de cualquier inferencia.
- **Estado:** Todas las solicitudes en este Workspace pasan por el sanitizador previo.`,
          timestamp: new Date(),
        },
      ]);
      return;
    }

    if (cmdLower === '/sessions' || cmdLower === 'sessions' || cmdLower === '/sesiones' || cmdLower === '/resume' || cmdLower === 'resume') {
      openSessionsManager();
      return;
    }

    setIsQuerying(true);

    try {
      let res;
      try {
        res = await api.sendDeepQuery(repoId, promptToSend, activeFile || undefined);
      } catch (deepErr: any) {
        try {
          res = await api.sendChatMessage(repoId, promptToSend);
        } catch (chatErr: any) {
          throw new Error(`Inferencia DeepQuery: ${deepErr.message || 'Error'} | Chat RAG: ${chatErr.message || 'Error'}`);
        }
      }

      const newAssistantMsg: WorkspaceMessage = {
        role: 'assistant',
        content: res.response,
        citations: res.citations,
        timestamp: new Date(),
      };

      setMessages((prev) => {
        const updated = [...prev, newAssistantMsg];
        // Auto-guardar la sesión en la base de datos
        persistSession(updated);
        return updated;
      });
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Error al procesar consulta: ${err.message || 'Error del servidor RAG.'}`,
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsQuerying(false);
    }
  };

  const persistSession = async (allMessages: WorkspaceMessage[]) => {
    if (!repoId) return;
    try {
      const serializableMessages = allMessages.map((m) => ({
        role: m.role,
        content: m.content,
        citations: m.citations,
        timestamp: m.timestamp instanceof Date ? m.timestamp.toISOString() : m.timestamp,
      }));

      const firstUserMsg = allMessages.find((m) => m.role === 'user');
      const title = firstUserMsg ? firstUserMsg.content.slice(0, 60) : `Conversación en ${repoName || 'repositorio'}`;

      if (activeSessionId) {
        await api.updateSession(activeSessionId, {
          title,
          source: 'web',
          messages: serializableMessages,
        });
      } else {
        const created = await api.saveSession({
          repo_id: repoId,
          title,
          source: 'web',
          messages: serializableMessages,
        });
        setActiveSessionId(created.id);
      }
    } catch (e) {
      console.error('Error al persistir sesión', e);
    }
  };

  const openSessionsManager = async () => {
    setIsSessionsModalOpen(true);
    setIsLoadingSessions(true);
    try {
      const sessions = await api.getSessions(repoId || undefined);
      setSavedSessions(sessions);
    } catch (e) {
      console.error('Error al cargar lista de sesiones', e);
    } finally {
      setIsLoadingSessions(false);
    }
  };

  const resumeSession = async (sessionId: string) => {
    try {
      const detail = await api.getSession(sessionId);
      if (detail && Array.isArray(detail.messages)) {
        const parsed = detail.messages.map((m: any) => ({
          role: m.role || 'assistant',
          content: m.content || '',
          citations: m.citations || [],
          timestamp: m.timestamp ? new Date(m.timestamp) : new Date(),
        }));
        setMessages(parsed);
        setActiveSessionId(detail.id);
        setIsSessionsModalOpen(false);
      }
    } catch (e) {
      console.error('Error al reanudar sesión', e);
    }
  };

  const copyCodeToClipboard = () => {
    if (!fileContent) return;
    navigator.clipboard.writeText(fileContent);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const renderMessageContent = (content: string, citations?: CodeCitation[]) => {
    const citationRegex = /`?\[([a-zA-Z0-9_\-\./\\]+):(\d+)(?:-(\d+))?\]`?/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = citationRegex.exec(content)) !== null) {
      const start = match.index;
      const end = citationRegex.lastIndex;

      if (start > lastIndex) {
        parts.push(content.slice(lastIndex, start));
      }

      const filePath = match[1];
      const startLine = parseInt(match[2], 10);
      const endLine = match[3] ? parseInt(match[3], 10) : startLine;
      const label = `${filePath}:${startLine}${match[3] ? '-' + endLine : ''}`;

      parts.push(
        <button
          key={`${start}-${label}`}
          type="button"
          onClick={() => openFile(filePath, [startLine, endLine])}
          className="inline-flex items-center gap-1 mx-1 px-2 py-0.5 border border-brand/50 bg-brand-soft text-brand-ink font-mono text-[11px] align-baseline hover:bg-brand transition-colors cursor-pointer"
          title={`Abrir ${filePath} en líneas ${startLine}-${endLine}`}
        >
          <Code2 className="size-3 text-brand" />
          <span>{label}</span>
        </button>
      );

      lastIndex = end;
    }

    if (lastIndex < content.length) {
      parts.push(content.slice(lastIndex));
    }

    return (
      <div className="space-y-2">
        <p className="whitespace-pre-wrap leading-relaxed">{parts}</p>

        {citations && citations.length > 0 && (
          <div className="mt-3 pt-2.5 border-t border-border-subtle/60 flex flex-wrap gap-1.5 items-center">
            <span className="font-mono text-[10px] text-text-muted mr-1">Citas de código:</span>
            {citations.map((c, i) => (
              <button
                key={i}
                type="button"
                onClick={() => openFile(c.file_path, [c.start_line, c.end_line])}
                className="inline-flex items-center gap-1 px-2 py-0.5 border border-brand/40 bg-surface-2 text-text font-mono text-[10px] hover:border-brand hover:text-brand transition-colors"
              >
                <Code2 className="size-3 text-brand" />
                <span>{c.file_path}:{c.start_line}-{c.end_line}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderTreeNodes = (nodes: FileTreeNode[], depth: number = 0) => {
    return nodes
      .filter((node) => {
        if (!treeSearch.trim()) return true;
        const q = treeSearch.toLowerCase();
        return node.name.toLowerCase().includes(q) || node.path.toLowerCase().includes(q);
      })
      .map((node) => {
        if (node.type === 'directory') {
          const isExpanded = !!expandedFolders[node.path];
          return (
            <div key={node.path} className="text-xs">
              <div
                onClick={() => toggleFolder(node.path)}
                className="flex items-center gap-1.5 py-1 px-2 text-text-muted hover:text-text cursor-pointer select-none transition-colors"
                style={{ paddingLeft: `${depth * 10 + 8}px` }}
              >
                {isExpanded ? (
                  <ChevronDown className="size-3.5 text-text-muted flex-shrink-0" />
                ) : (
                  <ChevronRight className="size-3.5 text-text-muted flex-shrink-0" />
                )}
                {isExpanded ? (
                  <FolderOpen className="size-3.5 text-brand flex-shrink-0" />
                ) : (
                  <Folder className="size-3.5 text-brand/70 flex-shrink-0" />
                )}
                <span className="font-mono truncate">{node.name}</span>
              </div>
              {isExpanded && node.children && (
                <div>{renderTreeNodes(node.children, depth + 1)}</div>
              )}
            </div>
          );
        }

        const isSelected = activeFile === node.path;
        const peerOnThisFile = crew.find(
          (c) => c.officer_name !== officerName && c.current_file === node.path
        );
        const isColliding = activeCollisions.some(
          (a) => a.conflicting_files.includes(node.path)
        );

        return (
          <div
            key={node.path}
            onClick={() => openFile(node.path)}
            style={{ paddingLeft: `${depth * 10 + 16}px` }}
            className={`flex items-center justify-between gap-1.5 py-1 px-2 text-xs font-mono cursor-pointer transition-colors ${
              isSelected
                ? 'bg-brand-soft text-brand-ink font-semibold border-l-2 border-brand'
                : isColliding
                ? 'bg-[#E73427]/10 text-[#E73427] border-l-2 border-[#E73427]'
                : 'text-text-muted hover:text-text hover:bg-surface-2'
            }`}
          >
            <div className="flex items-center gap-2 truncate min-w-0">
              <FileCode className="size-3.5 flex-shrink-0 text-brand/60" />
              <span className="truncate">{node.name}</span>
            </div>

            {peerOnThisFile && (
              <span
                className={cn(
                  "text-[9px] px-1 py-0.2 border font-bold flex items-center gap-1 flex-shrink-0",
                  isColliding
                    ? "border-[#E73427] bg-[#E73427] text-white animate-pulse"
                    : "border-[#FFC72C] bg-[#FFC72C]/20 text-[#B45309]"
                )}
                title={`${peerOnThisFile.officer_name} está operando en este archivo`}
              >
                <Radio className="size-2.5" />
                <span>{peerOnThisFile.officer_name.split(' ')[0]}</span>
              </span>
            )}
          </div>
        );
      });
  };

  const fileLines = fileContent ? fileContent.split('\n') : [];

  return (
    <div className="w-full h-full flex flex-col overflow-hidden bg-bg">
      {/* ── TOP WORKSPACE STATUS BAR ── */}
      <div className="h-10 border-b border-border-subtle bg-surface/80 px-4 flex items-center justify-between text-xs font-mono flex-shrink-0">
        <div className="flex items-center gap-3">
          <span className="px-2 py-0.5 border border-brand/40 bg-brand-soft text-brand font-semibold text-[11px]">
            OPENNAVY COCKPIT
          </span>
          <span className="text-text-muted hidden sm:inline">
            Repositorio: <strong className="text-text">{repoName || repoId || 'N/A'}</strong>
          </span>
        </div>

        <div className="flex items-center gap-2">
          {activeFile && (
            <span className="text-text-muted text-[11px] truncate max-w-xs hidden md:inline">
              Archivo activo: <span className="text-text font-semibold">{activeFile}</span>
            </span>
          )}
          <button
            type="button"
            onClick={() => setIsSonarOpen(!isSonarOpen)}
            className={cn(
              "inline-flex items-center gap-1.5 px-2.5 py-1 border text-[11px] font-mono transition-colors",
              isSonarOpen
                ? "border-[#0084C7] bg-[#0084C7]/15 text-[#0084C7] font-bold"
                : activeCollisions.length > 0
                ? "border-[#E73427] bg-[#E73427]/10 text-[#E73427] animate-pulse font-bold"
                : "border-border-subtle bg-surface text-text-muted hover:text-text"
            )}
            title="Fleet Sonar: Radar Multijugador LAN (US-08 & US-09)"
          >
            <Radio className={cn("size-3.5", sonarConnected ? (activeCollisions.length > 0 ? "text-[#E73427]" : "text-[#0084C7]") : "text-text-muted")} />
            <span>Sonar ({crew.length})</span>
            {activeCollisions.length > 0 && (
              <span className="size-2 rounded-full bg-[#E73427] animate-ping" />
            )}
          </button>
          <button
            type="button"
            onClick={openSessionsManager}
            className="inline-flex items-center gap-1.5 px-2 py-1 border border-border-subtle bg-surface text-text-muted hover:text-text text-[11px]"
            title="Ver Historial de Sesiones (/resume)"
          >
            <History className="size-3.5 text-brand" />
            <span className="hidden sm:inline">Sesiones (/resume)</span>
          </button>
          <button
            type="button"
            onClick={() => setIsFileTreeOpen(!isFileTreeOpen)}
            className="inline-flex items-center gap-1.5 px-2 py-1 border border-border-subtle bg-surface text-text-muted hover:text-text text-[11px]"
            title="Alternar Árbol de Archivos"
          >
            {isFileTreeOpen ? <SidebarClose className="size-3.5" /> : <SidebarOpen className="size-3.5" />}
            <span className="hidden sm:inline">Archivos</span>
          </button>
        </div>
      </div>

      {/* ── COLLISION ALERT BANNER (US-08) ── */}
      {activeCollisions.length > 0 && (
        <div className="bg-[#E73427]/15 border-b border-[#E73427] p-2.5 px-4 flex items-center justify-between gap-3 text-xs font-mono text-[#E73427] animate-pulse z-20">
          <div className="flex items-center gap-2.5 min-w-0">
            <ShieldAlert className="size-4 flex-shrink-0 text-[#E73427]" />
            <span className="font-bold uppercase tracking-wider text-[10px] px-1.5 py-0.5 bg-[#E73427] text-white">
              Rumbo de Colisión Detectado
            </span>
            <span className="truncate text-text font-medium text-[11px]">
              {activeCollisions[0].reason} ({activeCollisions[0].officers.join(' ↔ ')})
            </span>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <button
              onClick={() => setIsSonarOpen(true)}
              className="px-2.5 py-1 border border-[#E73427] bg-[#E73427] text-white text-[11px] font-bold hover:opacity-90"
            >
              Abrir Radar
            </button>
            <button
              onClick={() => dismissCollision(activeCollisions[0].id)}
              className="p-1 hover:text-text"
              title="Descartar alerta de colisión"
            >
              <X className="size-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* ── MAIN WORKSPACE SPLIT AREA ── */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 min-h-0 overflow-hidden">
        {/* ── LEFT: WORKSPACE COPILOT & COURSE PLOTTER (5 COLUMNS) ── */}
        <div className="lg:col-span-5 border-b lg:border-b-0 lg:border-r border-border-subtle bg-surface/40 flex flex-col min-h-0 overflow-hidden">
          {/* Mode Switcher Tabs */}
          <div className="h-11 border-b border-border-subtle bg-surface px-2.5 flex items-center justify-between flex-shrink-0">
            <div className="flex items-center gap-1 font-mono text-xs">
              <button
                type="button"
                onClick={() => setActiveLeftPanel('plotter')}
                className={`px-3 py-1.5 flex items-center gap-1.5 text-xs font-mono transition-colors ${
                  activeLeftPanel === 'plotter'
                    ? 'bg-brand text-bg font-bold border border-brand'
                    : 'text-text-muted hover:text-text hover:bg-surface-2'
                }`}
              >
                <Compass className="size-3.5" />
                <span>Trazador de Rumbo</span>
              </button>
              <button
                type="button"
                onClick={() => setActiveLeftPanel('chat')}
                className={`px-3 py-1.5 flex items-center gap-1.5 text-xs font-mono transition-colors ${
                  activeLeftPanel === 'chat'
                    ? 'bg-brand text-bg font-bold border border-brand'
                    : 'text-text-muted hover:text-text hover:bg-surface-2'
                }`}
              >
                <Sparkles className="size-3.5" />
                <span>Copilot Náutico</span>
              </button>
            </div>
            <span className="font-mono text-[10px] px-2 py-0.5 border border-[#003893]/30 bg-[#003893]/10 text-[#003893] font-semibold hidden sm:inline">
              Gemma 4 · AST & Tarjan
            </span>
          </div>

          {activeLeftPanel === 'plotter' ? (
            <CoursePlotterPanel
              repoId={repoId}
              repoName={repoName}
              onSelectWaypoint={(file, lines) => openFile(file, lines)}
            />
          ) : (
            <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
              {/* Quick Questions Pills */}
              <div className="p-3 border-b border-border-subtle/60 bg-surface-2/30 flex items-center gap-1.5 overflow-x-auto scroll-accent flex-shrink-0">
                {quickQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSendMessage(q)}
                    disabled={isQuerying || !repoId}
                    className="font-mono text-[10px] px-2.5 py-1 border border-border-subtle bg-surface hover:border-brand/50 hover:bg-surface-2 text-text-muted hover:text-text whitespace-nowrap transition-colors flex-shrink-0 disabled:opacity-50"
                  >
                    {q}
                  </button>
                ))}
              </div>

          {/* Messages Scroll Area */}
          <div className="flex-1 overflow-y-auto scroll-accent p-4 space-y-4">
            {messages.map((msg, index) => {
              const isAssistant = msg.role === 'assistant';
              return (
                <div
                  key={index}
                  className={`flex gap-3 text-xs ${
                    isAssistant ? 'items-start' : 'items-start flex-row-reverse'
                  }`}
                >
                  <div
                    className={`size-6 rounded-none flex items-center justify-center flex-shrink-0 mt-0.5 border ${
                      isAssistant
                        ? 'border-brand/40 bg-brand-soft text-brand'
                        : 'border-border-strong bg-surface text-text'
                    }`}
                  >
                    {isAssistant ? <Bot className="size-3.5" /> : <User className="size-3.5" />}
                  </div>

                  <div
                    className={`p-3 max-w-[85%] border font-sans text-xs ${
                      isAssistant
                        ? 'border-border-subtle bg-surface/90 text-text'
                        : 'border-brand/40 bg-brand text-brand-ink font-medium shadow-[0_0_12px_rgba(139,92,246,0.25)]'
                    }`}
                  >
                    {isAssistant
                      ? renderMessageContent(msg.content, msg.citations)
                      : msg.content}
                  </div>
                </div>
              );
            })}

            {isQuerying && (
              <div className="flex items-center gap-2 p-3 border border-border-subtle bg-surface font-mono text-xs text-text-muted">
                <Loader2 className="size-4 animate-spin text-brand" />
                <span>Analizando AST y consultando normas arquitectónicas...</span>
              </div>
            )}

            <div ref={chatMessagesEndRef} />
          </div>

          {/* Copilot Input Form with Slash Auto-Suggest */}
          <div className="relative border-t border-border-subtle bg-surface flex-shrink-0">
            {slashSuggestions && (
              <div className="absolute bottom-full left-0 right-0 mb-1 border border-border-subtle bg-surface/95 backdrop-blur-md shadow-xl p-2 divide-y divide-border-subtle/50 z-20">
                <div className="px-2 py-1 text-[10px] font-mono uppercase tracking-wider text-text-muted flex items-center justify-between">
                  <span>Comandos Disponibles</span>
                  <span>Esc / clic para seleccionar</span>
                </div>
                <div className="space-y-1 pt-1 max-h-48 overflow-y-auto scroll-accent">
                  {slashCommandsList.map((item) => (
                    <button
                      key={item.cmd}
                      type="button"
                      onClick={() => {
                        setInputMessage('');
                        handleSendMessage(item.cmd);
                      }}
                      className="w-full text-left px-2.5 py-1.5 hover:bg-surface-2 flex items-center justify-between group transition-colors"
                    >
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-xs font-bold text-brand group-hover:underline">
                          {item.cmd}
                        </span>
                        <span className="text-xs text-text">{item.label}</span>
                      </div>
                      <span className="text-[10px] text-text-muted hidden sm:inline">
                        {item.desc}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="p-3 flex gap-2"
            >
              <input
                type="text"
                placeholder={
                  repoId
                    ? 'Pregunta al Copilot o escribe / para ver comandos (/help, /tree, /models)...'
                    : 'Selecciona un repositorio para iniciar el Copilot'
                }
                value={inputMessage}
                onChange={(e) => {
                  const val = e.target.value;
                  setInputMessage(val);
                  setSlashSuggestions(val.startsWith('/'));
                }}
                disabled={isQuerying || !repoId}
                className="flex-1 bg-surface-2 border border-border-subtle px-3 py-2 text-xs font-mono text-text outline-none focus:border-brand transition-colors disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={isQuerying || !inputMessage.trim() || !repoId}
                className="px-4 py-2 border border-brand bg-brand text-brand-ink font-mono text-xs font-semibold hover:opacity-95 transition-opacity disabled:opacity-50 flex items-center gap-1.5"
              >
                <Send className="size-3.5" />
                <span className="hidden sm:inline">Enviar</span>
              </button>
            </form>
          </div>
        </div>
      )}
    </div>

        {/* ── RIGHT: EXPLORER & SYNTAX CODE VIEWER (7 COLUMNS) ── */}
        <div className="lg:col-span-7 flex flex-col min-h-0 overflow-hidden bg-bg">
          {/* File Viewer Toolbar */}
          <div className="h-11 border-b border-border-subtle bg-surface px-4 flex items-center justify-between flex-shrink-0">
            <div className="flex items-center gap-2 min-w-0">
              <FileCode className="size-4 text-brand flex-shrink-0" />
              <span className="font-mono text-xs text-text font-semibold truncate">
                {activeFile || 'Selecciona un archivo del árbol'}
              </span>
              {fileLanguage && fileLanguage !== 'plaintext' && (
                <span className="font-mono text-[10px] px-1.5 py-0.5 border border-border-subtle bg-surface-2 text-text-muted uppercase">
                  {fileLanguage}
                </span>
              )}
            </div>

            <div className="flex items-center gap-2">
              {fileContent && (
                <button
                  type="button"
                  onClick={copyCodeToClipboard}
                  className="inline-flex items-center gap-1 px-2.5 py-1 border border-border-subtle bg-surface hover:border-brand/40 text-text-muted hover:text-text font-mono text-xs transition-colors"
                  title="Copiar código fuente"
                >
                  {copiedCode ? (
                    <>
                      <Check className="size-3 text-emerald-400" />
                      <span className="text-emerald-400">Copiado</span>
                    </>
                  ) : (
                    <>
                      <Copy className="size-3" />
                      <span>Copiar</span>
                    </>
                  )}
                </button>
              )}
            </div>
          </div>

          {/* Sub-split: File Tree Sidebar + Code View Area */}
          <div className="flex-1 flex min-h-0 overflow-hidden">
            {/* File Tree Drawer */}
            {isFileTreeOpen && (
              <div className="w-56 sm:w-64 border-r border-border-subtle bg-surface/50 flex flex-col flex-shrink-0 min-h-0">
                {/* Search in Tree */}
                <div className="p-2 border-b border-border-subtle">
                  <div className="relative">
                    <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 size-3 text-text-muted" />
                    <input
                      type="text"
                      placeholder="Filtrar archivos..."
                      value={treeSearch}
                      onChange={(e) => setTreeSearch(e.target.value)}
                      className="w-full pl-7 pr-2 py-1 bg-surface-2 border border-border-subtle text-[11px] font-mono text-text outline-none focus:border-brand"
                    />
                  </div>
                </div>

                {/* Tree List */}
                <div className="flex-1 overflow-y-auto scroll-accent p-1">
                  {isLoadingTree ? (
                    <div className="p-4 text-center text-text-muted font-mono text-[11px] flex flex-col items-center justify-center gap-2">
                      <Loader2 className="size-4 animate-spin text-[#0084C7]" />
                      <span>Cargando árbol de archivos...</span>
                    </div>
                  ) : treeError ? (
                    <div className="p-3 border border-[#E73427] bg-[#E73427]/10 text-xs font-mono text-[#E73427] space-y-2">
                      <div className="font-bold flex items-center gap-1.5">
                        <AlertTriangle className="size-4 flex-shrink-0" />
                        <span>Error de Árbol</span>
                      </div>
                      <p className="text-[11px] leading-tight text-text break-words">{treeError}</p>
                      <button
                        type="button"
                        onClick={loadTree}
                        className="px-2 py-1 bg-[#E73427] text-white text-[10px] font-bold hover:opacity-90"
                      >
                        Reintentar
                      </button>
                    </div>
                  ) : tree.length === 0 ? (
                    <div className="p-4 text-center text-text-muted font-mono text-[11px]">
                      Sin archivos disponibles
                    </div>
                  ) : (
                    renderTreeNodes(tree)
                  )}
                </div>
              </div>
            )}

            {/* Code Lines Container */}
            <div
              ref={codeContainerRef}
              className="flex-1 overflow-y-auto scroll-accent bg-bg/95 p-3 font-mono text-xs select-text"
            >
              {isLoadingFile ? (
                <div className="h-full flex items-center justify-center gap-2 text-text-muted">
                  <Loader2 className="size-5 animate-spin text-brand" />
                  <span>Cargando contenido del archivo...</span>
                </div>
              ) : fileError ? (
                <div className="h-full flex flex-col items-center justify-center p-6 text-center">
                  <div className="p-4 border border-[#E73427] bg-[#E73427]/10 max-w-md space-y-2.5">
                    <div className="flex items-center justify-center gap-2 text-[#E73427] font-bold font-mono text-sm">
                      <AlertTriangle className="size-5 flex-shrink-0" />
                      <span>Error al Cargar Archivo</span>
                    </div>
                    <p className="font-mono text-xs text-text break-words">{fileError}</p>
                    {activeFile && (
                      <button
                        type="button"
                        onClick={() => openFile(activeFile)}
                        className="px-3 py-1.5 bg-[#E73427] text-white text-xs font-mono font-bold hover:opacity-90"
                      >
                        Reintentar Lectura
                      </button>
                    )}
                  </div>
                </div>
              ) : fileContent ? (
                <div className="divide-y divide-transparent">
                  {fileLines.map((line, idx) => {
                    const lineNum = idx + 1;
                    const isHighlighted =
                      highlightRange &&
                      lineNum >= highlightRange[0] &&
                      lineNum <= highlightRange[1];

                    return (
                      <div
                        key={lineNum}
                        id={`workspace-line-${lineNum}`}
                        className={`flex py-0.5 px-2 transition-colors duration-150 ${
                          isHighlighted
                            ? 'bg-brand-soft/70 border-l-2 border-brand text-brand-ink font-semibold'
                            : 'hover:bg-surface-2/40 text-text'
                        }`}
                      >
                        <span className="w-10 select-none text-right pr-4 text-text-muted/60 text-[11px]">
                          {lineNum}
                        </span>
                        <pre className="flex-1 whitespace-pre font-mono overflow-x-auto">
                          {line || ' '}
                        </pre>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-text-muted gap-2">
                  <FileCode className="size-8 text-text-muted/50" />
                  <p className="font-mono text-xs">Selecciona un archivo del explorador para examinarlo</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* ── FLEET SONAR RADAR DRAWER (US-08 & US-09 - Dylan Gamero) ── */}
      {isSonarOpen && (
        <div className="fixed sm:absolute top-10 bottom-0 right-0 w-full sm:w-[420px] bg-surface border-l border-border-strong shadow-2xl z-40 flex flex-col min-h-0">
          <div className="h-10 border-b border-border-subtle bg-surface-2 px-3 flex items-center justify-between flex-shrink-0">
            <div className="flex items-center gap-2">
              <Radio className="size-4 text-[#0084C7] animate-pulse" />
              <span className="font-mono text-xs font-bold text-text">Fleet Sonar Cockpit</span>
              <span className="font-mono text-[10px] text-text-muted">LAN Mesh</span>
            </div>
            <button
              onClick={() => setIsSonarOpen(false)}
              className="p-1 text-text-muted hover:text-text"
              title="Cerrar Sonar"
            >
              <X className="size-4" />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto min-h-0">
            <FleetSonarRadar
              currentFile={activeFile}
              repoId={repoId}
              onOpenFile={(file) => openFile(file)}
              onSelectWaypoint={(file, lines) => openFile(file, lines)}
              className="h-full border-none shadow-none"
            />
          </div>
        </div>
      )}

      {/* ── SESSIONS MODAL (/resume) ── */}
      {isSessionsModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-2xl bg-surface border border-border-subtle shadow-2xl flex flex-col max-h-[80vh]">
            <div className="p-3.5 border-b border-border-subtle flex items-center justify-between bg-surface-2/40">
              <div className="flex items-center gap-2">
                <History className="size-4 text-brand" />
                <h3 className="font-sans text-sm font-bold text-text">Historial de Conversaciones (/resume)</h3>
              </div>
              <button
                type="button"
                onClick={() => setIsSessionsModalOpen(false)}
                className="p-1 text-text-muted hover:text-text transition-colors"
              >
                <X className="size-4" />
              </button>
            </div>

            <div className="p-4 flex-1 overflow-y-auto scroll-accent space-y-2">
              {isLoadingSessions ? (
                <div className="py-12 flex flex-col items-center justify-center gap-2 text-text-muted">
                  <Loader2 className="size-5 animate-spin text-brand" />
                  <span className="font-mono text-xs">Cargando sesiones guardadas...</span>
                </div>
              ) : savedSessions.length === 0 ? (
                <div className="py-12 text-center text-text-muted font-mono text-xs">
                  No hay sesiones guardadas todavía para este repositorio.
                </div>
              ) : (
                savedSessions.map((sess) => (
                  <div
                    key={sess.id}
                    className="p-3 border border-border-subtle bg-surface hover:border-brand/50 transition-colors flex items-center justify-between gap-3 group"
                  >
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-[10px] px-1.5 py-0.5 border border-brand/30 bg-brand-soft text-brand uppercase">
                          {sess.source}
                        </span>
                        <h4 className="font-sans text-xs font-semibold text-text truncate group-hover:text-brand">
                          {sess.title}
                        </h4>
                      </div>
                      <div className="mt-1 flex items-center gap-3 font-mono text-[10px] text-text-muted">
                        <span>Modelo: {sess.model}</span>
                        <span>•</span>
                        <span>{sess.messages_count} mensajes</span>
                        <span>•</span>
                        <span>{new Date(sess.updated_at).toLocaleString()}</span>
                      </div>
                    </div>

                    <button
                      type="button"
                      onClick={() => resumeSession(sess.id)}
                      className="px-3 py-1.5 border border-brand bg-brand text-brand-ink font-mono text-xs font-semibold hover:opacity-95 transition-opacity flex items-center gap-1.5 flex-shrink-0"
                    >
                      <RotateCcw className="size-3.5" />
                      <span>Reanudar</span>
                    </button>
                  </div>
                ))
              )}
            </div>

            <div className="p-3 border-t border-border-subtle bg-surface-2/20 flex justify-end">
              <button
                type="button"
                onClick={() => setIsSessionsModalOpen(false)}
                className="px-4 py-1.5 border border-border-subtle bg-surface font-mono text-xs text-text-muted hover:text-text transition-colors"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
