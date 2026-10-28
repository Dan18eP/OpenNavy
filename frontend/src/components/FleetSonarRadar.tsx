import React, { useState, useEffect, useRef } from 'react';
import {
  Radio,
  Users,
  AlertTriangle,
  Compass,
  FileCode,
  ShieldAlert,
  Send,
  Sparkles,
  ExternalLink,
  CheckCircle,
  Wifi,
  WifiOff,
  RefreshCw,
  X,
  Target,
  Layers,
  MapPin,
  Clock,
  ChevronRight,
  UserCheck,
} from 'lucide-react';
import { useFleetSonar } from '../hooks/useFleetSonar';
import { api } from '../services/api';
import { cn } from '../lib/utils';
import { CrewMember, CollisionAlert, SharedBlueprint } from '../services/sonarService';

interface FleetSonarRadarProps {
  currentFile?: string;
  onSelectWaypoint?: (file: string, lines: [number, number]) => void;
  onOpenFile?: (file: string) => void;
  repoId?: string | null;
  className?: string;
}

export const FleetSonarRadar: React.FC<FleetSonarRadarProps> = ({
  currentFile,
  onSelectWaypoint,
  onOpenFile,
  repoId,
  className,
}) => {
  const {
    connected,
    officerName,
    crew,
    activeCollisions,
    latestBlueprint,
    blueprintHistory,
    navigate,
    setOfficerName,
    dismissCollision,
  } = useFleetSonar();

  const [activeTab, setActiveTab] = useState<'radar' | 'telemetry' | 'blueprints' | 'plotter'>('radar');
  const [editingOfficer, setEditingOfficer] = useState<boolean>(false);
  const [officerInput, setOfficerInput] = useState<string>(officerName);

  // Plotter modal / form state
  const [missionInput, setMissionInput] = useState<string>('');
  const [isPlotting, setIsPlotting] = useState<boolean>(false);
  const [plotError, setPlotError] = useState<string | null>(null);

  // Canvas radar ref
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const sweepAngleRef = useRef<number>(0);

  // Notify backend whenever currentFile changes
  useEffect(() => {
    if (currentFile && connected) {
      navigate(currentFile);
    }
  }, [currentFile, connected]);

  // Radar Canvas Animation Loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let isSubscribed = true;

    const render = () => {
      if (!isSubscribed) return;

      const width = canvas.width;
      const height = canvas.height;
      const centerX = width / 2;
      const centerY = height / 2;
      const radius = Math.min(centerX, centerY) - 16;

      // Clear with dark navy / slate tone
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, width, height);

      // Radar Concentric Circles
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 1;

      // Background Grid
      const rings = [0.25, 0.5, 0.75, 1.0];
      rings.forEach((r, idx) => {
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * r, 0, Math.PI * 2);
        ctx.strokeStyle = idx === 3 ? '#334155' : '#1e293b';
        ctx.stroke();

        // Distance text
        ctx.fillStyle = '#475569';
        ctx.font = '9px monospace';
        ctx.fillText(`${Math.round(r * 100)}%`, centerX + 4, centerY - radius * r + 11);
      });

      // Crosshairs
      ctx.beginPath();
      ctx.moveTo(centerX - radius, centerY);
      ctx.lineTo(centerX + radius, centerY);
      ctx.moveTo(centerX, centerY - radius);
      ctx.lineTo(centerX, centerY + radius);
      ctx.strokeStyle = '#1e293b';
      ctx.stroke();

      // Cardinal Points
      ctx.fillStyle = '#64748b';
      ctx.font = '10px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('N', centerX, centerY - radius + 10);
      ctx.fillText('S', centerX, centerY + radius - 4);
      ctx.fillText('E', centerX + radius - 8, centerY + 3);
      ctx.fillText('W', centerX - radius + 8, centerY + 3);

      // Sweep Beam (Rotating sector)
      sweepAngleRef.current = (sweepAngleRef.current + 0.025) % (Math.PI * 2);
      const sweep = sweepAngleRef.current;

      const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
      gradient.addColorStop(0, 'rgba(0, 132, 199, 0.2)');
      gradient.addColorStop(1, 'rgba(0, 132, 199, 0.02)');

      ctx.save();
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, sweep - 0.35, sweep);
      ctx.closePath();
      ctx.fillStyle = gradient;
      ctx.fill();

      // Leading edge of sweep
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(centerX + radius * Math.cos(sweep), centerY + radius * Math.sin(sweep));
      ctx.strokeStyle = '#0084C7';
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.restore();

      // Center Blip: Current Officer (Dylan Gamero)
      ctx.beginPath();
      ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#0084C7';
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Officer label
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('TÚ (Local)', centerX, centerY + 14);

      // Plot peer crew blips
      const otherCrew = crew.filter((c) => c.officer_name !== officerName);
      otherCrew.forEach((member, i) => {
        // Compute distance based on module coupling with current file
        const proximity = computeProximity(currentFile || '', member.current_file || '');
        // Radial distance: 1.0 = same file (very close to center), 0.2 = decoupled (far edge)
        const distRatio = Math.max(0.2, 1.15 - proximity);
        const blipRadius = radius * distRatio;
        const angle = (i * ((Math.PI * 2) / Math.max(1, otherCrew.length))) + 0.5;

        const blipX = centerX + blipRadius * Math.cos(angle);
        const blipY = centerY + blipRadius * Math.sin(angle);

        // Check if this peer is currently in a collision alert
        const isInCollision = activeCollisions.some((a) =>
          a.officers.includes(member.officer_name)
        );

        // Blip pulse if in collision
        if (isInCollision) {
          ctx.beginPath();
          ctx.arc(blipX, blipY, 11, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(231, 52, 39, 0.7)';
          ctx.lineWidth = 2;
          ctx.stroke();
        }

        // Blip point
        ctx.beginPath();
        ctx.arc(blipX, blipY, 5, 0, Math.PI * 2);
        ctx.fillStyle = isInCollision ? '#E73427' : '#FFC72C';
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.2;
        ctx.stroke();

        // Officer tag
        ctx.fillStyle = isInCollision ? '#FCA5A5' : '#E2E8F0';
        ctx.font = '9px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(member.officer_name.split(' ')[0], blipX, blipY - 8);

        // File tag if present
        if (member.current_file) {
          const shortName = member.current_file.split('/').pop() || '';
          ctx.fillStyle = '#94A3B8';
          ctx.font = '8px monospace';
          ctx.fillText(shortName.slice(0, 14), blipX, blipY + 14);
        }
      });

      animationFrameRef.current = requestAnimationFrame(render);
    };

    render();

    return () => {
      isSubscribed = false;
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [crew, officerName, currentFile, activeCollisions]);

  // Compute coupling proximity between two file paths (0.1 to 1.0)
  const computeProximity = (fileA: string, fileB: string): number => {
    if (!fileA || !fileB) return 0.2;
    if (fileA === fileB) return 1.0;

    const partsA = fileA.split('/');
    const partsB = fileB.split('/');

    // Same folder
    if (partsA.slice(0, -1).join('/') === partsB.slice(0, -1).join('/')) {
      return 0.8;
    }

    // Shared parent module
    if (partsA[0] && partsB[0] && partsA[0] === partsB[0]) {
      return 0.55;
    }

    return 0.25;
  };

  // Plot course with Gemma 4 and broadcast to LAN
  const handlePlotCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!missionInput.trim() || isPlotting) return;

    setIsPlotting(true);
    setPlotError(null);

    try {
      const activeRepo = repoId || 'default';
      await api.plotCourse({
        repo_id: activeRepo,
        mission: missionInput.trim(),
        officer_name: officerName,
      });

      setMissionInput('');
      setActiveTab('blueprints');
    } catch (err: any) {
      console.error('Error plotting course', err);
      setPlotError(err.message || 'Error al conectar con el Almirante Gemma 4');
    } finally {
      setIsPlotting(false);
    }
  };

  // Demo simulator helper: simulates a peer navigation to test collision
  const handleSimulatePeerCollision = () => {
    if (!currentFile) {
      alert('Abre primero un archivo en el explorador para probar el radar de colisión.');
      return;
    }
    // Navigate with peer presence simulation
    navigate(currentFile);
  };

  return (
    <div className={cn('flex flex-col bg-surface border border-border-subtle shadow-sm', className)}>
      {/* ── TOP RADAR HEADER ── */}
      <div className="h-10 border-b border-border-subtle bg-surface-2/60 px-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Radio className={cn('size-4', connected ? 'text-[#0084C7] animate-pulse' : 'text-text-muted')} />
            {connected && (
              <span className="absolute -top-0.5 -right-0.5 size-1.5 bg-[#0084C7] rounded-full" />
            )}
          </div>
          <span className="font-mono text-xs font-bold text-text tracking-wide">
            FLEET SONAR
          </span>
          <span className="font-mono text-[10px] text-text-muted hidden sm:inline">
            Radar LAN Multijugador
          </span>
        </div>

        {/* Navigation Tabs inside Radar Panel */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => setActiveTab('radar')}
            className={cn(
              'px-2 py-0.5 text-[11px] font-mono border transition-colors',
              activeTab === 'radar'
                ? 'border-[#0084C7] bg-[#0084C7]/10 text-[#0084C7] font-semibold'
                : 'border-transparent text-text-muted hover:text-text'
            )}
          >
            Radar ({crew.length})
          </button>
          <button
            onClick={() => setActiveTab('telemetry')}
            className={cn(
              'px-2 py-0.5 text-[11px] font-mono border transition-colors',
              activeTab === 'telemetry'
                ? 'border-[#0084C7] bg-[#0084C7]/10 text-[#0084C7] font-semibold'
                : 'border-transparent text-text-muted hover:text-text'
            )}
          >
            Tripulación
          </button>
          <button
            onClick={() => setActiveTab('blueprints')}
            className={cn(
              'px-2 py-0.5 text-[11px] font-mono border transition-colors',
              activeTab === 'blueprints'
                ? 'border-[#0084C7] bg-[#0084C7]/10 text-[#0084C7] font-semibold'
                : 'border-transparent text-text-muted hover:text-text'
            )}
          >
            Planos {latestBlueprint ? '(1)' : ''}
          </button>
          <button
            onClick={() => setActiveTab('plotter')}
            className={cn(
              'px-2 py-0.5 text-[11px] font-mono border transition-colors flex items-center gap-1',
              activeTab === 'plotter'
                ? 'border-[#E73427] bg-[#E73427]/10 text-[#E73427] font-semibold'
                : 'border-transparent text-text-muted hover:text-[#E73427]'
            )}
          >
            <Sparkles className="size-3" />
            <span>Trazar Rumbo</span>
          </button>
        </div>
      </div>

      {/* ── CRITICAL / WARNING COLLISION BANNER (US-08) ── */}
      {activeCollisions.length > 0 && (
        <div className="divide-y divide-border-subtle">
          {activeCollisions.map((collision) => {
            const isCritical = collision.severity === 'CRITICAL';
            return (
              <div
                key={collision.id}
                className={cn(
                  'p-2.5 px-3 flex items-start justify-between gap-3 font-mono text-xs border-b transition-all',
                  isCritical
                    ? 'bg-[#E73427]/10 border-[#E73427] text-[#E73427]'
                    : 'bg-[#FFC72C]/10 border-[#FFC72C] text-[#B45309]'
                )}
              >
                <div className="flex items-start gap-2.5 flex-1 min-w-0">
                  <ShieldAlert className={cn('size-4 mt-0.5 flex-shrink-0 animate-bounce', isCritical ? 'text-[#E73427]' : 'text-[#FFC72C]')} />
                  <div className="space-y-0.5 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-bold uppercase tracking-wider text-[10px] px-1.5 py-0.2 border rounded-xs bg-surface">
                        {isCritical ? 'Rumbo de Colisión Crítico' : 'Alerta de Acoplamiento Tarjan'}
                      </span>
                      <span className="text-[10px] opacity-75">
                        Proximidad: {Math.round((collision.proximity_score || 0.8) * 100)}%
                      </span>
                    </div>
                    <p className="text-[11px] font-sans font-medium text-text leading-tight">
                      <strong>{collision.officers.join(' y ')}</strong> están operando sobre módulos en conflicto.
                    </p>
                    <div className="text-[10px] font-mono text-text-muted truncate">
                      Archivo: <span className="font-semibold text-text">{collision.conflicting_files.join(', ')}</span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => dismissCollision(collision.id)}
                  className="text-text-muted hover:text-text p-1"
                  title="Descartar alerta de radar"
                >
                  <X className="size-3.5" />
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* ── TAB CONTENT ── */}
      <div className="flex-1 min-h-[260px] max-h-[360px] overflow-hidden flex flex-col">
        {/* TAB 1: RADAR CANVAS VIEW */}
        {activeTab === 'radar' && (
          <div className="relative flex-1 bg-[#0f172a] flex flex-col items-center justify-center p-3 select-none">
            <canvas
              ref={canvasRef}
              width={340}
              height={260}
              className="w-full max-w-[340px] h-[260px] block"
            />

            {/* Radar status overlay footer */}
            <div className="absolute bottom-2 left-3 right-3 flex items-center justify-between text-[10px] font-mono text-slate-400 bg-slate-900/80 px-2 py-1 border border-slate-800 backdrop-blur-xs">
              <div className="flex items-center gap-1.5">
                <span className={cn('size-2 rounded-full', connected ? 'bg-emerald-400' : 'bg-red-400')} />
                <span>{connected ? 'LAN Sincronizada' : 'Desconectado'}</span>
              </div>
              <div>
                <span>Tripulantes: <strong>{crew.length}</strong></span>
              </div>
              <div>
                <span>Oficial: <strong>{officerName.split(' ')[0]}</strong></span>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: CREW TELEMETRY VIEW */}
        {activeTab === 'telemetry' && (
          <div className="flex-1 overflow-y-auto p-3 space-y-3 font-mono text-xs">
            {/* Identity Switcher */}
            <div className="p-2.5 border border-border-subtle bg-surface-2/40 flex items-center justify-between gap-2">
              <div className="flex items-center gap-2 min-w-0">
                <UserCheck className="size-4 text-[#0084C7] flex-shrink-0" />
                <div className="min-w-0">
                  <div className="text-[10px] text-text-muted">Tu Oficial en el Radar:</div>
                  {editingOfficer ? (
                    <div className="flex items-center gap-1 mt-1">
                      <input
                        type="text"
                        value={officerInput}
                        onChange={(e) => setOfficerInput(e.target.value)}
                        className="px-2 py-0.5 bg-surface border border-[#0084C7] text-xs font-mono outline-none"
                      />
                      <button
                        onClick={() => {
                          setOfficerName(officerInput);
                          setEditingOfficer(false);
                        }}
                        className="px-2 py-0.5 bg-[#0084C7] text-white text-[11px] font-bold"
                      >
                        Guardar
                      </button>
                    </div>
                  ) : (
                    <div className="font-bold text-text truncate">{officerName}</div>
                  )}
                </div>
              </div>

              {!editingOfficer && (
                <button
                  onClick={() => setEditingOfficer(true)}
                  className="px-2 py-1 text-[10px] border border-border-subtle hover:border-[#0084C7] text-text-muted hover:text-text transition-colors"
                >
                  Cambiar
                </button>
              )}
            </div>

            {/* Quick Officer Presets */}
            <div className="flex items-center gap-1.5 text-[10px] text-text-muted">
              <span>Alternar rol rápido:</span>
              <button
                onClick={() => setOfficerName('Dylan Gamero')}
                className={cn('px-1.5 py-0.5 border', officerName === 'Dylan Gamero' ? 'border-[#0084C7] text-[#0084C7] font-bold' : 'border-border-subtle')}
              >
                Dylan
              </button>
              <button
                onClick={() => setOfficerName('Daniel Echeverría')}
                className={cn('px-1.5 py-0.5 border', officerName === 'Daniel Echeverría' ? 'border-[#0084C7] text-[#0084C7] font-bold' : 'border-border-subtle')}
              >
                Daniel
              </button>
              <button
                onClick={() => setOfficerName('Brandon Carranza')}
                className={cn('px-1.5 py-0.5 border', officerName === 'Brandon Carranza' ? 'border-[#0084C7] text-[#0084C7] font-bold' : 'border-border-subtle')}
              >
                Brandon
              </button>
            </div>

            {/* Crew Members List */}
            <div className="space-y-1.5">
              <div className="text-[10px] uppercase tracking-wider text-text-muted font-bold">
                Tripulantes en el Puente ({crew.length})
              </div>
              {crew.length === 0 ? (
                <div className="p-4 text-center text-text-muted text-[11px] border border-dashed border-border-subtle">
                  Esperando conexión de tripulantes sobre la red local...
                </div>
              ) : (
                crew.map((member, i) => {
                  const isYou = member.officer_name === officerName;
                  return (
                    <div
                      key={i}
                      className={cn(
                        'p-2 border transition-colors flex items-center justify-between gap-2',
                        isYou
                          ? 'border-[#0084C7]/40 bg-[#0084C7]/5'
                          : 'border-border-subtle bg-surface hover:border-border-strong'
                      )}
                    >
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-1.5">
                          <span className={cn('size-2 rounded-full', isYou ? 'bg-[#0084C7]' : 'bg-emerald-400')} />
                          <span className="font-bold text-text text-xs truncate">
                            {member.officer_name} {isYou ? '(Tú)' : ''}
                          </span>
                        </div>
                        <div className="text-[10px] text-text-muted truncate mt-0.5">
                          {member.current_file ? (
                            <button
                              onClick={() => onOpenFile?.(member.current_file!)}
                              className="hover:underline hover:text-[#0084C7] flex items-center gap-1"
                              title="Abrir archivo que inspecciona este compañero"
                            >
                              <FileCode className="size-3" />
                              <span className="truncate">{member.current_file}</span>
                            </button>
                          ) : (
                            <span className="italic">Navegando el puente de mando</span>
                          )}
                        </div>
                      </div>

                      {member.current_file && (
                        <span className="text-[9px] px-1.5 py-0.5 border border-border-subtle bg-surface-2 text-text-muted">
                          {computeProximity(currentFile || '', member.current_file) >= 0.8
                            ? 'Acoplado'
                            : 'Distante'}
                        </span>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          </div>
        )}

        {/* TAB 3: SHARED BLUEPRINTS (US-09) */}
        {activeTab === 'blueprints' && (
          <div className="flex-1 overflow-y-auto p-3 space-y-3 font-mono text-xs">
            {latestBlueprint ? (
              <div className="border border-[#0084C7]/40 bg-[#0084C7]/5 p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="px-1.5 py-0.5 bg-[#0084C7] text-white text-[10px] font-bold">
                    PLANO ACTIVO GEMMA 4
                  </span>
                  <span className="text-[10px] text-text-muted">
                    {new Date(latestBlueprint.timestamp).toLocaleTimeString()}
                  </span>
                </div>

                <div className="font-sans font-semibold text-text text-xs">
                  {latestBlueprint.mission}
                </div>

                <div className="text-[10px] text-text-muted">
                  Trazado por: <strong className="text-text">{latestBlueprint.officer_name}</strong>
                </div>

                {/* Waypoints List */}
                <div className="space-y-1 pt-1 border-t border-border-subtle">
                  <div className="text-[10px] font-bold text-text-muted">Coordenadas Náuticas (Waypoints):</div>
                  <div className="space-y-1">
                    {latestBlueprint.waypoints.map((wp, idx) => (
                      <button
                        key={idx}
                        onClick={() => onSelectWaypoint?.(wp.file, wp.lines)}
                        className="w-full text-left p-1.5 border border-border-subtle bg-surface hover:border-[#0084C7] hover:bg-[#0084C7]/5 flex items-center justify-between group transition-colors"
                      >
                        <div className="flex items-center gap-1.5 min-w-0">
                          <MapPin className="size-3 text-[#0084C7] flex-shrink-0" />
                          <span className="text-[11px] font-semibold text-text truncate">
                            {wp.file}:{wp.lines[0]}-{wp.lines[1]}
                          </span>
                        </div>
                        <span className="text-[10px] text-text-muted group-hover:text-[#0084C7]">
                          Navegar
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-6 text-center text-text-muted border border-dashed border-border-subtle space-y-2">
                <Compass className="size-8 mx-auto text-text-muted/60" />
                <p className="text-xs">No hay planos de rumbo activos en la sesión.</p>
                <button
                  onClick={() => setActiveTab('plotter')}
                  className="px-3 py-1.5 border border-[#0084C7] bg-[#0084C7] text-white text-xs font-semibold"
                >
                  Trazar Rumbo con Gemma 4
                </button>
              </div>
            )}

            {/* History count */}
            {blueprintHistory.length > 1 && (
              <div className="text-[10px] text-text-muted text-right">
                {blueprintHistory.length} planos en el historial de la sesión
              </div>
            )}
          </div>
        )}

        {/* TAB 4: COURSE PLOTTER FORM */}
        {activeTab === 'plotter' && (
          <form onSubmit={handlePlotCourse} className="flex-1 p-3 flex flex-col gap-2 font-mono text-xs">
            <div className="text-[10px] font-bold text-text-muted uppercase tracking-wider">
              Ingesta de Misión / Trazador de Rumbo Multimodal
            </div>

            <textarea
              value={missionInput}
              onChange={(e) => setMissionInput(e.target.value)}
              placeholder="Describe el issue, error o funcionalidad a implementar (ej: 'El endpoint de autenticación no valida expiración del token JWT')..."
              rows={4}
              disabled={isPlotting}
              className="w-full p-2 bg-surface-2 border border-border-subtle text-xs font-mono text-text outline-none focus:border-[#E73427] resize-none"
            />

            {plotError && (
              <div className="p-2 border border-[#E73427] bg-[#E73427]/10 text-[#E73427] text-[11px]">
                {plotError}
              </div>
            )}

            <div className="mt-auto pt-2 flex items-center justify-between border-t border-border-subtle">
              <span className="text-[10px] text-text-muted">
                Difunde automáticamente por WebSocket a la LAN.
              </span>
              <button
                type="submit"
                disabled={isPlotting || !missionInput.trim()}
                className="px-4 py-1.5 border border-[#E73427] bg-[#E73427] text-white text-xs font-bold hover:opacity-90 disabled:opacity-50 flex items-center gap-1.5"
              >
                {isPlotting ? (
                  <>
                    <RefreshCw className="size-3 animate-spin" />
                    <span>Razonando con Gemma 4...</span>
                  </>
                ) : (
                  <>
                    <Send className="size-3" />
                    <span>Trazar y Difundir</span>
                  </>
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
