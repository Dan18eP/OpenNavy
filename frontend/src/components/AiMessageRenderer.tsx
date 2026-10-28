import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Code2, Copy, Check } from 'lucide-react';
import { CodeCitation } from '../services/api';

interface AiMessageRendererProps {
  content: string;
  citations?: CodeCitation[];
  onOpenFile?: (path: string, range?: [number, number]) => void;
}

const CodeBlock: React.FC<{ language: string; value: string }> = ({ language, value }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(value);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-3 border border-border-subtle overflow-hidden bg-[#131c26] text-[#f8fafc]">
      <div className="flex items-center justify-between px-3 py-1.5 bg-[#192531] border-b border-white/10 text-[10px] font-mono">
        <span className="text-white/70 uppercase tracking-wider font-semibold">
          {language || 'code'}
        </span>
        <button
          type="button"
          onClick={handleCopy}
          className="inline-flex items-center gap-1 text-white/80 hover:text-white transition-colors"
          title="Copiar código"
        >
          {copied ? (
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
      </div>
      <pre className="p-3 overflow-x-auto text-[11px] font-mono leading-relaxed text-[#e2e8f0]">
        <code>{value}</code>
      </pre>
    </div>
  );
};

export const AiMessageRenderer: React.FC<AiMessageRendererProps> = ({
  content,
  citations,
  onOpenFile,
}) => {
  // Pre-process citations in text so file citations become markdown links with citation scheme
  const processedContent = React.useMemo(() => {
    if (!content) return '';
    // Regex for path/to/file.ext:10 or path/to/file.ext:10-25
    const citationRegex = /`?\[([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+):(\d+)(?:-(\d+))?\]`?/g;
    return content.replace(citationRegex, (match, filePath, start, end) => {
      const lineRange = end ? `${start}-${end}` : start;
      return `[${filePath}:${lineRange}](citation:${filePath}:${lineRange})`;
    });
  }, [content]);

  return (
    <div className="space-y-2 text-text">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h1 className="text-base font-bold text-text mt-3 mb-1.5 border-b border-border-subtle pb-1">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-sm font-bold text-text mt-2.5 mb-1 text-[#003893]">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-xs font-bold text-text mt-2 mb-1 uppercase tracking-wide text-[#003893]">
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-xs font-bold text-text mt-1.5 mb-0.5">
              {children}
            </h4>
          ),
          p: ({ children }) => (
            <p className="text-xs leading-relaxed my-1.5 text-text">
              {children}
            </p>
          ),
          ul: ({ children }) => (
            <ul className="list-disc pl-5 space-y-1 my-1.5 text-xs text-text">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal pl-5 space-y-1 my-1.5 text-xs text-text">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="text-xs leading-relaxed text-text">
              {children}
            </li>
          ),
          strong: ({ children }) => (
            <strong className="font-bold text-text">
              {children}
            </strong>
          ),
          em: ({ children }) => (
            <em className="italic text-text-secondary font-medium">
              {children}
            </em>
          ),
          blockquote: ({ children }) => (
            <blockquote className="border-l-2 border-[#003893] pl-3 py-1 my-2 bg-[#003893]/5 text-text-muted italic text-xs">
              {children}
            </blockquote>
          ),
          table: ({ children }) => (
            <div className="overflow-x-auto my-2 border border-border-subtle">
              <table className="w-full border-collapse text-xs font-mono">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-surface-2 border-b border-border-subtle text-text">
              {children}
            </thead>
          ),
          tbody: ({ children }) => (
            <tbody className="divide-y divide-border-subtle bg-surface text-text">
              {children}
            </tbody>
          ),
          tr: ({ children }) => <tr>{children}</tr>,
          th: ({ children }) => (
            <th className="px-2.5 py-1 text-left font-bold text-text border-r last:border-r-0 border-border-subtle">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="px-2.5 py-1 text-text border-r last:border-r-0 border-border-subtle">
              {children}
            </td>
          ),
          a: ({ href, children }) => {
            if (href && href.startsWith('citation:')) {
              const raw = href.replace('citation:', '');
              const parts = raw.split(':');
              const filePath = parts[0];
              const lines = parts[1] ? parts[1].split('-').map(Number) : [1, 1];
              const startLine = lines[0] || 1;
              const endLine = lines[1] || startLine;

              return (
                <button
                  type="button"
                  onClick={() => onOpenFile?.(filePath, [startLine, endLine])}
                  className="inline-flex items-center gap-1 mx-1 px-2 py-0.5 border border-[#003893]/40 bg-[#003893]/10 text-[#003893] font-mono text-[11px] align-baseline hover:bg-[#003893] hover:text-white transition-colors cursor-pointer font-medium"
                  title={`Abrir ${filePath} en líneas ${startLine}-${endLine}`}
                >
                  <Code2 className="size-3 text-[#003893] group-hover:text-white" />
                  <span>{children}</span>
                </button>
              );
            }
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#0084c7] hover:underline font-medium"
              >
                {children}
              </a>
            );
          },
          code: ({ inline, className, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(className || '');
            const value = String(children).replace(/\n$/, '');

            if (!inline && match) {
              return <CodeBlock language={match[1]} value={value} />;
            }
            if (!inline && value.includes('\n')) {
              return <CodeBlock language="plaintext" value={value} />;
            }
            return (
              <code
                className="font-mono text-[11px] px-1.5 py-0.5 bg-surface-2 border border-border-subtle text-[#003893] font-semibold"
                {...props}
              >
                {children}
              </code>
            );
          },
        }}
      >
        {processedContent}
      </ReactMarkdown>

      {/* Code Citations bottom badge list */}
      {citations && citations.length > 0 && (
        <div className="mt-3 pt-2.5 border-t border-border-subtle/60 flex flex-wrap gap-1.5 items-center">
          <span className="font-mono text-[10px] text-text-muted mr-1">Citas de código:</span>
          {citations.map((c, i) => (
            <button
              key={i}
              type="button"
              onClick={() => onOpenFile?.(c.file_path, [c.start_line, c.end_line])}
              className="inline-flex items-center gap-1 px-2 py-0.5 border border-[#003893]/30 bg-surface-2 text-[#003893] font-mono text-[10px] hover:bg-[#003893] hover:text-white transition-colors font-medium"
              title={`Ir a ${c.file_path}:${c.start_line}-${c.end_line}`}
            >
              <Code2 className="size-3 text-[#003893]" />
              <span>{c.file_path}:{c.start_line}-{c.end_line}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
