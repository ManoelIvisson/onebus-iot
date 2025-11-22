import network
import urequests
import time
import machine
from machine import Timer, Pin, UART
from conversor_nmea import ConversorNmea
import utime
import ujson as json


# Wi-Fi
SSID = 'Roteador'
PASSWORD = 'onebusv1'

conectando = False
mac_str = ''

# Servidor Flask
URL = 'https://onebus-backend.onrender.com/coordenada-viagem/create'

# GPS
conversor = ConversorNmea()
gps = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
ultima_gprmc = None
buffer_serial = b""

# LEDs
LED_VERMELHO = Pin(13, Pin.OUT)
LED_VERDE = Pin(11, Pin.OUT)

# Temporizadores
temporizador_coleta_dados = Timer()
temporizador_envio_dados = Timer()
temporizador_verifica_conexao = Timer()

def conectar_wifi():
  global mac_str
  
  wlan = network.WLAN(network.STA_IF)
  wlan.active(False)
  wlan.active(True)
  LED_VERMELHO.value(1)
  
  # obtém o endereço MAC (bytes)
  mac = wlan.config('mac')

  # exibe o MAC formatado
  mac_str = ':'.join(['{:02X}'.format(b) for b in mac])
  
  print('Conectando na rede...')
  if not wlan.isconnected():
      wlan.connect(SSID, PASSWORD)
      
      tempo_inicial = time.time()
      while not wlan.isconnected():
          if time.time() - tempo_inicial > 30:
              print("Tentando conexo novamente...")
              break
          time.sleep(1)
          print(".")
  LED_VERMELHO.value(0)
  LED_VERDE.value(1)
  print('configurao da rede: ', wlan.ifconfig())
  
    
def ler_gps_continuamente(timer):
  global ultima_gprmc, buffer_serial
  dados = gps.read()
  
  if dados:
    buffer_serial += dados
  
  while b"\n" in buffer_serial:
    linha, buffer_serial = buffer_serial.split(b"\n", 1)
    linha = linha.strip()
  
    try:
      texto = linha.decode('utf-8').strip()
      for s in texto.split("$"):
        s = s.strip()
        if s.startswith('GPRMC') and "W" in s:
          ultima_gprmc = "$" + s  
    except Exception as e:
        print("Erro ao decodificar: ", e)
    
def enviar_dados(timer):
  global ultima_gprmc, mac_str
  print(ultima_gprmc)
  if ultima_gprmc is not None:
    dados = conversor.converter_gprmc(ultima_gprmc)
    if dados is not None:
      dados_json = {
        "mac": mac_str,
        "latitude": dados["latitude"],
        "longitude": dados["longitude"],
        "criado_em": dados["criado_em"]
      }
    try:
      res = urequests.post(URL, headers = {'content-type': 'application/json'}, data = json.dumps(dados_json))
      print("Enviando...", res)
      if res is None:
        return None
      
      dados = res.json()
      res.close()
    except Exception as e:
      print(e)
  else:
    print("Sem dados validos para envio")
    

if __name__ == "__main__":
    temporizador_coleta_dados.init(freq=1, mode=Timer.PERIODIC, callback=ler_gps_continuamente)
    temporizador_envio_dados.init(period=10000, mode=Timer.PERIODIC, callback=enviar_dados)
    conectar_wifi()
    
    while True:
        utime.sleep(1)
