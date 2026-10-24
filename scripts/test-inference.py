#!/usr/bin/env python3
"""
Script de diagnóstico rápido para verificar conectividad y velocidad de tokens
con el servidor de Gemma 4 (local o mediante Cloudflare Tunnel).
"""

import sys
import time
import requests
import json

# URL por defecto o tomada del primer argumento CLI
SERVER_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:11434"

# Normalizar URL
if not SERVER_URL.startswith("http"):
    SERVER_URL = f"https://{SERVER_URL}"
SERVER_URL = SERVER_URL.rstrip("/")

API_URL = f"{SERVER_URL}/v1/chat/completions"

print(f"\n[1/3] Probando conexión contra: {SERVER_URL}")

payload = {
    "model": "gemma4:e4b",
    "messages": [
        {"role": "system", "content": "Eres un asistente conciso."},
        {"role": "user", "content": "Hola! Di 'Listo para la hackathon' y genera 3 ideas de proyectos open source en 2 lineas cada una."}
    ],
    "stream": True,
    "temperature": 0.2
}

start_time = time.time()
first_token_time = None
token_count = 0

print(f"[2/3] Solicitando inferencia con modelo 'gemma4:e4b'...")

try:
    response = requests.post(API_URL, json=payload, stream=True, timeout=120)
    response.raise_for_status()

    print("[3/3] Respuesta en tiempo real:\n" + "-"*50)
    
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith("data: "):
                data_str = decoded_line[6:]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data["choices"][0].get("delta", {}).get("content", "")
                    if delta:
                        if first_token_time is None:
                            first_token_time = time.time()
                        print(delta, end="", flush=True)
                        token_count += 1
                except Exception:
                    pass

    total_time = time.time() - start_time
    ttft = (first_token_time - start_time) if first_token_time else total_time
    tps = token_count / (total_time - ttft) if (total_time - ttft) > 0 else 0

    print("\n" + "-"*50)
    print(" Metricas de Rendimiento:")
    print(f"  • Tiempo al primer token (TTFT): {ttft:.2f} s")
    print(f"  • Tiempo total: {total_time:.2f} s")
    print(f"  • Tokens generados: {token_count}")
    print(f"  • Velocidad aproximada: {tps:.1f} tokens/segundo")
    print(" Conexión verificada con éxito!\n")

except requests.exceptions.RequestException as e:
    print(f"\n Error de conexión: {e}")
    print("Tip: Verifica que el servidor esté activo y que el puerto o túnel estén disponibles.")
    sys.exit(1)
