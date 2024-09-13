import heapq

class Processo:

    def __init__(self, ordem, prioridade, surtoCpu, tempoEs, totalCpu):
        self.ordem = ordem
        self.prioridade = prioridade
        self.surtoCpu = surtoCpu
        self.countSurto = 0
        self.quantoParaAcabar = 0
        self.tempoEs = tempoEs
        self.totalCpu = totalCpu
        self.creditos = prioridade
        self.tempoCpu = 0
        self.ready = True
        self.blocked = False
        self.isExe = False
        self.ended = False
        self.credEnded = False
        self.processosEmCredito = 0
        self.estado = ""
        self.tempo_total = 0
    
    def __lt__(self, other):
        # Compara o processo para organização na heap (por maior crédito e PID menor)
        if self.creditos == other.creditos:
            return self.ordem < other.ordem
        return self.creditos > other.creditos
    
    def getEstadoAtual(self):
        if self.isExe == False:
            if self.ready == False:
                self.estado = "Blocked"
            else:
                self.estado = "Ready"
        else:
            self.estado = "Executing"
    
    def block(self):
        self.ready = False
        self.blocked = True
    
    
    def unlock(self):
        self.ready = True
        self.blocked = False
        self.getEstadoAtual()

    def resetar_creditos(self):
        if self.creditos == 0:
            self.creditos = self.creditos // 2 + self.prioridade

    def perder_credito(self):
        if self.fim_de_exec:
            return self.ended

        if self.isExe == True and self.creditos > 0:
            self.creditos -= 1
            self.tempo_total += 1
            if self.countSurto < self.surtoCpu and self.tempo_limite_cpu() == False:
                self.perder_credito()
            else:
                isExe = False
                
        if self.creditos == 0:
            self.credEnded = True

    def tempo_limite_cpu(self):
        if self.tempoCpu > self.tempoEs:
            self.block()
        else:
            return False
    
    def fim_de_exec(self):
        if self.quantoParaAcabar > self.totalCpu:
            self.ended = True
    
    def tempoEntradaSaida(self):
        if self.tempoEs > 0:
            self.tempoEs -=1
            self.getEstadoAtual()
        if self.tempoEs == 0:
            self.unlock()



    


def escalonador(processos, tempo_simulacao):
    fila_prontos = []  # Heap para fila de prontos baseada nos créditos
    processos_bloqueados = []  # Lista para processos bloqueados
    processos_sem_creditos = []
    tempo_atual = 0  # Relógio de tempo
    historico_estados = []

    # Inicializa a fila de prontos
    for processo in processos:
        heapq.heappush(fila_prontos, processo)

    while tempo_atual < tempo_simulacao:

        if len(fila_prontos) == 0:
            for processo in processos:
                processo.resetar_creditos()
                heapq.heappush(fila_prontos, processo)

        processo_atual = heapq.heappop(fila_prontos)
        processo_atual.isExe = True
        processo_atual.getEstadoAtual()
        historico_estados.append((tempo_atual, processo_atual.ordem, processo_atual.estado))

        # Executa o processo atual por 1ms
        processo_atual.perder_credito()
        
        
            

        for processo in processos_bloqueados:
            processo.tempoEntradaSaida()
            if processo.estado == "Ready":
                heapq.heappush(fila_prontos, processo)

        if processo_atual.ended == False:

            if processo_atual.credEnded:
                processos_sem_creditos.append(processo_atual)
        
            if processo_atual.estado == "Blocked":
                processos_bloqueados.append(processo_atual)

            if processo_atual.estado == "Ready":
                heapq.heappush(fila_prontos, processo_atual)
        
        if processo_atual.tempo_total == 0:
            tempo_atual += 1

        tempo_atual = tempo_atual + processo_atual.tempo_total

    return historico_estados, processos


# Exemplo de uso:
processos =  [
    Processo(ordem=1, prioridade=3, surtoCpu=2, tempoEs=5, totalCpu=6),
    Processo(ordem=2, prioridade=3, surtoCpu=3, tempoEs=10, totalCpu=6),
    Processo(ordem=3, prioridade=3, surtoCpu=0, tempoEs=0, totalCpu=14),
    Processo(ordem=4, prioridade=3, surtoCpu=0, tempoEs=0, totalCpu=10)
    #Processo(pid=5, prioridade=7)
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
    print(f"Processo {processo.ordem}:")
    print(f"  Tempo de Execução (CPU): {processo.tempo_total}ms")
    print(f"  Turnaround Time: {processo.tempo_total}ms")
    print(f"  Créditos Finais: {processo.creditos}")
    print(f"  Estado Final: {processo.estado}")

