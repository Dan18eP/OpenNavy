# Estándar de Equipo: Protocolo de Flujo Git, Commits y No-Concurrencia

**Identificador:** `git_workflow_standards`  
**Tipo:** `team_standard`  
**Categoría:** Gobernanza y Proceso de Desarrollo  
**Autoridad:** OpenNavy Engineering Standards Board  
**Rule-ID:** NAVY-TEAM-GIT-01  
**Severidad:** high  
**Versión:** 1.0  

---

## 1. Principio de No-Concurrencia y Secuencialidad
Para garantizar la integridad del código y eliminar colisiones en entornos colaborativos y de agentes autónomos:
1. **Una Tarea a la Vez:** Las Historias de Usuario o refactorizaciones se ejecutan secuencialmente de forma estricta.
2. **Ramas Dedicadas:** Cada entrega nace desde `develop` actualizado y utiliza la convención formal: `feature/<nombre-hu>` o `fix/<nombre>`.
3. **Límite de Commits:** Mínimo 2 commits y máximo 4 commits convencionales por Historia de Usuario.

---

## 2. Formato Convencional de Commits y Pull Requests
- **Convención:** `feat(<area>): descripción concisa`, `fix(<area>): ...`, `docs(<area>): ...`.
- **Prohibición Estricta de Emojis:** Tanto los mensajes de commit como los títulos de Pull Requests deben estar libres de emojis.
- **Merge Obligatorio por PR:** Se prohíben merges directos a `develop`; toda integración debe tramitarse mediante Pull Request (`gh pr create` y `gh pr merge --merge`).

---

## 3. Definición de Terminado (DoD)
Una tarea solo se considera concluida cuando:
- Supera el 100% de la suite de pruebas unitarias e integración en verde.
- Genera el reporte de entrega formal en `documentation/done/[area]/...`.
- Registra la bitácora correspondiente en `documentation/changelog/`.
