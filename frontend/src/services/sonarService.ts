/**
 * OpenNavy: Fleet Sonar & Real-Time Multiplayer Telemetry Service
 * Implements US-08 (Architectural Collision Radar) and US-09 (Shared Blueprint Broadcast)
 * Responsible: Dylan Gamero (Real-Time & Systems Engineer)
 */

export interface CrewMember {
  officer_name: string;
  current_file: string | null;
  current_issue: string | null;
  connected_at: string;
}

export interface CollisionAlert {
  id: string;
  severity: 'CRITICAL' | 'WARNING';
  reason: string;
  officers: string[];
  conflicting_files: string[];
  timestamp: string;
  proximity_score?: number; // 0 to 1 (1 = identical file, 0.7 = same directory)
}

export interface BlueprintWaypoint {
  file: string;
  lines: [number, number];
  reason: string;
}

export interface SharedBlueprint {
  id: string;
  officer_name: string;
  mission: string;
  waypoints: BlueprintWaypoint[];
  timestamp: string;
}

export interface SonarState {
  connected: boolean;
  officerName: string;
  crew: CrewMember[];
  activeCollisions: CollisionAlert[];
  latestBlueprint: SharedBlueprint | null;
  blueprintHistory: SharedBlueprint[];
}

type SonarListener = (state: SonarState) => void;

class FleetSonarClient {
  private ws: WebSocket | null = null;
  private officerName: string = 'Dylan Gamero';
  private reconnectTimer: any = null;
  private pingInterval: any = null;
  private listeners: Set<SonarListener> = new Set();

  private state: SonarState = {
    connected: false,
    officerName: 'Dylan Gamero',
    crew: [],
    activeCollisions: [],
    latestBlueprint: null,
    blueprintHistory: [],
  };

