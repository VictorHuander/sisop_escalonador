import random
import heapq

class Processo:
    def __init__(self, pid, prioridade):
        self.pid = pid
        self.prioridade = prioridade
        self.creditos = prioridade
        self.tempo_executando = 0
        self.estado = "Pronto"
        self.tempo_total = 0  # Turnaround time

    def __lt__(self, other):
        # Compara o processo para organização na heap (por maior crédito e PID menor)
        if self.creditos == other.creditos:
            return self.pid < other.pid
        return self.creditos > other.creditos

    def perder_credito(self):
        # Processo perde um crédito e aumenta o tempo de execução
        if self.creditos > 0:
            self.creditos -= 1
            self.tempo_executando += 1
        else:
            self.estado = "Pronto"  # Processo fica pronto novamente

    def bloquear(self):
        self.estado = "Bloqueado"
    
    def desbloquear(self):
        self.estado = "Pronto"

    def resetar_creditos(self):
        # Fórmula cred = cred/2 + prio - 1
        self.creditos = self.creditos // 2 + self.prioridade - 1
        if self.creditos > 0:
            self.estado = "Pronto"

def escalonador(processos, tempo_simulacao):
    fila_prontos = []  # Heap para fila de prontos baseada nos créditos
    processos_bloqueados = []  # Lista para processos bloqueados
    tempo_atual = 0  # Relógio de tempo
    historico_estados = []

    # Inicializa a fila de prontos
    for processo in processos:
        heapq.heappush(fila_prontos, processo)

    while tempo_atual < tempo_simulacao:
        # Verifica se há processos na fila de prontos
        if fila_prontos:
            # Seleciona o processo com maior crédito
            processo_atual = heapq.heappop(fila_prontos)
            processo_atual.estado = "Executando"
            historico_estados.append((tempo_atual, processo_atual.pid, processo_atual.estado))
            
            # Executa o processo atual por 1ms
            processo_atual.perder_credito()
            processo_atual.tempo_total += 1

            # Simula uma chance de bloqueio por operações de E/S
            if random.random() < 0.05:  # 5% de chance de bloquear
                processo_atual.bloquear()
                processos_bloqueados.append(processo_atual)
            elif processo_atual.creditos > 0:
                heapq.heappush(fila_prontos, processo_atual)  # Reinsere na fila de prontos se ainda houver créditos
            else:
                processo_atual.estado = "Pronto"  # Volta ao estado pronto se os créditos acabarem
                heapq.heappush(fila_prontos, processo_atual)  # Reinsere na fila de prontos

        # Reatribuição de créditos se todos os processos na fila de prontos tiverem créditos zerados
        if all(p.creditos == 0 for p in fila_prontos):
            for p in fila_prontos:
                p.resetar_creditos()
            for p in processos_bloqueados:
                p.resetar_creditos()
            fila_prontos = [p for p in fila_prontos if p.estado == "Pronto"]
            heapq.heapify(fila_prontos)

        # Desbloqueio de processos aleatoriamente
        if processos_bloqueados and random.random() < 0.1:  # 10% de chance de desbloquear um processo bloqueado
            processo_desbloqueado = processos_bloqueados.pop(0)
            processo_desbloqueado.desbloquear()
            heapq.heappush(fila_prontos, processo_desbloqueado)

        tempo_atual += 1

    return historico_estados, processos

# Exemplo de uso:
processos =  [
    Processo(pid=1, prioridade=5),
    Processo(pid=2, prioridade=3),
    Processo(pid=3, prioridade=8),
    Processo(pid=4, prioridade=2),
    Processo(pid=5, prioridade=7)
]
tempo_simulacao = 100  # 100ms de tempo de simulação
historico, processos_finais = escalonador(processos, tempo_simulacao)

# Exibe o histórico de estados dos processos ao longo do tempo
print("Histórico de Estados:")
for t, pid, estado in historico:
    print(f"Tempo {t}ms - Processo {pid} está {estado}")

# Exibe o tempo de execução final e turnaround time de cada processo
print("\nResumo dos Processos:")
for processo in processos_finais:
    print(f"Processo {processo.pid}:")
    print(f"  Tempo de Execução (CPU): {processo.tempo_executando}ms")
    print(f"  Turnaround Time: {processo.tempo_total}ms")
    print(f"  Créditos Finais: {processo.creditos}")
    print(f"  Estado Final: {processo.estado}")
