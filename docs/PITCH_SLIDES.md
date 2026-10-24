---
marp: true
theme: uncover
paginate: true
backgroundColor: #0A1128
color: #F8FAFC
style: |
  section {
    font-family: 'Inter', system-ui, sans-serif;
    text-align: left;
    padding: 40px 60px;
  }
  h1 {
    color: #38BDF8;
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
  }
  h2 {
    color: #94A3B8;
    font-size: 1.4rem;
    margin-top: 0;
  }
  .highlight {
    color: #FACC15;
    font-weight: bold;
  }
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 20px;
  }
  .card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 12px;
    padding: 16px 20px;
  }
  .badge {
    background: #0284C7;
    color: white;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
  }
---

<!-- _class: lead -->
![width:180px](../assets/logo_opennavy.svg)

# OPENNAVY
### El Navegador Soberano de Flota para Repositorios Open Source

<span class="badge">MLH Hacktoberfest 2026</span>
<span class="badge">Google DeepMind Gemma 4</span>
<span class="badge">MIT License</span>

**Equipo:** Daniel Echeverría · Brandon Carranza · Dylan Gamero

---

# 1. El Problema: El Muro de Privacidad y la Niebla de Código

<div class="grid">
  <div class="card">
    <h3 style="color: #F87171; margin-top:0;">🛑 El Muro de Compliance</h3>
    <p>En banca, salud y defensa, <b>Cursor o Copilot están prohibidos</b> por enviar código a nubes de terceros (SOC2, GDPR).</p>
  </div>
  <div class="card">
    <h3 style="color: #FB923C; margin-top:0;">🌊 Fatiga en Open Source</h3>
    <p>El <b>80% de contribuidores abandonan</b> al no poder descifrar arquitecturas de 50.000+ líneas.</p>
  </div>
</div>

<div class="card" style="margin-top: 20px; border-color: #38BDF8;">
  <p style="margin: 0; font-size: 1.15rem;">
    💡 <b>La Solución OpenNavy:</b> Una cabina de mando local-first impulsada por <b>Google Gemma 4</b> y un radar multijugador LAN sin nube.
  </p>
</div>

---

# 2. La Trilogía Tecnológica: Demostración en Vivo

<div class="grid">
  <div class="card">
    <h3 style="color: #38BDF8; margin-top:0;">🧭 Trazador de Rumbo Multimodal</h3>
    <p>Ingesta de capturas de error o issues. <b>Gemma 4 Vision</b> razona en local (<code>&lt;|think|&gt;</code>) y emite <b>waypoints exactos</b> con Tree-sitter.</p>
  </div>
  <div class="card">
    <h3 style="color: #4ADE80; margin-top:0;">🛰️ Sonar de Flota (Malla LAN)</h3>
    <p>WebSockets en FastAPI sobre Wi-Fi local. Detecta <b>colisiones arquitectónicas</b> con el <b>Algoritmo de Tarjan SCC</b> antes de hacer git commit.</p>
  </div>
</div>

<p style="margin-top: 25px; text-align: center; color: #94A3B8;">
  ⚡ <i>0 ms de latencia a la nube · 100% Soberano · Sin cuentas requeridas</i>
</p>

---

# 3. Arquitectura Robusta y Modelo de Negocio

<div class="grid">
  <div class="card">
    <h3 style="color: #38BDF8; margin-top:0;">⚙️ Arquitectura Hexagonal</h3>
    <ul>
      <li>Tree-sitter AST universal</li>
      <li>Tarjan SCC (O(|V|+|E|) ciclos)</li>
      <li>Google Gemma 4 (<code>e4b</code> / <code>e2b</code>)</li>
      <li>FastAPI + React 18 / Tailwind</li>
    </ul>
  </div>
  <div class="card">
    <h3 style="color: #FACC15; margin-top:0;">💼 Estrategia Open-Core</h3>
    <ul>
      <li><b>Comunidad (MIT):</b> $0, 100% libre para Hacktoberfest y devs.</li>
      <li><b>Flota Enterprise:</b> $35 / dev / mes. On-premise para sectores regulados con auditoría ISO 5055.</li>
    </ul>
  </div>
</div>

<div style="text-align: center; margin-top: 30px;">
  <span style="font-size: 1.3rem; color: #38BDF8; font-weight: bold;">
    OpenNavy: La brújula y el radar soberano para el software moderno.
  </span>
</div>
