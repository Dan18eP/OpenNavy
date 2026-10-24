// Diagnostic test script for Node.js / TypeScript devs
const SERVER_URL = process.argv[2] || "http://localhost:11434";
const cleanUrl = SERVER_URL.replace(/\/+$/, "");
const API_URL = `${cleanUrl}/v1/chat/completions`;

console.log(`\n[1/3] Probando conexión contra: ${cleanUrl}`);

async function testInference() {
  const payload = {
    model: "gemma4:e4b",
    messages: [
      { role: "system", content: "Eres un asistente conciso." },
      { role: "user", content: "Hola! Di 'Servidor listo' y 2 ventajas de Open Source." }
    ],
    stream: true,
    temperature: 0.2
  };

  const startTime = Date.now();
  let firstTokenTime = null;
  let tokenCount = 0;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log("[2/3] Conexión establecida. Recibiendo streaming en tiempo real:\n" + "-".repeat(50));

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const dataStr = line.slice(6).trim();
          if (dataStr === "[DONE]") break;
          try {
            const parsed = JSON.parse(dataStr);
            const content = parsed.choices?.[0]?.delta?.content;
            if (content) {
              if (!firstTokenTime) firstTokenTime = Date.now();
              process.stdout.write(content);
              tokenCount++;
            }
          } catch (e) {}
        }
      }
    }

    const totalTimeMs = Date.now() - startTime;
    const ttftMs = firstTokenTime ? firstTokenTime - startTime : totalTimeMs;
    const genSec = (totalTimeMs - ttftMs) / 1000;
    const tps = genSec > 0 ? (tokenCount / genSec).toFixed(1) : 0;

    console.log("\n" + "-".repeat(50));
    console.log(" Métricas:");
    console.log(`  • TTFT (latencia inicial): ${ttftMs} ms`);
    console.log(`  • Tiempo total: ${(totalTimeMs / 1000).toFixed(2)} s`);
    console.log(`  • Tokens recibidos: ${tokenCount}`);
    console.log(`  • Velocidad aprox.: ${tps} tokens/s`);
    console.log(" Verificación completada con éxito!\n");

  } catch (error) {
    console.error("\n❌ Error al conectar:", error.message);
    process.exit(1);
  }
}

testInference();
