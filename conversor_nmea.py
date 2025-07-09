class ConversorNmea:
    
    def converter_gprmc(self, sentenca: str):
        """
        Função que converte sentenças NMEA GPRMC para JSON
        """

        sentenca_separada = sentenca.replace(" ", "").split(',')

        try:
            latitude = sentenca_separada[3]
            direcao_latitude = sentenca_separada[4]

            graus_latitude = int(latitude[0:2])
            minutos_latitude = float(latitude[2:])/60

            longitude = sentenca_separada[5]
            direcao_longitude = sentenca_separada[6]

            graus_longitude = int(longitude[0:3])
            minutos_longitude = float(longitude[3:])/60
            
            if direcao_latitude == "S":
                latitude = (graus_latitude + minutos_latitude) * -1
            else:
                latitude = graus_latitude + minutos_latitude

            if direcao_longitude == "W":
                longitude = (graus_longitude + minutos_longitude) * -1
            else:
                longitude = graus_longitude + minutos_longitude
        except (IndexError, ValueError) as e:
            print(f'Erro ao processar sentença GPRMC: {e}')
            return None

        return {
            "latitude": round(latitude, 6),
            "longitude": round(longitude, 6)
        }
