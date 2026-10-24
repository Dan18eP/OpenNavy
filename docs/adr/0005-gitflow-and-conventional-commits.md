# ADR-0005: Flujo de Trabajo GitFlow y Commits Convencionales

## Estado
Aceptado

## Contexto
OpenNavy se publica como un proyecto open source de alto impacto técnico. Mantener una historia de Git descuidada con commits masivos ("fix everything", "update code") daña la credibilidad del proyecto ante jueces de hackathons, revisores técnicos de la comunidad y mantenedores de software libre.

## Decision
Se adopta formalmente el estándar GitFlow complementado con la especificación de Commits Convencionales (Conventional Commits v1.0.0):

### 1. Modelo de Ramas (GitFlow)
* **`main`:** Rama de producción protegida. Solo contiene versiones estables y etiquetadas listas para entrega.
* **`develop`:** Rama principal de integración donde confluyen las características completadas y probadas.
* **`feature/<nombre>`:** Ramas efímeras creadas a partir de `develop` para desarrollar historias de usuario específicas del backlog (ej. `feature/course-plotter-ui`, `feature/sonar-collision-radar`).
* **`hotfix/<nombre>`:** Correcciones críticas derivadas de `main`.

### 2. Estándar de Mensajes de Commit
Cada commit debe ser atómico y seguir el formato:
`<tipo>(<alcance>): <descripcion concisa en minusculas>`

Tipos permitidos:
* `feat`: Nueva funcionalidad para el usuario.
* `fix`: Corrección de un defecto o bug.
* `docs`: Cambios exclusivos en documentación técnica.
* `refactor`: Modificación de código que no altera funcionalidad ni corrige bugs.
* `test`: Adición o corrección de pruebas unitarias/integración.
* `chore`: Mantenimiento de scripts de build o dependencias.

### 3. Reglas de Estilo
* Estrictamente prohibido el uso de emojis en mensajes de commit, documentación técnica formal y contratos de código para mantener máxima legibilidad en terminales y herramientas CI/CD estándar.

## Consecuencias
* Positivo: Trazabilidad profesional de cada incremento de valor.
* Positivo: Generación automatizada de changelogs y notas de release.
* Positivo: Facilidad para revisión de código por pares en Pull Requests.
