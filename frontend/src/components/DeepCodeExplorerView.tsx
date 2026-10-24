import React, { useState, useEffect, useRef } from 'react';
import { 
  FolderTree, 
  FileCode, 
  Folder, 
  Send, 
  Zap, 
  ExternalLink, 
  Copy, 
  Check 
} from 'lucide-react';
import { api } from '../services/api';

interface FileTreeNode {
  name: string;
  path: string;
  type: string;
  size?: number;
  language?: string;
  children?: FileTreeNode[];
}

interface DeepExplorerProps {
  repoId: string;
  repoName: string;
}

export const DeepCodeExplorerView: React.FC<DeepExplorerProps> = ({ repoId, repoName }) => {
  const [tree, setTree] = useState<FileTreeNode[]>([]);
  const [activeFile, setActiveFile] = useState<string>('');
  const [fileContent, setFileContent] = useState<string>('');
  const [fileLanguage, setFileLanguage] = useState<string>('plaintext');
  const [highlightRange, setHighlightRange] = useState<[number, number] | null>(null);

  // Chat State
  const [messages, setMessages] = useState<Array<{
    role: 'user' | 'assistant';
    content: string;
    citations?: Array<{ file_path: string; start_line: number; end_line: number; label: string }>;
  }>>([
    {
      role: 'assistant',
      content: `Hola. Soy el auditor **Praxia DeepCode**. Puedes preguntarme cómo funciona el sistema, qué dependencias o clases tienen antipatrones o cómo refactorizar funciones complejas. Navega los archivos a la derecha o haz clic en las citas de código para saltar directamente a sus líneas.`,
    }
  ]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isQuerying, setIsQuerying] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  const codeContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (repoId) {
      loadTree();
    }
  }, [repoId]);

  const loadTree = async () => {
    try {
      const data = await api.getRepoTree(repoId);
      setTree(data);
      // Abrir primer archivo si existe
      if (data && data.length > 0) {
        findAndOpenFile(data);
      }
    } catch (e) {
      console.error('Error cargando árbol', e);
    }
  };

  const findAndOpenFile = (nodes: FileTreeNode[]) => {
    for (const node of nodes) {
      if (node.type === 'file') {
        openFile(node.path);
        return;
      }
      if (node.children) {
        findAndOpenFile(node.children);
        return;
      }
    }
  };

  const openFile = async (path: string, range?: [number, number]) => {
    setActiveFile(path);
    setHighlightRange(range || null);
    try {
      const res = await api.getRepoFile(repoId, path);
      setFileContent(res.content);
      setFileLanguage(res.language);

      // Auto-scroll a la línea
      if (range) {
        setTimeout(() => {
          scrollToLine(range[0]);
        }, 150);
      }
    } catch (e) {
      console.error('Error abriendo archivo', e);
    }
  };

  const scrollToLine = (lineNum: number) => {
    const el = document.getElementById(`line-${lineNum}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isQuerying) return;

    const userText = inputMessage;
    setInputMessage('');
    setMessages((prev) => [...prev, { role: 'user', content: userText }]);
    setIsQuerying(true);

    try {
      const res = await api.sendDeepQuery(repoId, userText, activeFile);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.response,
          citations: res.citations,
        }
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Error al procesar consulta: ${err.message || 'Error del servidor'}`
        }
      ]);
    } finally {
      setIsQuerying(false);
    }
  };

  const copyCode = () => {
    navigator.clipboard.writeText(fileContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderTreeNodes = (nodes: FileTreeNode[], depth: number = 0) => {
    return nodes.map((node) => {
      const isSelected = activeFile === node.path;
      if (node.type === 'directory') {
        return (
          <div key={node.path} className="text-xs">
            <div className="flex items-center gap-1.5 py-1 px-2 text-text-muted hover:text-text cursor-pointer select-none">
              <Folder className="w-3.5 h-3.5 text-brand/60" />
              <span className="font-mono truncate">{node.name}</span>
            </div>
            {node.children && (
              <div className="pl-3 border-l border-border-subtle ml-2">
                {renderTreeNodes(node.children, depth + 1)}
              </div>
            )}
          </div>
        );
      }
      return (
        <div
          key={node.path}
          onClick={() => openFile(node.path)}
          className={`flex items-center gap-1.5 py-1 px-2 text-xs font-mono cursor-pointer transition-colors ${
            isSelected
              ? 'bg-brand-soft text-brand-ink font-semibold border-l-2 border-brand'
              : 'text-text-muted hover:text-text hover:bg-surface-2'
          }`}
        >
          <FileCode className="w-3.5 h-3.5 flex-shrink-0" />
          <span className="truncate">{node.name}</span>
        </div>
      );
    });
  };

  const lines = fileContent ? fileContent.split('\n') : [];

  const renderMessageContent = (content: string) => {
    // Regex matching markdown citations [filepath:start-end] or [filepath:start] or `[filepath:start-end]`
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
      const endLine = match[3] ? parseInt(match[3], 10) : startLine + 5;
      const label = `${filePath}:${startLine}${match[3] ? '-' + endLine : ''}`;

      parts.push(
        <button
          key={`${start}-${label}`}
          type="button"
          onClick={() => openFile(filePath, [startLine, endLine])}
          className="inline-flex items-center gap-1 mx-1 px-2 py-0.5 border border-brand/40 bg-brand-soft hover:bg-brand text-brand-ink font-mono text-[11px] align-baseline transition-colors"
          title={`Abrir ${filePath} en líneas ${startLine}-${endLine}`}
        >
          <ExternalLink className="w-3 h-3 inline" />
          <span>{label}</span>
        </button>
      );

      lastIndex = end;
    }

    if (lastIndex < content.length) {
      parts.push(content.slice(lastIndex));
    }

    return parts;
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-0 border border-border-subtle overflow-hidden bg-surface/90 h-[calc(100vh-100px)] min-h-[600px]">
      {/* ── PANEL IZQUIERDO: Conversación DeepCode & Citaciones (5 Cols) ── */}
      <div className="lg:col-span-5 flex flex-col border-r border-border-subtle h-full bg-surface">
        {/* Top Header */}
        <div className="p-3.5 px-4 border-b border-border-subtle flex items-center justify-between bg-surface-2/40">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-text font-bold">{repoName}</span>
          </div>
          <span className="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 border border-brand/40 bg-brand-soft text-brand">
            <Zap className="w-3 h-3 text-brand" /> Fast RAG
          </span>
        </div>

        {/* Message Feed */}
        <div className="flex-1 overflow-y-auto scroll-accent p-4 space-y-4 text-sm font-sans">
          {messages.map((m, idx) => (
            <div key={idx} className={`space-y-1.5 ${m.role === 'user' ? 'text-right' : 'text-left'}`}>
              <div
                className={`inline-block p-4 border max-w-[90%] text-left ${
                  m.role === 'user'
                    ? 'bg-brand/20 text-text border-brand/40'
                    : 'bg-surface-2/40 text-text-secondary border-border-subtle'
                }`}
              >
                <div className="whitespace-pre-wrap leading-relaxed font-sans text-xs sm:text-[13.5px]">
                  {renderMessageContent(m.content)}
                </div>

                {/* Citaciones exactas de código clicables */}
                {m.citations && m.citations.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-border-subtle space-y-1.5">
                    <span className="text-[11px] font-mono uppercase tracking-wider text-brand block">
                      Citas de código interactivo:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {m.citations.map((c, i) => (
                        <button
                          key={i}
                          type="button"
                          onClick={() => openFile(c.file_path, [c.start_line, c.end_line])}
                          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-brand-soft hover:bg-brand text-brand-ink text-[11px] font-mono border border-brand/40 transition-colors"
                        >
                          <ExternalLink className="w-3 h-3" />
                          <span>{c.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          {isQuerying && (
            <div className="flex items-center gap-3 p-3 border border-brand/30 bg-surface-2/50 max-w-fit">
              <div className="flex gap-1.5 items-center">
                <span className="w-2 h-2 bg-brand animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-brand animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-brand animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
              <span className="text-xs font-mono text-text-secondary">
                Praxia AI razonando con rúbricas RAG y modelo local...
              </span>
            </div>
          )}
        </div>

        {/* Input Bottom Bar */}
        <form onSubmit={handleSendMessage} className="p-3 border-t border-border-subtle bg-surface-2/30 flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Preguntar sobre antipatrones o funciones (ej. ¿cómo refactorizar auth?)..."
            className="flex-1 bg-bg-deep border border-border-subtle px-4 py-2.5 text-xs font-mono text-text placeholder:text-text-muted focus:outline-none focus:border-brand transition-colors"
          />
          <button
            type="submit"
            disabled={isQuerying || !inputMessage.trim()}
            className="px-5 py-2.5 bg-brand hover:bg-brand/90 text-brand-ink font-mono font-bold text-xs flex items-center justify-center transition-colors disabled:opacity-40"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

      {/* ── PANEL DERECHO: Árbol de Carpetas + Visor de Código (7 Cols) ── */}
      <div className="lg:col-span-7 flex flex-col h-full bg-bg-deep">
        {/* Code Header Tab */}
        <div className="p-3 px-4 border-b border-border-subtle flex items-center justify-between bg-surface/80">
          <div className="flex items-center gap-2 text-xs font-mono text-text-secondary">
            <span className="px-2 py-0.5 border border-border-subtle bg-surface-2 text-[10px] text-text-muted uppercase">
              {fileLanguage}
            </span>
            <span className="truncate max-w-[320px] text-text font-semibold">{activeFile || 'Sin archivo seleccionado'}</span>
          </div>

          <button
            onClick={copyCode}
            className="flex items-center gap-1.5 text-xs font-mono text-text-secondary hover:text-text px-2.5 py-1 border border-border-subtle bg-surface-2 hover:border-brand/40 transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copiado' : 'Copiar'}</span>
          </button>
        </div>

        {/* Main Workspace: File Tree (small left) + Code Lines (right) */}
        <div className="flex-1 flex overflow-hidden">
          {/* File Tree Sidebar */}
          <div className="w-56 border-r border-border-subtle bg-surface/40 overflow-y-auto scroll-accent p-2">
            <div className="px-2 py-1 text-[10px] font-mono uppercase tracking-widest text-text-muted mb-1 flex items-center gap-1">
              <FolderTree className="w-3 h-3 text-brand" /> Archivos
            </div>
            {renderTreeNodes(tree)}
          </div>

          {/* Syntax Highlighted Lines Viewer */}
          <div ref={codeContainerRef} className="flex-1 overflow-y-auto scroll-accent p-4 font-mono text-xs leading-6 bg-bg-deep/95">
            {lines.length > 0 ? (
              lines.map((lineText, idx) => {
                const lineNum = idx + 1;
                const isHighlighted =
                  highlightRange && lineNum >= highlightRange[0] && lineNum <= highlightRange[1];
                return (
                  <div
                    key={lineNum}
                    id={`line-${lineNum}`}
                    className={`flex items-start transition-colors px-2 py-0.5 ${
                      isHighlighted
                        ? 'bg-brand-soft border-l-2 border-brand text-text font-medium'
                        : 'hover:bg-surface-2/30 text-text-secondary'
                    }`}
                  >
                    <span className="w-10 text-text-muted select-none flex-shrink-0 text-right pr-4 text-[11px]">
                      {lineNum}
                    </span>
                    <pre className="overflow-x-auto whitespace-pre font-mono m-0">{lineText || ' '}</pre>
                  </div>
                );
              })
            ) : (
              <div className="text-text-muted text-center py-20 font-mono text-xs">
                Selecciona un archivo del árbol a la izquierda para inspeccionar su código.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
