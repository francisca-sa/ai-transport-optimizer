import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

CLIMA_ADVERSO = {
    'rain': {'nome': 'Chuva', 'intensidade': 'moderada'},
    'heavy rain': {'nome': 'Chuva intensa', 'intensidade': 'forte'},
    'snow': {'nome': 'Neve', 'intensidade': 'forte'},
    'sleet': {'nome': 'Aguaceiros', 'intensidade': 'moderada'},
    'thunderstorm': {'nome': 'Tempestade', 'intensidade': 'extrema'},
    'fog': {'nome': 'Nevoeiro', 'intensidade': 'moderada'},
    'hail': {'nome': 'Granizo', 'intensidade': 'extrema'},
    'extreme': {'nome': 'Condições extremas', 'intensidade': 'extrema'}
}

AUTONOMIA_TANQUE = {
    'Taxi': 500,
    'Autocarro Interurbano': 800,
}
