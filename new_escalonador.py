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
        self.getEstadoAtual()
    
    def unlock(self):
        self.ready = True
        self.blocked = False
        self.getEstadoAtual()

    def resetar_creditos(self):
        if self.creditos == 0:
            self.creditos = self.creditos // 2 + self.prioridade

    def perder_credito(self):
        if self.fim_de_exec():
            return self.ended

        if self.isExe == True and self.creditos > 0:
            self.creditos -= 1
            
        if self.creditos == 0:
            self.credEnded = True


    def tempo_limite_cpu(self):
        if self.tempoCpu > self.totalCpu:
            self.block()
            return True
        else:
            return False
    
    def fim_de_exec(self):
        if self.quantoParaAcabar > self.totalCpu:
            self.ended = True
            self.quantoParaAcabar = 0
        else:
            self.quantoParaAcabar =+ 1
    
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
    processo_atual = ""
    

    # Inicializa a fila de prontos
    for processo in processos:
        heapq.heappush(fila_prontos, processo)

    while tempo_atual < tempo_simulacao:

        if len(fila_prontos) == 0:
            for processo in processos:
                processo.resetar_creditos()
                heapq.heappush(fila_prontos, processo)

        if processo_atual == "":
            processo_atual = heapq.heappop(fila_prontos)
            processo_atual.isExe = True

        if (processo_atual.surtoCpu != -1 and processo_atual.countSurto == processo_atual.surtoCpu) or processo_atual.tempo_limite_cpu() == True:
            processo_atual.isExe = False
            processo_atual.block()
            processos_bloqueados.append(processo_atual)
            processo_atual = heapq.heappop(fila_prontos)
            processo_atual.isExe = True
        
        processo_atual.getEstadoAtual()
        historico_estados.append((tempo_atual, processo_atual.ordem, processo_atual.estado, processo_atual.creditos))

        # Executa o processo atual por 1ms
        processo_atual.perder_credito()
        processo_atual.tempo_total += 1
        processo_atual.tempoCpu += 1

    

        processo_atual.countSurto += 1
        
            

        for processo in processos_bloqueados:
            if processo.tempoEs != -1:
                processo.tempoEntradaSaida()
                if processo.estado == "Ready":
                    heapq.heappush(fila_prontos, processo)

        if processo_atual.ended == False:
            print("entrei aqui")
            if processo_atual.creditos == 0:
                print("entrei aqui tambem")
                processo_atual.isExe = False
                processos_sem_creditos.append(processo_atual)
                processo_atual = heapq.heappop(fila_prontos)
                processo_atual.isExe = True
                print(len(processos_sem_creditos))

            elif processo_atual.estado == "Blocked":
                processos_bloqueados.append(processo_atual)
                processo_atual = heapq.heappop(fila_prontos)

        

        tempo_atual += 1

    return historico_estados, processos


# Exemplo de uso:
processos =  [
    Processo(ordem=1, prioridade=3, surtoCpu=2, tempoEs=5, totalCpu=6),
    Processo(ordem=2, prioridade=3, surtoCpu=3, tempoEs=10, totalCpu=6),
    Processo(ordem=3, prioridade=3, surtoCpu=-1, tempoEs=-1, totalCpu=14),
    Processo(ordem=4, prioridade=3, surtoCpu=-1, tempoEs=-1, totalCpu=10)
    #Processo(pid=5, prioridade=7)
]
tempo_simulacao = 40  # 100ms de tempo de simulação
historico, processos_finais = escalonador(processos, tempo_simulacao)


# Exibe o histórico de estados dos processos ao longo do tempo
print("Histórico de Estados:")
for t, pid, estado, creditos in historico:
    print(f"Tempo {t}ms - Processo {pid} está {estado} com {creditos} creditos")

# Exibe o tempo de execução final e turnaround time de cada processo
print("\nResumo dos Processos:")
for processo in processos_finais:
    print(f"Processo {processo.ordem}:")
    print(f"  Tempo de Execução (CPU): {processo.tempo_total}ms")
    print(f"  Turnaround Time: {processo.tempo_total}ms")
    print(f"  Créditos Finais: {processo.creditos}")
    print(f"  Estado Final: {processo.estado}")

