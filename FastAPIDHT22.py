# Librerías a instalar
# pip install fastapi uvicorn[standard] pymodbus==3.11.4

# librerías
import asyncio # para usar el comando delay
from pymodbus.client import ModbusTcpClient # protoclo modbus
from fastapi import FastAPI, WebSocket #Para montar el servidor
from fastapi.responses import HTMLResponse #Respuesta de parte del seridor
#Datos para la conexion
IP = "192.168.1.117"
PORT = 502

#Definición de registros
REG_TEMP = 0
REG_HUM = 1

app = FastAPI()

HTML = """
<!doctype_html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Adquisición de datos DHT22</title>
    <style>
        body {font-family: Arial; margin: 40px;}
        .card {padding: 20px; border; 1px solid #ccc; border-radius: 12px; width: 300px}
        .value {font-size: 2rem; margin: 10px 0;}
    </style>
</head>
<body>
    <h2>Monitoreo DHT22</h2>
    <div class="card">
        <div id="temp" class="value"> Temperatura: -- </div>
        <div id="hum" class="value"> Humedad: -- </div>
    </div>
    <script>
        let ws = new WebSocket("ws://"  + location.host + "/ws");

        ws.onmessage = function(event){
            let data =  JSON.parse(event.data)
            document.getElementById("temp").innerHTML = "Temperatura: " + data.temp.toFixed(2);
            document.getElementById("hum").innerHTML = "Humedad: " + data.hum.toFixed(2)
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

    client = ModbusTcpClient(IP, port=PORT)

    if not client.connect():
        print("Conexion con el ESP32 no establecida")
        await ws.send_json({"temp": 0, "hum": 0})
        await ws.close()
        return

    print("Conexión establecida. Leyendo cada 5 segundos \n")

    try:
        while True:
            rr = client.read_holding_registers(REG_TEMP, count=2, device_id=1)

            if rr.isError():
                print("Error en la lectura")
            else:
                temp = rr.registers[0]
                hum = rr.registers[1]
                print(f"Temperatura: {temp/100.0:.2f} | Humedad: {hum/100.0:.2f}")
                await ws.send_json({"temp": temp/100.0, "hum":hum/100.0})
            await asyncio.sleep(2)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        await ws.close()
        print("Conexción cerrada")
        print("Programa finalizado")