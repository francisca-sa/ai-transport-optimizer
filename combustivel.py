from config import AUTONOMIA_TANQUE
from math import radians, sin, cos, sqrt, atan2

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def verificar_reabastecimento_etapa(distancia_etapa_km, tipo_transporte):
    autonomia = AUTONOMIA_TANQUE.get(tipo_transporte, float('inf'))
    
    if autonomia == float('inf') or distancia_etapa_km <= autonomia:
        return []
    
    pontos = []
    distancia_acumulada = autonomia
    while distancia_acumulada < distancia_etapa_km:
        pontos.append(distancia_acumulada)
        distancia_acumulada += autonomia
    
    return pontos