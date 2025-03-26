import random

seed = 379
previus = seed
a = 1238123
c = 1293921
m = 1340459862
n = 100000

def nextRandom():
    global previus
    previus = ((a * previus) + c) % m
    return previus / m

def simularFila(servidores, capacidade_maxima, n, chegada_min, chegada_max, atendimento_min, atendimento_max):
    tempo_estados = [0] * (capacidade_maxima + 1)
    estado_fila = 0
    clientes_perdidos = 0
    tempo_simulacao = 0.0

    for _ in range(n):
        numero_aleatorio = nextRandom()
        tempo_chegada = chegada_min + (chegada_max - chegada_min) * nextRandom()  
        tempo_atendimento = atendimento_min + (atendimento_max - atendimento_min) * nextRandom() 
        if numero_aleatorio < 0.5: 
            if estado_fila < capacidade_maxima:
                estado_fila += 1
            else:
                clientes_perdidos += 1
        else: 
            if estado_fila > 0:
                estado_fila = max(0, estado_fila - servidores) 

        tempo_estados[estado_fila] += 1
        tempo_simulacao += (tempo_chegada + tempo_atendimento)

    calcular_probabilidades(tempo_estados, tempo_simulacao)
    print(f"Clientes perdidos: {clientes_perdidos}")
    print(f"Tempo total de simulação: {tempo_simulacao:.2f}")

def calcular_probabilidades(tempo_estados, tempo_simulacao):
    print("Distribuição de Probabilidade dos Estados da Fila:")
    for i, tempo in enumerate(tempo_estados):
        probabilidade = (tempo / tempo_simulacao) * 100
        print(f"Estado {i}: {probabilidade:.4f}%")

print("Simulação G/G/1/5:")
simular_fila(servidores=1, capacidade_maxima=5, n=n, chegada_min=2, chegada_max=5, atendimento_min=3, atendimento_max=5)

print("\nSimulação G/G/2/5:")
simular_fila(servidores=2, capacidade_maxima=5, n=n, chegada_min=2, chegada_max=5, atendimento_min=3, atendimento_max=5)
