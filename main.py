from conversor_nmea import ConversorNmea

conversor = ConversorNmea()

print(conversor.converter_gprmc("$GPRMC,081836.500,A,0625.0000,S,03630.0000,W,0.00,0.00,090725,,,A*6C"))