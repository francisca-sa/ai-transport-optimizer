from datetime import datetime

def converter_hora_para_minutos(hora_str):
    try:
        horas, minutos = map(int, hora_str.split(':'))
        return horas * 60 + minutos
    except (ValueError, AttributeError):
        return 0

def formatar_minutos_para_hhmm(minutos, limitar_24h=True):
    horas_total = minutos // 60
    minutos_total = minutos % 60
    
    if limitar_24h:
        horas = horas_total % 24
    else:
        horas = horas_total
    
    return f"{horas:02d}:{minutos_total:02d}"


def calcular_espera(tempo_atual, intervalo_minutos, primeira_partida_hora, ultima_partida_hora):
    primeira_min = converter_hora_para_minutos(primeira_partida_hora)
    ultima_min = converter_hora_para_minutos(ultima_partida_hora)
    
    if not intervalo_minutos:
        return 0
    
    if intervalo_minutos == "[1 por dia]":
        if tempo_atual <= primeira_min:
            return primeira_min - tempo_atual
        else:
            return (1440 - tempo_atual) + primeira_min
    
    intervalo_num = int(intervalo_minutos)
    
    if tempo_atual < primeira_min:
        return primeira_min - tempo_atual
    elif tempo_atual > ultima_min:
        return (1440 - tempo_atual) + primeira_min

    tempo_relativo = tempo_atual - primeira_min
    espera = intervalo_num - (tempo_relativo % intervalo_num)
    
    return espera if espera != intervalo_num else 0


def calcular_tempo_total(G, caminho, horario_inicio):
    tempo_atual = horario_inicio
    etapas = []
    start_time = None

    if horario_inicio == 0 and len(caminho) >= 2:
        primeira_origem = caminho[0]
        primeira_destino = caminho[1]
        dados_primeira_etapa = G[primeira_origem][primeira_destino]
        
        primeira_partida_str = dados_primeira_etapa.get('primeira_partida_hora', '00:00')
        primeira_partida_min = converter_hora_para_minutos(primeira_partida_str)
        
        espera_inicial = primeira_partida_min - tempo_atual
        if espera_inicial < 0:
            espera_inicial += 1440
        
        tempo_atual += espera_inicial

    start_time = tempo_atual

    for i in range(len(caminho) - 1):
        u, v = caminho[i], caminho[i+1]
        dados = G[u][v]

        if i > 0:
            espera = calcular_espera(
                tempo_atual % 1440,
                dados.get('intervalo_minutos'),
                dados.get('primeira_partida_hora'),
                dados.get('ultima_partida_hora')
            )
            tempo_atual += espera

        tempo_viagem = dados.get('tempo', 0)
        partida_min = tempo_atual
        tempo_atual += tempo_viagem

        etapas.append({
            'origem': u,
            'destino': v,
            'partida': formatar_minutos_para_hhmm(partida_min),
            'chegada': formatar_minutos_para_hhmm(tempo_atual),
            'duracao': tempo_viagem
        })

    duracao_total = tempo_atual - start_time
    return duracao_total, etapas
