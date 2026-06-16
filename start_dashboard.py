import httpx
import asyncio
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- КОНФИГУРАЦИЯ ---
REMNA_API_URL = "https://your-remnawave-instance.com"
REMNA_TOKEN = "YOUR_REMN_API_TOKEN"
HEADERS = {"Authorization": f"Bearer {REMNA_TOKEN}"}
ONLINE_THRESHOLD_SEC = 30  # Жесткий порог по твоему запросу

async def fetch_data():
    async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=10.0) as client:
        nodes_task = client.get(f"{REMNA_API_URL}/api/nodes")
        users_task = client.get(f"{REMNA_API_URL}/api/users")
        
        nodes_resp, users_resp = await asyncio.gather(nodes_task, users_task)
        
        if nodes_resp.status_code != 200 or users_resp.status_code != 200:
            return {"nodes": [], "online_users": [], "global_stats": {}, "error": "API Error"}

        nodes_raw = nodes_resp.json().get('response', [])
        users_raw = users_resp.json().get('response', {}).get('users', [])

        # 1. Обрабатываем ТОЛЬКО онлайн-ноды
        active_nodes = []
        total_online_from_nodes = 0
        
        for n in nodes_raw:
            if n.get('isDisabled') or not n.get('isConnected'):
                continue
                
            sys_data = n.get('system') or {}
            sys_info = sys_data.get('info') or {}
            sys_stats = sys_data.get('stats') or {}
            
            mem_total = sys_info.get('memoryTotal', 0)
            mem_used = sys_stats.get('memoryUsed', 0)
            load_avg = sys_stats.get('loadAvg', [0, 0, 0])
            users_online = n.get('usersOnline', 0)
            
            total_online_from_nodes += users_online
            
            active_nodes.append({
                "uuid": n['uuid'],
                "name": n['name'],
                "address": n.get('address', 'N/A'),
                "cpu_model": sys_info.get('cpuModel', 'Unknown'),
                "ram_percent": round((mem_used / mem_total * 100), 1) if mem_total else 0,
                "ram_used_mb": round(mem_used / 1024 / 1024, 1),
                "ram_total_mb": round(mem_total / 1024 / 1024, 1),
                "load_1m": load_avg[0] if len(load_avg) > 0 else 0,
                "traffic_gb": round(n.get('trafficUsedBytes', 0) / 1024**3, 2),
                "users_online": users_online  # Достоверный счетчик от ядра
            })

        # 2. Эмуляция списка "Онлайн" по порогу 30 секунд
        now_utc = datetime.now(timezone.utc)
        online_users_list = []
        
        for u in users_raw:
            traffic = u.get('userTraffic') or {}
            online_at_str = traffic.get('onlineAt')
            
            if not online_at_str:
                continue
                
            try:
                # Парсинг ISO формата с миллисекундами
                online_at = datetime.fromisoformat(online_at_str.replace('Z', '+00:00'))
                diff_sec = (now_utc - online_at).total_seconds()
                
                if diff_sec <= ONLINE_THRESHOLD_SEC:
                    node_uuid = traffic.get('lastConnectedNodeUuid')
                    node_name = next((n['name'] for n in active_nodes if n['uuid'] == node_uuid), "Unknown")
                    
                    online_users_list.append({
                        "username": u['username'],
                        "node_name": node_name,
                        "seconds_ago": int(diff_sec)
                    })
            except (ValueError, TypeError):
                continue

        return {
            "nodes": active_nodes,
            "online_users": online_users_list,  # Список по фильтру <30с
            "global_stats": {
                "total_nodes_up": len(active_nodes),
                "real_online_total": total_online_from_nodes  # Реальный онлайн от ядер
            },
            "error": None
        }

@app.get("/")
async def read_root():
    try:
        with open("END.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>END.html not found</h1>", status_code=500)

@app.get("/api/dashboard-data")
async def get_dashboard_data():
    return await fetch_data()

@app.get("/api/weather")
async def get_weather(lat: float = 55.0415, lon: float = 82.9346, tz: str = "Asia/Novosibirsk"):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&wind_speed_unit=ms&timezone={tz}"
        async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
            r = await client.get(url)
            if r.status_code == 200:
                return r.json()
    except Exception as e:
        return {"error": f"Backend fetch failed: {str(e)}"}
    return {"error": "Failed to fetch weather"}

if __name__ == "__main__":
    import uvicorn
    print("Запуск дашборда... http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)