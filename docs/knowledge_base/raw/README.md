# Documentos Canónicos en Formato Crudo (Raw Canonical Documents)

Este directorio alberga los documentos oficiales emitidos por organizaciones de estandarización reconocidas (ISO, IEC, NIST, OWASP, IEEE, libros formales de ingeniería de software) en sus formatos originales:
- Archivos `.pdf`
- Documentos `.docx`
- Presentaciones `.pptx`
- Páginas web / HTML `.html`

## Cómo procesar documentos

1. Coloca tu archivo certificado en este directorio (ejemplo: `ISO_IEC_25010_2023.pdf`).
2. Ejecuta el pipeline de ingesta automatizado con Microsoft MarkItDown:
   ```bash
   python -m app.rag.importer --raw-dir ../knowledge-base/raw --out-dir ../knowledge-base/criteria --reindex
   ```
3. El pipeline extraerá el contenido fiel con tablas y listas, inyectará los metadatos canónicos normativos y colocará el `.md` resultante en `knowledge-base/criteria/`.
4. El motor RAG vectorizará inmediatamente los nuevos chunks para que el LLM y el chat puedan citarlos con su autor y sección exacta.
