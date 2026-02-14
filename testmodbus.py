from pymodbus.client import ModbusTcpClient
import time

IP = "192.168.1.117"
PORT = "502"
COIL_LED = 0

client = ModbusTcpClient(IP, port=PORT)

if not client.connect():
    print("No hay conexión")
    exit()

print("Conexión establecida")

try:
    while True:
        opcion = input("1 para encender | 0 para apagar | q para salir")
        if opcion.lower() == "q":
            break
        
        if opcion not in ["0","1"]:
            print("No ingresaste una opción valida")
            continue

        valor = bool(int(opcion))
        client.write_coil(COIL_LED, valor)

        estado = "Encendido" if valor else "Apagado"
        print(f"El estado es {estado}")

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    client.close()
    print("Programa finalizado")