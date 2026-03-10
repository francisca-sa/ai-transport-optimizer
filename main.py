from grafo import carregar_grafo, desenhar_grafo
from clima import ajustar_grafo_com_clima
from procuras import obter_top_caminhos_por_custo, calcular_custo_total, obter_caminhos
from tempo import converter_hora_para_minutos, calcular_tempo_total, formatar_minutos_para_hhmm
from combustivel import verificar_reabastecimento_etapa

def main():
    G, pos = carregar_grafo("ligacoes.csv")
    G = ajustar_grafo_com_clima(G, pos)
    desenhar_grafo(G, pos)

    print("\n=== Escolha do Método de Procura ===")
    usar_algoritmo = input("Deseja escolher um algoritmo específico? (s/n): ").strip().lower()
    
    algoritmo = None
    if usar_algoritmo == 's':
        print("\nAlgoritmos disponíveis:")
        print("1. BFS (Procura em Largura)")
        print("2. DFS (Procura em Profundidade)")
        print("3. Custo Uniforme")
        print("4. A* (Custo + Heurística Geográfica)")
        print("5. Greedy (Heurística Geográfica Pura)")
        opcao = input("Escolha o número do algoritmo: ").strip()

        if opcao == '1':
            algoritmo = 'bfs'
        elif opcao == '2':
            algoritmo = 'dfs'
        elif opcao == '3':
            algoritmo = 'ucs'
        elif opcao == '4':
            algoritmo = 'a_star'
        elif opcao == '5':
            algoritmo = 'greedy'
        else:
            print("Opção inválida. A usar procura padrão.")

    num_passageiros = int(input("\nQuantos adeptos vão viajar? "))
    origem = input("Estádio de origem: ").strip()
    destino = input("Estádio de destino: ").strip()
    
    horario_chegada = None
    if input("Tem um horário de chegada específico? (s/n): ").strip().lower() == "s":
        horario_chegada = converter_hora_para_minutos(input("Horário de chegada (HH:MM): "))
    
    horario_partida = None
    if input("Tem um horário de partida específico? (s/n): ").strip().lower() == "s":
        horario_partida = converter_hora_para_minutos(input("Horário de partida (HH:MM): "))
    
    tempo_limite = None
    if horario_chegada and horario_partida:
        if horario_chegada >= horario_partida:
            tempo_limite = horario_chegada - horario_partida
        else:
            tempo_limite = (horario_chegada + 1440) - horario_partida
    
    if not horario_chegada or horario_partida:
        if input("Deseja definir um tempo máximo de viagem? (s/n): ").strip().lower() == "s":
            tempo_max_str = input("Tempo máximo de viagem (HH:MM): ").strip()
            tempo_limite = converter_hora_para_minutos(tempo_max_str)
    
    if algoritmo:
        print(f"\nA usar algoritmo: {algoritmo.upper()}")
        caminhos = obter_caminhos(G, origem, destino, num_passageiros, pos, algoritmo, tempo_limite)
    else:
        print("\nA usar busca padrão (melhor relação custo-tempo)")
        caminhos = obter_top_caminhos_por_custo(G, origem, destino, num_passageiros, num_caminhos=10)

    caminho_valido = None
    etapas = []
    excedeu_tempo = False

    if algoritmo:
        if caminhos:
            caminho_valido = caminhos[0]
            partida = horario_partida if horario_partida is not None else 0
            tempo_total, etapas = calcular_tempo_total(G, caminho_valido, partida)
            if tempo_limite is not None and tempo_total > tempo_limite:
                excedeu_tempo = True
    else:
        for caminho in caminhos:
            partida = horario_partida if horario_partida is not None else 0
            tempo_total, etapas_candidato = calcular_tempo_total(G, caminho, partida)
            
            if (tempo_limite is None) or (tempo_total <= tempo_limite):
                caminho_valido = caminho
                etapas = etapas_candidato
                break
    
    if caminho_valido:
        custo_total, custos_etapas = calcular_custo_total(G, caminho_valido, num_passageiros)
        custo_por_pessoa = custo_total / num_passageiros 
        
        print("\n--- CAMINHO ENCONTRADO ---")
        if excedeu_tempo:
            print("AVISO: O caminho encontrado excede o tempo limite definido!")
        print(f"Custo total para {num_passageiros} passageiros: €{custo_total:.2f}")
        print(f"Custo por pessoa: €{custo_por_pessoa:.2f}")
        print(f"Tempo total: {formatar_minutos_para_hhmm(tempo_total, limitar_24h=False)}")

        print("\nDetalhes do percurso:")
        for i, etapa in enumerate(etapas, 1):
            u = etapa['origem']
            v = etapa['destino']
            dados = G[u][v]
            
            transporte = dados['tipo']
            capacidade = dados.get('capacidade')
            distancia_km = dados.get('distancia_km', 0)
            custo_etapa_por_pessoa = custos_etapas[i-1]
            
            print(f"\n{i}. De {u} para {v} via {transporte}")
            print(f"   - Partida: {etapa['partida']}h | Chegada: {etapa['chegada']}h")
            print(f"   - Duração: {formatar_minutos_para_hhmm(etapa['duracao'], limitar_24h=False)}h | Distância aproximada: {distancia_km:.1f} km")
            print(f"   - Custo por pessoa nesta etapa: €{custo_etapa_por_pessoa:.2f}")

            if capacidade is not None and capacidade < num_passageiros:
                viagens = (num_passageiros + capacidade - 1) // capacidade
                print(f"AVISO: Capacidade máxima: {capacidade} passageiros")
                print(f"       Necessárias {viagens} viagens")

            if transporte in ['Taxi', 'Autocarro Interurbano']:
                pontos = verificar_reabastecimento_etapa(distancia_km, transporte)
                if pontos:
                    pontos_str = ", ".join([f"{p:.1f} km" for p in pontos])
                    print(f"AVISO: Reabastecimento do veículo necessário após aproximadamente {pontos_str} de viagem.")
                else:
                    print(f"Informação: Combustível suficiente")
    else:
        print("\nAVISO: Nenhum caminho encontrado dentro das restrições.")

if __name__ == "__main__":
    main()