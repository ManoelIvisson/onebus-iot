import network
import urequests
import time
import machine
from machine import Timer, Pin
from conversor_nmea import ConversorNmea

# Wi-Fi
#SSID = 'Minha Rede'
#PASSWORD = 'cim034gio'

# Wi-Fi
SSID = 'Redmi 9A'
PASSWORD = 'manoelivisson'

# Servidor Flask
FLASK_SERVER_IP = '192.168.3.10' # e.g., '192.168.1.100'
FLASK_SERVER_PORT = 5000
FLASK_ENDPOINT = '/onebus'

# GPS
conversor = ConversorNmea()
sentenca_mock = '$GPRMC,081836,A,0615.00,S,03630.00,W,000.0,360.0,080725,011.3,E*25'

# LEDs
LED_VERMELHO = Pin(13, Pin.OUT)
LED_VERDE = Pin(11, Pin.OUT)

# Temporizador
temporizador = Timer(0)

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    LED_VERMELHO.value(1)
    
    if not wlan.isconnected():
        print('Conectando na rede...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print(".")
    LED_VERMELHO.value(0)
    LED_VERDE.value(1)
    print('configurao da rede: ', wlan.ifconfig())
    
def enviar_dados(timer):
  # request = urequests.post(f"http://{FLASK_SERVER_IP}:{FLASK_SERVER_PORT}{FLASK_ENDPOINT}")
  print("Enviando...")
    
if __name__ == "__main__":
    conectar_wifi()
    print(conversor.converter_gprmc(sentenca_mock))
