# Rúbrica Normativa: Seguridad en Código y Top 10 LLM (OWASP)

**Autoridad:** Open Web Application Security Project (OWASP Top 10 & OWASP Top 10 for LLM Applications 2025)  
**Rule-ID:** OWASP-SEC-RUBRIC-01  
**Categoría:** security  
**Severidad:** critical  
**Identificador:** `owasp_security_rubric`

---

## 1. Vulnerabilidades Críticas en Código Fuente (OWASP Top 10)
1. **A01: Broken Access Control:** Falla en la imposición de límites en lo que los usuarios autenticados pueden ejecutar.
2. **A02: Cryptographic Failures:** Uso de algoritmos obsoletos (MD5, SHA1), claves simétricas en texto plano o falta de validación criptográfica en webhooks.
3. **A03: Injection:** Inyección de SQL, NoSQL, OS Command o LDAP mediante concatenación de entradas no confiables sin parametrización ni escaping.
4. **A07: Identification and Authentication Failures:** Falta de protección contra fuerza bruta, tokens de sesión débiles o secretos embebidos en el código fuente.

---

## 2. Vulnerabilidades Específicas de Agentes y Modelos LLM (OWASP LLM Top 10)
1. **LLM01: Prompt Injection:** Inyecciones directas o indirectas donde entradas no confiables (ej. código auditado, comentarios) manipulan el comportamiento del modelo.
   - *Mitigación Obligatoria:* Delimitación XML estricta `<untrusted_source_code>` e instrucciones de inmunidad en los system prompts.
2. **LLM06: Sensitive Information Disclosure (Fuga de Datos Sensibles):** Exposición inadvertida de credenciales, PII o tokens propietarios en el prompt o contexto RAG.
   - *Mitigación Obligatoria:* Enmascaramiento forzoso con `SecretMasker` antes de que el texto toque cualquier pipeline de inferencia o RAG.
3. **LLM08: Vector and Embedding Weaknesses:** Inyección de contenido malicioso o no autorizado en la base de conocimiento vectorial que altere las respuestas del sistema.

---

## 3. Criterios de Aceptación de Seguridad en Praxia
- Ningún secreto ni credencial en texto plano puede persistirse ni enviarse a un LLM externo.
- Toda firma de webhook debe verificarse con HMAC-SHA256 en tiempo constante antes del procesamiento.
