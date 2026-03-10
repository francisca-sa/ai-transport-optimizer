from flask import Flask, render_template, request, jsonify
from grafo import carregar_grafo
from tempo import converter_hora_para_minutos, formatar_minutos_para_hhmm
from procuras import obter_top_caminhos_por_custo, calcular_custo_total, obter_caminhos
from clima import ajustar_grafo_com_clima
from tempo import calcular_tempo_total
from combustivel import verificar_reabastecimento_etapa 

app = Flask(__name__)
G, pos = carregar_grafo("ligacoes.csv")
G = ajustar_grafo_com_clima(G, pos)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular_rota', methods=['POST'])
def calcular_rota():
    dados = request.json
    resultado = calcular_rota_logicista(
        G, 
        pos,
        dados['origem'],
        dados['destino'],
        int(dados['passageiros']),
        horario_partida=converter_hora_para_minutos(dados.get('horario_partida')) if dados.get('horario_partida') else None,
        horario_chegada=converter_hora_para_minutos(dados.get('horario_chegada')) if dados.get('horario_chegada') else None,
        tempo_maximo=converter_hora_para_minutos(dados.get('tempo_maximo')) if dados.get('tempo_maximo') else None,
        algoritmo=dados.get('algoritmo')
    )
    return jsonify(resultado)

def calcular_rota_logicista(G, pos, origem, destino, num_passageiros, horario_partida=None, horario_chegada=None, tempo_maximo=None, algoritmo=None):
    try:
        caminhos = obter_top_caminhos_por_custo(G, origem, destino, num_passageiros, 10)
        tempo_limite = None

        if horario_chegada and horario_partida:
            tempo_limite = horario_chegada - horario_partida
            if tempo_limite < 0: tempo_limite += 1440
        elif tempo_maximo:
            tempo_limite = tempo_maximo

        if algoritmo:
            caminhos = obter_caminhos(G, origem, destino, num_passageiros, pos, algoritmo, tempo_limite)
        else:
            caminhos = obter_top_caminhos_por_custo(G, origem, destino, num_passageiros, 10)

        for caminho in caminhos:
            tempo_total, etapas = calcular_tempo_total(G, caminho, horario_partida or 0)
            
            if tempo_limite and tempo_total > tempo_limite:
                continue

            custo_total, custos_etapas = calcular_custo_total(G, caminho, num_passageiros)
            
            detalhes_etapas = []
            excedeu_capacidade = False
            for i, etapa in enumerate(etapas):
                dados = G[etapa['origem']][etapa['destino']]
                capacidade = dados.get('capacidade')
                if capacidade and num_passageiros > capacidade:
                    excedeu_capacidade = True
                pontos_reabastecimento = verificar_reabastecimento_etapa(
                    dados.get('distancia_km', 0),
                    dados['tipo']
                )
                detalhes_etapas.append({
                    'etapa': i+1,
                    'origem': etapa['origem'],
                    'destino': etapa['destino'],
                    'transporte': dados['tipo'],
                    'partida': etapa['partida'],
                    'chegada': etapa['chegada'],
                    'duracao': formatar_minutos_para_hhmm(etapa['duracao'], False),
                    'custo_por_pessoa': custos_etapas[i],
                    'capacidade': capacidade,
                    'num_passageiros': num_passageiros,
                    'pontos_reabastecimento': pontos_reabastecimento
                })
                coordenadas_rota = []
                for node in caminho:
                    if node in pos:
                        coord = {'lat': pos[node][1], 'lon': pos[node][0]}
                        coordenadas_rota.append(coord)
            
            return {
                'custo_total': custo_total,
                'custo_por_pessoa': custo_total / num_passageiros,
                'duracao_total': formatar_minutos_para_hhmm(tempo_total, False),
                'etapas': detalhes_etapas,
                'coordenadas': coordenadas_rota,
                'origem_coord': {'lat': pos[origem][1], 'lon': pos[origem][0]},
                'destino_coord': {'lat': pos[destino][1], 'lon': pos[destino][0]},
                'excedeu_capacidade': excedeu_capacidade
            }
            
        return {'erro': 'Nenhum caminho válido encontrado'}
        
    except Exception as e:
        return {'erro': str(e)}

if __name__ == '__main__':
    app.run(debug=True)