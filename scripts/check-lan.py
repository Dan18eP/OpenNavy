#!/usr/bin/env python3
"""
OpenNavy LAN Diagnostic Tool
Verifies HTTP REST and WebSocket connectivity to the host machine for team members.
Usage:
    python scripts/check-lan.py http://localhost:8000
    python scripts/check-lan.py http://192.168.1.45:8000
"""

import sys
import time
import json
import urllib.request
import urllib.error


def check_http(base_url: str):
    print(f"[HTTP] Checking connection to {base_url}...")
    status_url = f"{base_url}/api/v1/sonar/status"
    start = time.time()
    try:
        req = urllib.request.Request(status_url, headers={"User-Agent": "OpenNavy-Diagnostic"})
        with urllib.request.urlopen(req, timeout=5) as response:
            latency = (time.time() - start) * 1000
            data = json.loads(response.read().decode())
            print(f"[HTTP OK] Status 200 ({latency:.1f}ms)")
            print(f"          Active officers on host: {data.get('active_officers', 0)}")
            print(f"          Officers list: {data.get('officers', [])}")
            return True
    except urllib.error.URLError as e:
        print(f"[HTTP FAIL] Could not connect to {status_url}: {e.reason}")
        return False
    except Exception as e:
        print(f"[HTTP FAIL] Error checking HTTP endpoint: {e}")
        return False


def check_blueprints(base_url: str):
    print(f"[BLUEPRINTS] Checking latest shared blueprint...")
    url = f"{base_url}/api/v1/sonar/blueprints/latest"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OpenNavy-Diagnostic"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            latest = data.get("latest_blueprint")
            if latest:
                print(f"[BLUEPRINTS OK] Found active blueprint:")
                print(f"                Mission: {latest.get('mission')}")
                print(f"                Officer: {latest.get('officer_name')}")
                print(f"                Waypoints count: {len(latest.get('waypoints', []))}")
            else:
                print("[BLUEPRINTS OK] No active blueprint yet on host (ready for course plotting).")
            return True
    except Exception as e:
        print(f"[BLUEPRINTS FAIL] Could not retrieve blueprints: {e}")
        return False


async def check_websocket_async(base_url: str):
    try:
        import websockets
    except ImportError:
        print("[WS SKIP] websockets library not installed in current environment. Install with: pip install websockets")
        return

    # Convert http:// or https:// to ws:// or wss://
    ws_url = base_url.replace("http://", "ws://").replace("https://", "wss://")
    endpoint = f"{ws_url}/api/v1/sonar/ws/sonar?officer=DiagnosticCadet"
    print(f"[WS] Connecting to WebSocket at {endpoint}...")

    start = time.time()
    try:
        async with websockets.connect(endpoint) as ws:
            connect_time = (time.time() - start) * 1000
            print(f"[WS OK] Connected in {connect_time:.1f}ms")

            # Receive initial message (FLEET_UPDATE)
            initial_msg = await ws.recv()
            data = json.loads(initial_msg)
            print(f"        Initial event received: {data.get('type')}")

            # Send ping
            ping_start = time.time()
            await ws.send(json.dumps({"type": "PING"}))
            pong_msg = await ws.recv()
            pong_data = json.loads(pong_msg)
            pong_time = (time.time() - ping_start) * 1000

            if pong_data.get("type") == "PONG":
                print(f"[WS OK] Ping-Pong roundtrip in {pong_time:.1f}ms")
            else:
                print(f"[WS WARN] Unexpected response to ping: {pong_data}")

            print("[WS OK] WebSocket Fleet Sonar channel verified successfully.")
    except Exception as e:
        print(f"[WS FAIL] WebSocket test failed: {e}")


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    target = target.rstrip("/")

    print("==================================================")
    print("      OpenNavy Fleet Sonar LAN Diagnostic        ")
    print("==================================================")
    print(f"Target Host: {target}\n")

    http_ok = check_http(target)
    if http_ok:
        check_blueprints(target)
        try:
            import asyncio
            asyncio.run(check_websocket_async(target))
        except Exception as e:
            print(f"[WS FAIL] {e}")

    print("\n==================================================")
    print("Diagnostic complete.")


if __name__ == "__main__":
    main()
