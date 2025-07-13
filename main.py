import network
import urequests
import time
import machine
from machine import Timer, Pin
from conversor_nmea import ConversorNmea
import utime
import ujson as json

# Wi-Fi
#SSID = 'Minha Rede'
#PASSWORD = 'cim034gio'

# Wi-Fi
SSID = 'Redmi 9A'
PASSWORD = 'manoelivisson'

# Servidor Flask
FLASK_SERVER_IP = '192.168.3.145' # e.g., '192.168.1.100'
FLASK_SERVER_PORT = 5000
FLASK_ENDPOINT = '/data'

# GPS
conversor = ConversorNmea()
gps = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# LEDs
LED_VERMELHO = Pin(13, Pin.OUT)
LED_VERDE = Pin(11, Pin.OUT)

# Temporizador
temporizador = Timer()


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
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
  dados_json = json.dumps(conversor.converter_gprmc(sentenca_mock))
  print(gps)
  print(gps.readline())
  print("Enviando...")
    
if __name__ == "__main__":
    conectar_wifi()
    print(conversor.converter_gprmc(sentenca_mock))
    temporizador.init(period=10000, mode=Timer.PERIODIC, callback=enviar_dados)

    while True:
        utime.sleep(1)
