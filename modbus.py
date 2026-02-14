import time
from pymodbus.client import ModbusTcpClient

ESP32_IP = "192.168.1.117"   # <- IP real del ESP32
PORT = 502

REG_TEMP = 0
REG_HUM = 1

def main():
    client = ModbusTcpClient(host=ESP32_IP, port=PORT)

    if not client.connect():
        print("No se pudo conectar al ESP32 (Modbus TCP).")
        return

    print("Conectado. Leyendo cada 5 segundos...\n")

    try:
        while True:
            rr = client.read_holding_registers(REG_TEMP, count=2, device_id=1)

            if rr.isError():
                print("Error en lectura:", rr)
            else:
                temp100 = rr.registers[0]
                hum100  = rr.registers[1]
                print(f"Temp: {temp100/100.0:.2f} °C | Hum: {hum100/100.0:.2f} %")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nSaliendo...")
    finally:
        client.close()

if __name__ == "__main__":
    main()