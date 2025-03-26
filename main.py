import matplotlib.pyplot as plt

# Parâmetros do gerador de números pseudoaleatórios
a = 1664525
c = 1013904223
M = 2**32
previous_seed = 123456789  # Seed inicial

# Variáveis globais para a simulação
tempo_global = 0.0
fila = 0
max_fila = 0
tempos_estado = []
eventos = []
count = 100000  # Número de aleatórios a usar
clientes_perdidos = 0
clientes_atendidos = 0
clientes_chegaram = 0

def next_random():
    """Gera um número pseudoaleatório entre 0 e 1"""
    global previous_seed, count
    previous_seed = (a * previous_seed + c) % M
    count -= 1
    return previous_seed / M

def schedule_event(tipo, tempo):
    """Agenda um novo evento"""
    eventos.append((tempo, tipo))
    eventos.sort(key=lambda x: x[0])

def uniforme(a, b):
    """Gera um número uniformemente distribuído entre a e b"""
    return a + (b - a) * next_random()

def chegada(servidores, capacidade):
    """Processa um evento de chegada"""
    global fila, tempo_global, max_fila, clientes_perdidos, clientes_chegaram
    
    clientes_chegaram += 1
    
    # Atualiza tempo acumulado para o estado atual
    if fila >= len(tempos_estado):
        tempos_estado.extend([0.0] * (fila - len(tempos_estado) + 1))
    tempos_estado[fila] += tempo_global - sum(tempos_estado[:fila+1])
    
    # Verifica se há espaço na fila
    if fila < capacidade + servidores:
        fila += 1
        if fila > max_fila:
            max_fila = fila
        
        # Se houver servidor livre, agenda saída
        if fila <= servidores:
            tempo_atendimento = uniforme(3, 5)
            schedule_event("saida", tempo_global + tempo_atendimento)
    else:
        clientes_perdidos += 1
    
    # Agenda próxima chegada
    tempo_chegada = uniforme(2, 5)
    schedule_event("chegada", tempo_global + tempo_chegada)

def saida(servidores, capacidade):
    """Processa um evento de saída"""
    global fila, tempo_global, clientes_atendidos
    
    clientes_atendidos += 1
    
    # Atualiza tempo acumulado para o estado atual
    if fila >= len(tempos_estado):
        tempos_estado.extend([0.0] * (fila - len(tempos_estado) + 1))
    tempos_estado[fila] += tempo_global - sum(tempos_estado[:fila+1])
    
    fila -= 1
    
    # Se ainda há clientes esperando, agenda próxima saída
    if fila >= servidores:
        tempo_atendimento = uniforme(3, 5)
        schedule_event("saida", tempo_global + tempo_atendimento)

def next_event():
    """Obtém o próximo evento"""
    if eventos:
        return eventos.pop(0)
    return None

def run_simulation(servidores, capacidade):
    """Executa a simulação"""
    global tempo_global, count, fila, max_fila, tempos_estado, eventos
    global clientes_perdidos, clientes_atendidos, clientes_chegaram
    
    # Reinicializa variáveis
    tempo_global = 0.0
    fila = 0
    max_fila = 0
    tempos_estado = [0.0]
    eventos = []
    clientes_perdidos = 0
    clientes_atendidos = 0
    clientes_chegaram = 0
    
    # Agenda primeira chegada no tempo 2.0
    schedule_event("chegada", 2.0)
    
    while count > 0 and eventos:
        evento = next_event()
        tempo_global = evento[0]
        
        if evento[1] == "chegada":
            chegada(servidores, capacidade)
        elif evento[1] == "saida":
            saida(servidores, capacidade)
    
    # Atualiza tempos para o estado final
    if fila < len(tempos_estado):
        tempos_estado[fila] += tempo_global - sum(tempos_estado[:fila+1])
    else:
        tempos_estado.extend([0.0] * (fila - len(tempos_estado) + 1))
        tempos_estado[fila] = tempo_global - sum(tempos_estado[:fila])

def print_results(servidores, capacidade):
    """Imprime os resultados"""
    print("\n" + "="*50)
    print(f"Resultados para G/G/{servidores}/{capacidade}")
    print(f"Chegadas entre 2-5, atendimento entre 3-5")
    print("="*50)
    
    print(f"\nTempo total de simulação: {tempo_global:.2f}")
    print(f"Clientes que chegaram: {clientes_chegaram}")
    print(f"Clientes atendidos: {clientes_atendidos}")
    print(f"Clientes perdidos: {clientes_perdidos}")
    print(f"Tamanho máximo da fila: {max_fila}")
    
    print("\nDistribuição de probabilidade dos estados:")
    for i in range(len(tempos_estado)):
        prob = tempos_estado[i] / tempo_global * 100
        print(f"Estado {i}: {tempos_estado[i]:.2f} unidades de tempo ({prob:.2f}%)")

def plot_results(servidores, capacidade):
    """Gera gráfico dos resultados"""
    probabilidades = [t/tempo_global*100 for t in tempos_estado]
    estados = list(range(len(tempos_estado)))
    
    plt.bar(estados, probabilidades)
    plt.xlabel('Estado da Fila (número de clientes)')
    plt.ylabel('Probabilidade (%)')
    plt.title(f'Distribuição de Probabilidade - G/G/{servidores}/{capacidade}')
    plt.show()

def main():
    """Função principal"""
    # Simulação G/G/1/5
    run_simulation(servidores=1, capacidade=5)
    print_results(servidores=1, capacidade=5)
    plot_results(servidores=1, capacidade=5)
    
    # Simulação G/G/2/5
    run_simulation(servidores=2, capacidade=5)
    print_results(servidores=2, capacidade=5)
    plot_results(servidores=2, capacidade=5)

if __name__ == "__main__":
    main()
