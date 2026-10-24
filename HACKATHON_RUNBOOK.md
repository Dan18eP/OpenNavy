# Hackathon Runbook: Servidor Gemma 4 & Cloudflare

Guía rápida de referencia para el día de la competencia (9:00 AM - 5:30 PM).

---

## 1. Arrancar el Servidor Central (1 Clic)

En la máquina anfitriona (la tuya o la de tu compañero), abre **PowerShell** en la carpeta del proyecto y ejecuta:

```powershell
.\scripts\start-server.ps1
```

* **Qué hace:**
  1. Inicia el demonio de Ollama con `OLLAMA_ORIGINS=*` y `OLLAMA_KEEP_ALIVE=-1`.
  2. Pre-carga `gemma4:e4b` en memoria.
  3. Levanta el túnel de Cloudflare y genera una URL pública segura tipo:
     `https://ejemplo-palabras-xyz.trycloudflare.com`

> **Importante:** Copia esa URL y compártela en el chat del equipo.

---

## 2. Conexión de los Desarrolladores (Clientes)

Cada integrante del equipo solo necesita configurar la variable de entorno o usar la URL compartida:

### En `.env` de cualquier proyecto (Frontend o Backend):
```env
AI_SERVER_URL=https://tu-url-de-cloudflare.trycloudflare.com/v1
AI_MODEL_NAME=gemma4:e4b
AI_FALLBACK_MODEL=gemma4:e2b
AI_API_KEY=ollama
```

### Probar la conexión desde la terminal:
```bash
python scripts/test-inference.py https://tu-url-de-cloudflare.trycloudflare.com
```

---

## 3. Cambio Rápido de Modelo

No necesitas reiniciar el servidor para alternar entre modelos. Simplemente cambia el nombre en el cuerpo de la petición:
- Para máxima calidad / razonamiento de código: `"model": "gemma4:e4b"`
- Para ultra velocidad / tareas ligeras: `"model": "gemma4:e2b"`

---

## 4. Protocolo de Emergencia ("Plan B")

Si la laptop host se queda sin batería, se congela o la red colapsa a las 4:00 PM:
1. Entra a [Google AI Studio](https://aistudio.google.com/) y genera una API key gratuita.
2. En tu archivo `.env`, cambia únicamente dos líneas:
   ```env
   AI_SERVER_URL=https://generativelanguage.googleapis.com/v1beta/openai/
   AI_API_KEY=TU_GEMINI_API_KEY
   AI_MODEL_NAME=gemini-2.5-flash
   ```
3. Gracias al SDK estándar de OpenAI, todo tu código seguirá funcionando exactamente igual sin cambiar lógica.

---

## ⏱️ 5. Hoja de Ruta para las 8.5 Horas

- **09:00 - 10:00:** Servidor levantado, URL compartida, alcance y arquitectura congelados.
- **10:00 - 13:00:** Lógica central y prompt engineering con Gemma 4.
- **13:00 - 13:30:** Prueba interna de integración (Endpoint respondiendo en streaming).
- **13:30 - 15:30:** Conexión de UI y afinamiento visual.
- **15:30:** **FEATURE FREEZE** (Prohibido añadir código nuevo).
- **15:30 - 16:30:** Pruebas de los 2 caminos felices para la demo y grabación de video backup de 60 segundos.
- **16:30 - 17:30:** Presentación (Pitch) de 3 diapositivas y ensayo en vivo.