  constructor() {
    // Intentar leer el oficial almacenado o usar el default de Dylan
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('opennavy_officer_name');
      if (stored) {
        this.officerName = stored;
        this.state.officerName = stored;
      }
    }
  }

  public setOfficerName(name: string) {
    if (!name.trim()) return;
    this.officerName = name.trim();
    this.state.officerName = this.officerName;
    if (typeof window !== 'undefined') {
      localStorage.setItem('opennavy_officer_name', this.officerName);
    }
    // Reconectar con el nuevo nombre si ya está conectado
    if (this.ws) {
      this.disconnect();
      this.connect();
    } else {
      this.notify();
    }
  }

  public getState(): SonarState {
    return this.state;
  }

  public subscribe(listener: SonarListener): () => void {
    this.listeners.add(listener);
    listener(this.state);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notify() {
    this.listeners.forEach((listener) => listener({ ...this.state }));
  }

  public connect() {
    if (typeof window === 'undefined') return;
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    const loc = window.location;
    const protocol = loc.protocol === 'https:' ? 'wss:' : 'ws:';
    // Utilizar el proxy de Vite o puerto 8000 directamente si es necesario
    const host = loc.host;
    const wsUrl = `${protocol}//${host}/api/v1/sonar/ws/sonar?officer=${encodeURIComponent(this.officerName)}`;

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        this.state.connected = true;
        this.notify();
        this.startHeartbeat();
      };

      this.ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          this.handleMessage(payload);
        } catch (err) {
          console.error('[FleetSonar] Error parsing WebSocket frame', err);
        }
      };

      this.ws.onclose = () => {
        this.state.connected = false;
        this.stopHeartbeat();
        this.notify();
        this.scheduleReconnect();
      };

      this.ws.onerror = (err) => {
        console.warn('[FleetSonar] WebSocket error, attempting reconnect...', err);
        this.ws?.close();
      };
    } catch (e) {
      console.error('[FleetSonar] Connection setup failed', e);
      this.scheduleReconnect();
    }
  }

  public disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    this.stopHeartbeat();
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.state.connected = false;
    this.notify();
  }

  private scheduleReconnect() {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, 3000);
  }

  private startHeartbeat() {
    this.stopHeartbeat();
    this.pingInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'PING' }));
      }
    }, 15000);
  }

  private stopHeartbeat() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  private handleMessage(data: any) {
    const eventType = data.type;

    switch (eventType) {
      case 'FLEET_UPDATE': {
        this.state.crew = data.crew || [];
        this.recomputeCollisions();
        this.notify();
        break;
      }

      case 'PEER_PRESENCE': {
        const { officer_name, file_path, issue_id } = data;
        const existingIndex = this.state.crew.findIndex((c) => c.officer_name === officer_name);
        if (existingIndex >= 0) {
          this.state.crew[existingIndex] = {
            ...this.state.crew[existingIndex],
            current_file: file_path,
            current_issue: issue_id,
          };
        } else {
          this.state.crew.push({
            officer_name,
            current_file: file_path,
            current_issue: issue_id,
            connected_at: data.timestamp || new Date().toISOString(),
          });
        }
        this.recomputeCollisions();
        this.notify();
        break;
      }

      case 'COLLISION_ALERT': {
        const alertId = `col-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`;
        const proximity = data.severity === 'CRITICAL' ? 1.0 : 0.75;
        const newAlert: CollisionAlert = {
          id: alertId,
          severity: data.severity || 'WARNING',
          reason: data.reason || 'Posible conflicto en módulos acoplados.',
          officers: data.officers || [],
          conflicting_files: data.conflicting_files || [],
          timestamp: data.timestamp || new Date().toISOString(),
          proximity_score: proximity,
        };

        // Evitar duplicados idénticos en la lista
        const isDuplicate = this.state.activeCollisions.some(
          (a) =>
            a.severity === newAlert.severity &&
            JSON.stringify(a.officers.sort()) === JSON.stringify(newAlert.officers.sort()) &&
            JSON.stringify(a.conflicting_files.sort()) === JSON.stringify(newAlert.conflicting_files.sort())
        );

        if (!isDuplicate) {
          this.state.activeCollisions = [newAlert, ...this.state.activeCollisions.slice(0, 4)];
          this.notify();
        }
        break;
      }

      case 'SHARED_BLUEPRINT':
      case 'SHARED_BLUEPRINT_SYNC': {
        const bp: SharedBlueprint = data.blueprint;
        if (bp) {
          this.state.latestBlueprint = bp;
          const exists = this.state.blueprintHistory.some((b) => b.id === bp.id);
          if (!exists) {
            this.state.blueprintHistory = [bp, ...this.state.blueprintHistory.slice(0, 19)];
          }
          this.notify();
        }
        break;
      }

      case 'PONG':
        // Heartbeat recibido correctamente
        break;

      default:
        break;
    }
  }

  public navigate(filePath: string, issueId?: string) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(
        JSON.stringify({
          type: 'NAVIGATE',
          file_path: filePath,
          issue_id: issueId,
        })
      );
    }
  }

  public dismissCollision(id: string) {
    this.state.activeCollisions = this.state.activeCollisions.filter((a) => a.id !== id);
    this.notify();
  }

  public clearAllCollisions() {
    this.state.activeCollisions = [];
    this.notify();
  }

  /**
   * Recalcula si el tripulante actual ya no está en conflicto para purgar alertas viejas
   */
  private recomputeCollisions() {
    const currentOfficer = this.officerName;
    const currentMember = this.state.crew.find((c) => c.officer_name === currentOfficer);
    if (!currentMember || !currentMember.current_file) {
      return;
    }

    // Filtrar alertas que ya no involucren archivos activos
    this.state.activeCollisions = this.state.activeCollisions.filter((alert) => {
      if (!alert.officers.includes(currentOfficer)) return true;
      return alert.conflicting_files.includes(currentMember.current_file!);
    });
  }
}

export const fleetSonarClient = new FleetSonarClient();
