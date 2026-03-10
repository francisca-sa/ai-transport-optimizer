import requests
import time
from config import OPENWEATHER_API_KEY, CLIMA_ADVERSO

def obter_condicao_climatica(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt"
    try:
        response = requests.get(url)
        data = response.json()
        if 'weather' in data:
            return data['weather'][0]['main'].lower()
        if 'rain' in data:
            if data['rain'].get('1h', 0) > 10:
                return 'heavy rain'
    except Exception as e:
        print(f"Erro ao obter clima: {e}")
    return None

def ajustar_grafo_com_clima(G, pos):
    G_ajustado = G.copy()
    cache_condicoes = {}

    for u, v, dados in list(G.edges(data=True)):
        tipo = dados.get('tipo')
        coord_origem = pos[u]
        coord_destino = pos[v]

        clima_origem = cache_condicoes.get(coord_origem)
        clima_destino = cache_condicoes.get(coord_destino)

        if clima_origem is None:
            clima_origem = obter_condicao_climatica(coord_origem[1], coord_origem[0])
            cache_condicoes[coord_origem] = clima_origem
            time.sleep(1)

        if clima_destino is None:
            clima_destino = obter_condicao_climatica(coord_destino[1], coord_destino[0])
            cache_condicoes[coord_destino] = clima_destino
            time.sleep(1)

        clima_afetado_origem = clima_origem in CLIMA_ADVERSO
        clima_afetado_destino = clima_destino in CLIMA_ADVERSO
        clima_afetado = clima_afetado_origem or clima_afetado_destino

        if not clima_afetado:
            continue

        if 'tempo_original' not in G_ajustado[u][v]:
            G_ajustado[u][v]['tempo_original'] = dados['tempo']

        intensidade_origem = CLIMA_ADVERSO.get(clima_origem, {}).get('intensidade', 'leve')
        intensidade_destino = CLIMA_ADVERSO.get(clima_destino, {}).get('intensidade', 'leve')
        intensidade = max(intensidade_origem, intensidade_destino)

        if tipo == 'caminhada':
            if intensidade == 'moderada':
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 2.0)
            elif intensidade == 'forte':
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 3.0)
            else:
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 4.0)
        
        elif tipo in ['táxi', 'autocarro', 'autocarro interurbano']:
            if intensidade == 'moderada':
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 1.3)
            elif intensidade == 'forte':
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 1.7)
            else:
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 2.5)
        
        elif tipo in ['metro', 'comboio']:
            if intensidade == 'extrema':
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 1.4)
        
        elif tipo == 'avião':
            if clima_origem == 'thunderstorm' or clima_destino == 'thunderstorm':
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 1.8)
            elif clima_origem == 'fog' or clima_destino == 'fog':
                G_ajustado[u][v]['tempo'] = round(dados['tempo'] * 1.2)

    return G_ajustado
