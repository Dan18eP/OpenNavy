import React, { useState, useRef } from 'react';
import { Send, Bot, User, Sparkles, BookOpen, Loader2, Code2, X, ExternalLink, Copy, Check } from 'lucide-react';
import { api, CodeCitation } from '../services/api';

interface ChatPanelProps {
  repoId: string | null;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  cited_sources?: string[];
  citations?: CodeCitation[];
  timestamp: Date;
}

interface SplitViewerState {
  filePath: string;
  content: string;
  language: string;
  highlightRange: [number, number] | null;
  loading: boolean;
  error?: string;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ repoId }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '¡Hola! Soy OpenNavy AI Copilot. Puedes preguntarme sobre las métricas de este repositorio, por qué se violó algún principio SOLID, o cómo solucionar las dependencias circulares con Google Gemma 4.',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [splitViewer, setSplitViewer] = useState<SplitViewerState | null>(null);
  const [copiedCode, setCopiedCode] = useState(false);
  const codeViewerRef = useRef<HTMLDivElement>(null);

  const quickQuestions = [
    '¿Cuáles son las violaciones de principios SOLID detectadas?',
    '¿Cómo puedo solucionar las dependencias circulares?',
    '¿Qué funciones tienen la mayor complejidad ciclomática?',
  ];

  const openSplitCode = async (filePath: string, range?: [number, number]) => {
    if (!repoId) return;

    setSplitViewer({
      filePath,
      content: '',
      language: 'plaintext',
      highlightRange: range || null,
      loading: true,
    });

    try {
      const res = await api.getRepoFile(repoId, filePath);
      setSplitViewer({
        filePath,
        content: res.content || '',
        language: res.language || 'plaintext',
        highlightRange: range || null,
        loading: false,
      });

      if (range) {
        setTimeout(() => {
          const el = document.getElementById(`split-line-${range[0]}`);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }, 150);
      }
    } catch (err: any) {
      setSplitViewer((prev) =>
        prev
          ? {
              ...prev,
              loading: false,
              error: err.message || 'No se pudo abrir el archivo especificado.',
            }
          : null
      );
    }
  };

  const closeSplitView = () => {
    setSplitViewer(null);
  };

  const copySplitCode = () => {
    if (!splitViewer?.content) return;
    navigator.clipboard.writeText(splitViewer.content);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const renderTextWithCitations = (content: string) => {
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
          onClick={() => openSplitCode(filePath, [startLine, endLine])}
          className="inline-flex items-center gap-1 mx-1 px-2 py-0.5 border border-brand/40 bg-brand-soft text-brand-ink font-mono text-[11px] align-baseline hover:bg-brand transition-colors cursor-pointer"
          title={`Abrir vista dividida en ${filePath} (${startLine}-${endLine})`}
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

    return parts;
  };

  const handleSend = async (textToSend?: string) => {
    const text = textToSend || input;
    if (!text.trim() || !repoId || isLoading) return;

    const userMsg: Message = {
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await api.sendChatMessage(repoId, text);
      const botMsg: Message = {
        role: 'assistant',
        content: response.response,
        cited_sources: response.cited_sources,
        citations: response.citations,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Lo siento, ocurrió un error al consultar el sistema RAG.',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const splitLines = splitViewer?.content ? splitViewer.content.split('\n') : [];

  return (
    <div
      className={`grid ${
        splitViewer ? 'grid-cols-1 lg:grid-cols-2' : 'grid-cols-1'
      } gap-4 h-full max-h-full p-4 sm:p-6 lg:p-8 overflow-hidden transition-all duration-200`}
    >
      {/* ── PANEL DE CHAT ── */}
      <div className="border border-border-subtle bg-surface/90 flex flex-col h-full min-w-0 overflow-hidden p-5">
        {/* Header */}
        <div className="flex items-center justify-between pb-3.5 border-b border-border-subtle mb-3.5">
          <div className="flex items-center gap-3">
            <div className="p-2 border border-brand/30 bg-brand-soft text-brand">
              <Bot className="size-5" />
            </div>
            <div>
              <h2 className="font-sans text-base font-bold tracking-tight text-text">
                Chat Contextual RAG sobre el Repositorio
              </h2>
              <p className="font-mono text-xs text-text-muted mt-0.5">
                Preguntas ancladas en la base de conocimiento y el historial de análisis
              </p>
            </div>
          </div>
        </div>

        {/* Suggested Quick Questions */}
        <div className="flex items-center gap-2 flex-wrap mb-3.5">
          {quickQuestions.map((q, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSend(q)}
              disabled={isLoading || !repoId}
              className="border border-border-subtle bg-surface-2/60 text-text-secondary hover:text-text hover:border-brand/40 hover:bg-brand-soft font-mono text-xs px-2.5 py-1 transition-all flex items-center gap-1.5 disabled:opacity-40"
            >
              <Sparkles className="size-3 text-brand" />
              <span>{q}</span>
            </button>
          ))}
        </div>

        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto scroll-accent flex flex-col gap-3.5 pr-2">
          {messages.map((m, idx) => {
            const isBot = m.role === 'assistant';
            return (
              <div
                key={idx}
                className={`flex gap-3 max-w-[92%] ${isBot ? 'self-start' : 'self-end flex-row-reverse'}`}
              >
                {isBot ? (
                  <div className="size-7 border border-brand/30 bg-brand-soft text-brand flex items-center justify-center flex-shrink-0">
                    <Bot className="size-4" />
                  </div>
                ) : (
                  <div className="size-7 border border-border-subtle bg-surface-2 text-text flex items-center justify-center flex-shrink-0">
                    <User className="size-4" />
                  </div>
                )}

                <div
                  className={`p-3.5 border text-sm leading-relaxed ${
                    isBot
                      ? 'border-border-subtle bg-surface-2/40 text-text-secondary'
                      : 'border-brand/40 bg-brand/20 text-text'
                  }`}
                >
                  <div className="whitespace-pre-wrap font-sans text-xs sm:text-sm">
                    {isBot ? renderTextWithCitations(m.content) : m.content}
                  </div>

                  {/* Interactive citations badges */}
                  {m.citations && m.citations.length > 0 && (
                    <div className="mt-2.5 pt-2 border-t border-border-subtle flex items-center gap-1.5 flex-wrap">
                      <Code2 className="size-3 text-brand" />
                      <span className="font-mono text-[11px] text-brand">Citas interactivas:</span>
                      {m.citations.map((c, cIdx) => (
                        <button
                          key={cIdx}
                          type="button"
                          onClick={() => openSplitCode(c.file_path, [c.start_line, c.end_line])}
                          className="border border-brand/40 bg-brand-soft text-brand-ink font-mono text-[11px] px-2 py-0.5 inline-flex items-center gap-1 hover:bg-brand transition-colors cursor-pointer"
                        >
                          <ExternalLink className="size-2.5" />
                          <span>{c.label}</span>
                        </button>
                      ))}
                    </div>
                  )}

                  {m.cited_sources && m.cited_sources.length > 0 && (
                    <div className="mt-2.5 pt-2 border-t border-border-subtle flex items-center gap-1.5 flex-wrap">
                      <BookOpen className="size-3 text-cyan-400" />
                      <span className="font-mono text-[11px] text-text-muted">Fuentes RAG:</span>
                      {m.cited_sources.map((src, sIdx) => (
                        <span
                          key={sIdx}
                          className="font-mono text-[11px] border border-border-subtle bg-surface-2 text-text-secondary px-2 py-0.5"
                        >
                          {src}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {isLoading && (
            <div className="flex items-center gap-2 font-mono text-xs text-brand">
              <Loader2 className="size-4 animate-spin text-brand" />
              <span>Consultando rúbrica RAG y base de conocimiento...</span>
            </div>
          )}
        </div>

        {/* Input Form */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex gap-2 mt-4 pt-3 border-t border-border-subtle"
        >
          <input
            type="text"
            placeholder={
              repoId
                ? 'Escribe una pregunta sobre el código, arquitectura o principios SOLID...'
                : 'Selecciona un repositorio primero'
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={!repoId || isLoading}
            className="flex-1 px-4 py-2.5 bg-bg-deep border border-border-subtle text-text placeholder:text-text-muted font-mono text-xs focus:border-brand focus:outline-none transition-colors"
          />

          <button
            type="submit"
            disabled={!repoId || !input.trim() || isLoading}
            className="px-5 py-2.5 bg-brand hover:bg-brand/90 text-brand-ink font-mono font-bold text-xs flex items-center justify-center transition-colors disabled:opacity-40"
          >
            <Send className="size-4" />
          </button>
        </form>
      </div>

      {/* ── PANEL SPLIT CODE VIEWER (Derecha) ── */}
      {splitViewer && (
        <div className="border border-brand/40 bg-bg-deep flex flex-col h-full min-w-0 overflow-hidden">
          {/* Header del split view */}
          <div className="p-3 px-4 border-b border-border-subtle flex items-center justify-between bg-surface/90">
            <div className="flex items-center gap-2 min-w-0">
              <Code2 className="size-4 text-brand flex-shrink-0" />
              <span
                className="font-mono text-xs text-text font-semibold truncate max-w-[240px]"
                title={splitViewer.filePath}
              >
                {splitViewer.filePath}
              </span>
              {splitViewer.highlightRange && (
                <span className="font-mono text-[10px] px-2 py-0.5 border border-brand/40 bg-brand-soft text-brand font-semibold">
                  L{splitViewer.highlightRange[0]}-{splitViewer.highlightRange[1]}
                </span>
              )}
            </div>

            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={copySplitCode}
                disabled={!splitViewer.content}
                className="font-mono text-xs px-2.5 py-1 border border-border-subtle bg-surface-2 hover:border-brand/40 text-text-secondary hover:text-text flex items-center gap-1.5 transition-colors disabled:opacity-40"
              >
                {copiedCode ? <Check className="size-3 text-emerald-400" /> : <Copy className="size-3" />}
                <span>{copiedCode ? 'Copiado' : 'Copiar'}</span>
              </button>

              <button
                type="button"
                onClick={closeSplitView}
                className="p-1 border border-border-subtle bg-surface-2 hover:border-brand/40 text-text-secondary hover:text-text transition-colors"
                title="Cerrar vista dividida"
              >
                <X className="size-4" />
              </button>
            </div>
          </div>

          {/* Cuerpo del visor de código */}
          <div
            ref={codeViewerRef}
            className="flex-1 overflow-y-auto overflow-x-auto p-4 font-mono text-xs leading-6 bg-bg-deep/95 scroll-accent"
          >
            {splitViewer.loading ? (
              <div className="flex items-center justify-center h-full gap-2 font-mono text-xs text-text-muted">
                <Loader2 className="size-4 animate-spin text-brand" />
                Cargando código fuente...
              </div>
            ) : splitViewer.error ? (
              <div className="border border-rose-500/30 bg-rose-950/20 text-rose-300 p-4 font-mono text-xs">
                {splitViewer.error}
              </div>
            ) : splitLines.length > 0 ? (
              splitLines.map((lineText, idx) => {
                const lineNum = idx + 1;
                const isHighlighted =
                  splitViewer.highlightRange &&
                  lineNum >= splitViewer.highlightRange[0] &&
                  lineNum <= splitViewer.highlightRange[1];

                return (
                  <div
                    key={lineNum}
                    id={`split-line-${lineNum}`}
                    className={`flex items-start px-2 py-0.5 transition-colors ${
                      isHighlighted
                        ? 'bg-brand-soft border-l-2 border-brand text-text font-medium'
                        : 'text-text-secondary hover:bg-surface-2/40'
                    }`}
                  >
                    <span className="w-10 text-text-muted select-none flex-shrink-0 text-right pr-4 text-[11px]">
                      {lineNum}
                    </span>
                    <pre className="overflow-x-visible whitespace-pre font-mono m-0">
                      {lineText || ' '}
                    </pre>
                  </div>
                );
              })
            ) : (
              <div className="text-text-muted text-center py-20 font-mono text-xs">
                El archivo está vacío.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
