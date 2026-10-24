import { useState, useEffect } from 'react';
import {
  fleetSonarClient,
  SonarState,
  CrewMember,
  CollisionAlert,
  SharedBlueprint,
} from '../services/sonarService';

export function useFleetSonar() {
  const [state, setState] = useState<SonarState>(fleetSonarClient.getState());

  useEffect(() => {
    // Iniciar conexión WebSocket
    fleetSonarClient.connect();

    // Suscribirse a cambios reactivos
    const unsubscribe = fleetSonarClient.subscribe((updatedState) => {
      setState(updatedState);
    });

    return () => {
      unsubscribe();
    };
  }, []);

  const navigate = (filePath: string, issueId?: string) => {
    fleetSonarClient.navigate(filePath, issueId);
  };

  const setOfficerName = (name: string) => {
    fleetSonarClient.setOfficerName(name);
  };

  const dismissCollision = (id: string) => {
    fleetSonarClient.dismissCollision(id);
  };

  const clearAllCollisions = () => {
    fleetSonarClient.clearAllCollisions();
  };

  return {
    connected: state.connected,
    officerName: state.officerName,
    crew: state.crew,
    activeCollisions: state.activeCollisions,
    latestBlueprint: state.latestBlueprint,
    blueprintHistory: state.blueprintHistory,
    navigate,
    setOfficerName,
    dismissCollision,
    clearAllCollisions,
  };
}
