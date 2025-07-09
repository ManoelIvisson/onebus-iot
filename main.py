from conversor_nmea import ConversorNmea

conversor = ConversorNmea()

print(conversor.converter_gprmc("$GPRMC,081836,A,0615.00,S,03630.00,W,012.5,270.0,080725,011.3,E*hh"))