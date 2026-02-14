import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pymodbus.client import ModbusTcpClient

ESP32_IP = "192.168.1.117"   # <-- Cambiar por IP real
PORT = 502

REG_TEMP = 0
REG_HUM = 1

app = FastAPI()

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Monitor DHT22</title>
  <style>
    body { font-family: Arial; margin: 40px; }
    .card { padding: 20px; border: 1px solid #ccc; border-radius: 12px; width: 320px;}
    .value { font-size: 2rem; margin: 10px 0;}
  </style>
</head>
<body>
  <h2>Monitoreo DHT22</h2>
  <div class="card">
    <div id="temp" class="value">Temp: --</div>
    <div id="hum" class="value">Hum: --</div>
  </div>

<script>
  let ws = new WebSocket("ws://" + location.host + "/ws");

  ws.onmessage = function(event) {
    let data = JSON.parse(event.data);
    document.getElementById("temp").innerHTML = "Temp: " + data.temp.toFixed(2) + " °C";
    document.getElementById("hum").innerHTML  = "Hum: " + data.hum.toFixed(2) + " %";
  };
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return HTMLResponse(HTML)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    client = ModbusTcpClient(host=ESP32_IP, port=PORT)

    if not client.connect():
        await ws.send_json({"temp": 0, "hum": 0})
        await ws.close()
        return

    try:
        while True:
            # 🔹 AJUSTE IMPORTANTE PARA PYMODBUS 3.11.4
            rr = client.read_holding_registers(
                REG_TEMP,
                count=2,
                device_id=1
            )

            if not rr.isError():
                temp = rr.registers[0] / 100.0
                hum  = rr.registers[1] / 100.0

                await ws.send_json({
                    "temp": temp,
                    "hum": hum
                })

            await asyncio.sleep(1)

    except Exception as e:
        print("Error WebSocket:", e)

    finally:
        client.close()
        await ws.close()