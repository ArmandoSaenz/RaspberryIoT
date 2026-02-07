import RPi.GPIO as GPIO
import time

ENA = 12      
IN1 = 16     
IN2 = 20     

GPIO.setmode(GPIO.BCM)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)

pwm = GPIO.PWM(ENA, 1000)  # 1 kHz
pwm.start(0)

try:
    while True:
        sentido = input("Sentido (A/B): ").strip().upper()

        if sentido not in ["A", "B"]:
            print("Error: sentido inválido. Use A o B.")
            continue

        entrada = input("Potencia (0-100): ")

        if not entrada.isdigit():
            print("Error: la potencia debe ser un número entero")
            continue

        potencia = int(entrada)

        if not 0 <= potencia <= 100:
            print("Error: la potencia debe estar entre 0 y 100")
            continue

        if potencia == 0:
            print("Motor detenido")
        elif sentido == "A":
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            pwm.ChangeDutyCycle(potencia)
            print(f"Giro en sentido A con potencia {potencia}%")
        else:
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            pwm.ChangeDutyCycle(potencia)
            print(f"Giro en sentido B con potencia {potencia}%")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nPrograma finalizado por el usuario")

finally:
    pwm.stop()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO liberados correctamente")