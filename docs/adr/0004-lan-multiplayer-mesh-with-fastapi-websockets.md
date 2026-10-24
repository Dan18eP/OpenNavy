# ADR-0004: Malla Multijugador LAN con WebSockets y Deteccion de Colisiones

## Estado
Aceptado

## Contexto
Durante hackathons, sprints presenciales de software libre o trabajo en oficinas desconectadas de internet exterior, los miembros del equipo sufren de colisiones de código y conflictos de integración (merge conflicts) porque no tienen visibilidad de qué archivos o módulos dependientes están siendo modificados por sus compañeros simultáneamente. Las herramientas colaborativas tradicionales dependen de bases de datos centralizadas en la nube (Firebase, Supabase).

## Decision
Se implementa un concentrador WebSocket en tiempo real sobre FastAPI (`/ws/sonar`) corriendo en el host local de la red LAN:
1. **Presencia de Tripulantes:** Cada cliente en la red se conecta al WebSocket y publica sus coordenadas de navegación (`NAVIGATE`: ruta de archivo y número de issue).
2. **Radar de Proximidad Topológica:** El backend evalúa en tiempo real si el archivo inspeccionado por el Usuario A comparte ciclo o frontera de dependencia con el archivo inspeccionado por el Usuario B según el grafo de Tarjan.
3. **Alerta de Rumbo de Colisión:** Si se detecta acoplamiento fuerte, se emite inmediatamente un evento `COLLISION_ALERT` a ambas pantallas antes de que se guarde o haga commit de los cambios.

## Consecuencias
* Positivo: Prevención proactiva de merge conflicts en tiempo real.
* Positivo: Cero dependencia de servicios en la nube; opera sobre la red Wi-Fi o punto de acceso local del equipo.
* Positivo: Latencia sub-milisegundo dentro de la red local.
* Negativo: Requiere que todos los desarrolladores mantengan conexión activa al WebSocket del servidor host durante la sesión colaborativa.
