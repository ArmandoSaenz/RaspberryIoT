import RPi.GPIO as GPIO
import time

ENA = 12    
IN1 = 16    
IN2 = 20    

GPIO.setmode(GPIO.BCM)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

GPIO.output(ENA, GPIO.HIGH)


pwm = GPIO.PWM(IN1, 1000)
pwm.start(0)

print("Control de potencia del motor DC")
print("Ctrl + C para salir\n")

try:
    while True:
        entrada = input("Potencia (0-100): ")

        if not entrada.isdigit():
            print("Error: solo se permiten valores enteros")
            continue

        potencia = int(entrada)

        if 0 <= potencia <= 100:
            pwm.ChangeDutyCycle(potencia)

            if potencia == 0:
                print("Motor detenido")
            else:
                print(f"Potencia aplicada: {potencia}%")
        else:
            print("Error: el valor debe estar entre 0 y 100")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nPrograma finalizado por el usuario")

finally:
    pwm.stop()
    GPIO.output(ENA, GPIO.LOW)  # Deshabilitar puente H
    GPIO.cleanup()
    print("GPIO liberados correctamente")